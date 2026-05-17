# Auditoría Brief 03 — Capa de stores (almacenamiento raw)

**Tipo:** AUDIT  
**Fecha:** 2026-05-03 23:16  
**Autor:** Claude  
**Brief auditado:** [20260503-1830_BRIEF_gemini-03-capa-stores.md](20260503-1830_BRIEF_gemini-03-capa-stores.md)  
**Estado:** APROBADO CON CORRECCIONES

---

## Veredicto

**APROBADO** — lógica de negocio y arquitectura correctas. Dos bugs de infraestructura corregidos durante la auditoría. 5/5 tests pasando.

---

## Checklist de seguridad

- [x] Sin credenciales hardcodeadas
- [x] Sin rutas absolutas hardcodeadas
- [x] Sin contenido de eventos en logs
- [x] El `encryption_key` se inyecta desde fuera — el store no lee env vars directamente
- [!] `PRAGMA key` usa f-string: `f"PRAGMA key='{self.encryption_key}'"` — SQLite no permite parámetros en PRAGMAs, así que no hay alternativa. La clave viene de variable de entorno (no de input de usuario), riesgo acotado. Aceptable para MVP.

## Checklist de arquitectura

- [x] `RawStore` implementa `BaseStore` correctamente
- [x] Invariante `consolidated = False` enforced en `save_event` y `save_events` — usa `model_copy()` para no mutar el objeto original
- [x] `mark_consolidated` solo actualiza, no crea eventos
- [x] SQL directo con aiosqlite — sin ORM
- [x] Schema y índices del `database_schemas.md` presentes

## Checklist de código

- [x] Tipos completos en todas las signatures
- [x] Sin imports no utilizados (post-corrección)
- [x] `stores/__init__.py` expone `BaseStore` y `RawStore`

---

## Bugs encontrados y corregidos

### Bug 1 — Doble-await en `_get_conn()` (bloqueante)

**Síntoma:** `RuntimeError: threads can only be started once` al ejecutar cualquier test.

**Causa:** El método `_get_conn()` hacía `await aiosqlite.connect(...)` (iniciaba el thread interno de aiosqlite), y luego los callers hacían `async with await self._get_conn() as db:` — llamando a `__aenter__` sobre una conexión ya iniciada, lo que intenta arrancar el thread una segunda vez.

**Corrección:** Se eliminó `_get_conn()` por completo. `initialize()` abre la conexión una vez y la guarda en `self._db`. Todos los métodos operan directamente sobre `self._db`.

---

### Bug 2 — Una conexión nueva por operación rompe `:memory:` (bloqueante)

**Síntoma:** El Bug 1 enmascaró este segundo problema. Cada vez que `_get_conn()` abría una conexión a `:memory:`, SQLite entregaba una base de datos vacía nueva. Los datos escritos en `initialize()` no eran visibles en `save_event()`, ni los de `save_event()` en `get_by_id()`.

**Causa:** Las bases de datos `:memory:` en SQLite son efímeras por conexión. Una nueva `aiosqlite.connect(Path(":memory:"))` siempre da una base vacía.

**Corrección:** `RawStore` mantiene una única conexión persistente (`self._db`) abierta desde `initialize()` hasta el cierre del store. La lógica de idempotencia se implementa con `if self._db is not None: return` al inicio de `initialize()`.

**Implicación para producción:** Con archivos reales en disco (`.db`), el bug original también habría fallado porque cada operación abría y cerraba su propia conexión, sin aprovechar transacciones compartidas y con overhead innecesario. La conexión persistente es mejor en todos los casos.

---

### Correcciones de infraestructura de tests (no bloqueantes, necesarias)

**`test_raw_store.py` — fixture async:** El fixture `store` usaba `@pytest.fixture` sobre una función `async`. En pytest-asyncio 0.21+ con modo STRICT, los fixtures async requieren `@pytest_asyncio.fixture`. Corregido: se cambió el decorador y se agregó `import pytest_asyncio`.

**`pyproject.toml` — asyncio_mode:** pytest-asyncio instalado sin configurar `asyncio_mode` corre en modo STRICT por defecto. Se agregó:
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

---

## Análisis del código entregado (post-corrección)

### `base.py` ✅

Copia exacta del contrato del brief. Limpio.

### `raw.py` ✅ (reescrito durante auditoría)

Arquitectura final: conexión única persistente en `self._db`, inicializada en `initialize()`. Todos los métodos operan sobre esa conexión. El invariante `consolidated = False` se enforcea mediante `model_copy()` antes de serializar. `save_events()` usa `executemany()` dentro de un único commit — atómico. `mark_consolidated()` construye placeholders dinámicos de forma segura (los valores van como parámetros, no interpolados).

### `stores/__init__.py` ✅

Correcto.

### `test_raw_store.py` ✅ (fixture corregido durante auditoría)

Los 5 tests verifican los comportamientos críticos del contrato. El test de `mark_consolidated` incluye un ID inexistente ("999") para verificar que el count solo cuenta filas realmente actualizadas — buen detalle de Gemini.

---

## Desviaciones del brief

- **`_get_conn()` helper:** Gemini introdujo un método privado no especificado en el brief. No es una desviación problemática en sí, pero la implementación tenía el bug descrito.
- **Correcciones de auditoría:** Los cambios a `raw.py`, `test_raw_store.py` y `pyproject.toml` fueron realizados por Claude durante la auditoría, no por Gemini. Se documentan aquí como parte del registro.

---

## Definición de Done — verificación

- [x] `from chassis.stores import BaseStore, RawStore` funciona sin error
- [x] Invariante `consolidated = False` es imposible de violar desde `save_event` / `save_events`
- [x] `initialize()` crea tabla e índices correctamente (idempotente)
- [x] Los 5 tests pasan (`5 passed in 0.09s`)
- [x] `aiosqlite` y `pytest-asyncio` en `requirements.txt` y `pyproject.toml`
- [x] Sin credenciales hardcodeadas