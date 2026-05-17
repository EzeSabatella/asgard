# Brief 04 — Embeddings + Clasificador

**Tipo:** BRIEF  
**Fecha:** 2026-05-03 18:40  
**Autor:** Claude  
**Relacionado con:** DEC-014, DEC-005 (docs/20260503-1800_DECISION_decisions-log-sesion-01.md)  
**Estado:** Vigente

---

## Objetivo

Implementar la interfaz abstracta de embeddings (con provider OpenAI para MVP) y el clasificador que recibe un `ConversationTurn` y determina qué observers deben procesarlo.

## Skills a activar

- [ ] `ai-ml-engineer` — EmbeddingProvider, aggressiveness, ConversationObserver contracts
- [ ] `python-backend-dev` — interfaces abstractas, async, OpenAI client

## Contexto — documentos a leer primero

- `CLAUDE.md` — sección "Embeddings" y "Clasificador"
- `SUPERAGENT.md` — sección "Pipeline de procesamiento"
- `docs/20260503-1800_DECISION_decisions-log-sesion-01.md` — DEC-014 (embeddings abstractos)
- `chassis/src/chassis/observers/base.py` — `ConversationObserver.is_relevant()` (el clasificador la invoca)
- `chassis/src/chassis/observers/registry.py` — cómo se accede al catálogo de observers
- `chassis/src/chassis/config.py` (Brief 02) — `get_config()` para leer provider y aggressiveness

---

## Tareas

### Tarea 1: Interfaz abstracta `EmbeddingProvider`

**Archivo a crear:**
- `chassis/src/chassis/embeddings/base.py`

**Contrato:**

```python
from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    """Abstract interface for embedding generation."""

    @property
    @abstractmethod
    def dimensions(self) -> int:
        """Number of dimensions in the output vector."""
        ...

    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Returns embedding vector for a single text."""
        ...

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Returns embedding vectors for a batch of texts. More efficient than N embed_text calls."""
        ...
```

**Constraints:**
- No lógica de retry ni caching en esta clase base — eso va en las implementaciones concretas
- El resultado de `embed_text` debe ser una lista de floats de longitud `self.dimensions`

---

### Tarea 2: Implementación `OpenAIEmbeddingProvider`

**Archivo a crear:**
- `chassis/src/chassis/embeddings/openai.py`

**Contrato:**

```python
from typing import List, Optional
from openai import AsyncOpenAI
from chassis.embeddings.base import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """
    OpenAI embeddings via the official async client.
    Model default: text-embedding-3-small (1536 dimensions).
    """

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        dimensions: int = 1536,
    ):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed_text(self, text: str) -> List[float]:
        response = await self._client.embeddings.create(
            input=text,
            model=self._model,
        )
        return response.data[0].embedding

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        response = await self._client.embeddings.create(
            input=texts,
            model=self._model,
        )
        return [item.embedding for item in response.data]
```

**Constraints:**
- El `api_key` se inyecta desde fuera — nunca leerlo directamente desde `os.environ` dentro de esta clase
- Usar `openai>=1.0.0` (cliente async nativo, no el legacy)
- `openai` debe agregarse a `requirements.txt`
- No implementar retry aquí — el caller maneja errores de la API

---

### Tarea 3: Actualizar `embeddings/__init__.py`

**Archivo a modificar:**
- `chassis/src/chassis/embeddings/__init__.py`

**Contenido:**

```python
from chassis.embeddings.base import EmbeddingProvider
from chassis.embeddings.openai import OpenAIEmbeddingProvider

__all__ = ["EmbeddingProvider", "OpenAIEmbeddingProvider"]
```

---

### Tarea 4: Clasificador de ConversationTurn

**Archivo a modificar:**
- `chassis/src/chassis/classifier/__init__.py`

**Contrato completo del módulo:**

```python
from typing import List
from chassis.models.context import ConversationTurn
from chassis.observers.base import ConversationObserver
from chassis.observers.registry import ObserverRegistry
from chassis.config import get_config


class Classifier:
    """
    Determines which ConversationObservers should process a given turn.
    Uses each observer's is_relevant() + aggressiveness threshold from config.
    """

    def __init__(self, registry: ObserverRegistry):
        self._registry = registry

    def classify(self, turn: ConversationTurn) -> List[ConversationObserver]:
        """
        Returns the list of observers that should process this turn.

        Selection criteria:
        1. Observer is in config.observers.enabled
        2. observer.is_relevant(turn) returns True
        3. observer.aggressiveness >= threshold defined in config (default 0.0)
        """
        config = get_config()
        enabled_names = set(config.observers.enabled)
        aggressiveness_map = config.observers.aggressiveness

        selected = []
        for observer in self._registry.get_all():
            if observer.name not in enabled_names:
                continue
            threshold = aggressiveness_map.get(observer.name, 0.0)
            if observer.aggressiveness < threshold:
                continue
            if observer.is_relevant(turn):
                selected.append(observer)

        return selected
```

**Constraints:**
- El clasificador NO llama a `observe()` — solo decide quién debe hacerlo
- La selección es síncrona (no async) — `is_relevant()` no debe hacer I/O
- Si `config.observers.aggressiveness` no tiene entry para un observer, el threshold default es `0.0` (pasa siempre si está en `enabled` y `is_relevant`)

---

### Tarea 5: Tests de embeddings y clasificador

**Archivos a crear:**
- `chassis/tests/test_embeddings.py`
- `chassis/tests/test_classifier.py`

**Tests de embeddings (usar `unittest.mock` para mockear el cliente OpenAI):**

```python
async def test_embed_text_returns_correct_dimensions():
    """embed_text retorna lista de floats con longitud == provider.dimensions."""

async def test_embed_batch_returns_one_vector_per_text():
    """embed_batch retorna una lista con la misma longitud que la entrada."""
```

**Tests del clasificador:**

```python
def test_disabled_observer_not_selected():
    """Observer fuera de config.observers.enabled no se selecciona."""

def test_irrelevant_observer_not_selected():
    """Observer cuyo is_relevant() retorna False no se selecciona."""

def test_relevant_enabled_observer_selected():
    """Observer habilitado y relevante aparece en el resultado."""

def test_aggressiveness_below_threshold_excluded():
    """Observer con aggressiveness menor al threshold del config no se selecciona."""
```

**Constraints:**
- Los tests del clasificador usan observers mock (`MagicMock`) — no dependen de implementaciones reales
- No hacer llamadas reales a la API de OpenAI en los tests — siempre mockear

---

## Lo que NO entra en este brief

- Implementar ChromaDB store de vectores — es Fase 1
- Implementar el pipeline completo (clasificar → observar → guardar)
- Crear endpoints de API
- Implementar `OllamaEmbeddingProvider` (es producción, no MVP)

## Definición de Done

- [ ] `from chassis.embeddings import EmbeddingProvider, OpenAIEmbeddingProvider` funciona
- [ ] `from chassis.classifier import Classifier` funciona
- [ ] `Classifier.classify()` respeta los 3 criterios de selección
- [ ] Tests de embeddings pasan (con mock del cliente OpenAI)
- [ ] Tests del clasificador pasan (4 tests)
- [ ] `openai>=1.0.0` en `requirements.txt`
- [ ] Sin credenciales hardcodeadas (el api_key se inyecta, no se lee del env)
