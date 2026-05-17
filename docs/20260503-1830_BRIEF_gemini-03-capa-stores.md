# Brief 03 — Capa de stores (almacenamiento raw)

**Tipo:** BRIEF  
**Fecha:** 2026-05-03 18:30  
**Autor:** Claude  
**Relacionado con:** SUPERAGENT.md sección "Capa de Almacenamiento"  
**Estado:** Vigente

---

## Objetivo

Implementar la capa de almacenamiento raw del chassis: interfaz abstracta `BaseStore` y su implementación concreta `RawStore` sobre SQLite (con SQLCipher para producción). Los stores reciben eventos clasificados y los persisten con `consolidated = False`.

## Skills a activar

- [ ] `data-engineer` — SQLite, separación física de stores, invariante consolidated=False
- [ ] `python-backend-dev` — interfaces abstractas, Pydantic, async

## Contexto — documentos a leer primero

- `CLAUDE.md` — sección "Almacenamiento"
- `SUPERAGENT.md` — sección "Cinco stores", invariante `consolidated = False`
- `chassis/src/chassis/models/events.py` — modelos de eventos (lo que entra al store)
- `docs/database_schemas.md` — schemas SQL de referencia

---

## Tareas

### Tarea 1: Interfaz abstracta `BaseStore`

**Archivo a crear:**
- `chassis/src/chassis/stores/base.py`

**Contrato:**

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from chassis.models.events import BaseEvent


class BaseStore(ABC):
    """Abstract interface for all event stores."""

    @abstractmethod
    async def save_event(self, event: BaseEvent) -> str:
        """
        Persists a single event. Returns the event_id assigned.
        INVARIANT: consolidated is always set to False on write.
        """
        ...

    @abstractmethod
    async def save_events(self, events: List[BaseEvent]) -> List[str]:
        """Persists multiple events atomically. Returns list of event_ids."""
        ...

    @abstractmethod
    async def get_unconsolidated(self, limit: int = 100) -> List[BaseEvent]:
        """Returns events where consolidated = False, ordered by created_at ASC."""
        ...

    @abstractmethod
    async def mark_consolidated(self, event_ids: List[str]) -> int:
        """
        Sets consolidated = True for the given event_ids.
        Returns count of rows updated.
        ONLY the consolidator may call this method.
        """
        ...

    @abstractmethod
    async def get_by_id(self, event_id: str) -> Optional[BaseEvent]:
        """Returns a single event by its ID, or None if not found."""
        ...
```

**Constraints:**
- `save_event` y `save_events` NUNCA pueden escribir `consolidated = True` — si el caller lo pasa como True, ignorarlo y forzar False
- Esta interfaz no sabe si usa SQLite, PostgreSQL, u otro backend

---

### Tarea 2: Implementación `RawStore` (SQLite)

**Archivo a crear:**
- `chassis/src/chassis/stores/raw.py`

**Contrato:**

```python
import aiosqlite
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from chassis.stores.base import BaseStore
from chassis.models.events import BaseEvent


class RawStore(BaseStore):
    """
    SQLite implementation of BaseStore.
    In production, SQLite file is encrypted with SQLCipher.
    In development/tests, runs without encryption.
    """

    def __init__(self, db_path: Path, encryption_key: Optional[str] = None):
        self.db_path = db_path
        self.encryption_key = encryption_key  # None = no encryption (dev/test)

    async def initialize(self) -> None:
        """Creates tables if they don't exist. Call once at startup."""
        ...

    async def save_event(self, event: BaseEvent) -> str:
        """Stores event with consolidated=False regardless of input."""
        ...

    async def save_events(self, events: List[BaseEvent]) -> List[str]:
        """Atomic batch insert, all with consolidated=False."""
        ...

    async def get_unconsolidated(self, limit: int = 100) -> List[BaseEvent]:
        ...

    async def mark_consolidated(self, event_ids: List[str]) -> int:
        ...

    async def get_by_id(self, event_id: str) -> Optional[BaseEvent]:
        ...
```

**Schema de la tabla `events` (SQLite):**

```sql
CREATE TABLE IF NOT EXISTS events (
    event_id    TEXT PRIMARY KEY,
    event_type  TEXT NOT NULL,
    source      TEXT NOT NULL,
    content     TEXT NOT NULL,        -- JSON serializado del evento completo
    created_at  TEXT NOT NULL,        -- ISO 8601
    consolidated INTEGER NOT NULL DEFAULT 0  -- 0=False, 1=True
);

CREATE INDEX IF NOT EXISTS idx_events_consolidated
    ON events (consolidated, created_at);
```

**Serialización de eventos:**
- El campo `content` almacena el evento como JSON (`event.model_dump_json()`)
- Al leer, deserializar con `BaseEvent.model_validate_json(row["content"])`

**Constraints:**
- `aiosqlite` debe agregarse a `requirements.txt`
- El `encryption_key` se inyecta desde la variable de entorno `CHASSIS_DB_KEY` — el store no la lee directamente (se la pasa quien lo instancia)
- Si `encryption_key is None`, el store funciona igual pero sin cifrado (modo desarrollo)
- El método `initialize()` debe ser idempotente (puede llamarse múltiples veces)
- No usar ORM — SQL directo con `aiosqlite`

---

### Tarea 3: Actualizar `stores/__init__.py`

**Archivo a modificar:**
- `chassis/src/chassis/stores/__init__.py`

**Contenido:**

```python
from chassis.stores.base import BaseStore
from chassis.stores.raw import RawStore

__all__ = ["BaseStore", "RawStore"]
```

---

### Tarea 4: Tests del store

**Archivo a crear:**
- `chassis/tests/test_raw_store.py`

**Contrato de tests (usar `pytest-asyncio` y base de datos en memoria `:memory:`):**

```python
async def test_save_event_forces_consolidated_false():
    """Guardar un evento con consolidated=True debe persistir como False."""

async def test_save_events_atomic():
    """save_events persiste todos los eventos o ninguno."""

async def test_get_unconsolidated_returns_only_false():
    """get_unconsolidated no retorna eventos ya consolidados."""

async def test_mark_consolidated_updates_count():
    """mark_consolidated retorna el número correcto de filas actualizadas."""

async def test_get_by_id_returns_none_for_missing():
    """get_by_id retorna None para un event_id inexistente."""
```

**Constraints:**
- Usar `db_path=Path(":memory:")` para los tests (no archivos en disco)
- `pytest-asyncio` debe agregarse a `requirements.txt` si no está

---

## Lo que NO entra en este brief

- Implementar `PatternStore` (ChromaDB) — es Brief 04
- Implementar `GraphStore` (Neo4j) — es Fase 1
- Implementar el consolidador que llama a `mark_consolidated`
- Crear dos instancias de RawStore (raw_technical.db + raw_emotional.db) — eso lo hace el startup de la app

## Definición de Done

- [ ] `from chassis.stores import BaseStore, RawStore` funciona sin error
- [ ] El invariante `consolidated = False` es imposible de violar desde `save_event` / `save_events`
- [ ] `initialize()` crea la tabla y los índices correctamente
- [ ] Los 5 tests pasan
- [ ] `aiosqlite` en `requirements.txt`
- [ ] Sin credenciales hardcodeadas