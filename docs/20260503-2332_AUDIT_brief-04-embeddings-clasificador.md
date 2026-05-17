# Auditoría Brief 04 — Embeddings + Clasificador

**Tipo:** AUDIT  
**Fecha:** 2026-05-03 23:32  
**Autor:** Claude  
**Brief auditado:** [20260503-1840_BRIEF_gemini-04-embeddings-clasificador.md](20260503-1840_BRIEF_gemini-04-embeddings-clasificador.md)  
**Estado:** APROBADO CON CORRECCIONES

---

## Veredicto

**APROBADO** — lógica de negocio correcta en todos los módulos. Un bug en los tests del clasificador corregido durante la auditoría. 6/6 tests pasando.

---

## Checklist de seguridad

- [x] Sin credenciales hardcodeadas
- [x] `api_key` se inyecta por parámetro — `OpenAIEmbeddingProvider` nunca lee `os.environ`
- [x] Sin rutas absolutas hardcodeadas

## Checklist de arquitectura

- [x] `EmbeddingProvider` es interfaz abstracta pura — sin lógica
- [x] `OpenAIEmbeddingProvider` implementa la interfaz correctamente
- [x] Proveedor detrás de interfaz abstracta — switch a Ollama es cambio de config, no de código ✅
- [x] `Classifier.classify()` es síncrono — `is_relevant()` no hace I/O
- [x] El clasificador NO llama a `observe()` — solo decide quién debe hacerlo
- [x] `get_config()` se invoca en cada `classify()` — correcto porque es singleton

## Checklist de código

- [x] Tipos completos en todas las signatures
- [!] `Optional` importado en `openai.py` pero no usado — import no utilizado (mismo patrón que el brief lo incluye, low priority)
- [x] `embeddings/__init__.py` expone correctamente las dos clases

---

## Bug encontrado y corregido

### `test_classifier.py` — `ConversationTurn` con campos incorrectos (bloqueante)

**Síntoma:** `ValidationError: 6 validation errors for ConversationTurn` en los 4 tests del clasificador.

**Causa:** Gemini construyó `ConversationTurn(speaker="user", text="hello")` pero el modelo real (`chassis/models/context.py`) requiere `user_id`, `session_id`, `turn_id`, `timestamp`, `role`, `content`. Los campos `speaker` y `text` no existen en el schema.

**Raíz:** Gemini no consultó el modelo concreto antes de escribir los tests — asumió una interfaz simplificada.

**Corrección:** Se agregó el helper `_make_turn()` con todos los campos requeridos y se reemplazaron las cuatro instanciaciones incorrectas.

---

## Análisis del código

### `embeddings/base.py` ✅

Copia exacta del contrato. Limpio.

### `embeddings/openai.py` ✅

Implementación correcta. El cliente `AsyncOpenAI` se instancia en `__init__` (no en cada llamada). `embed_batch` pasa la lista directamente a la API — correcto, OpenAI acepta arrays en el campo `input`. La respuesta se mapea en orden con `response.data[i].embedding`. Un import no usado (`Optional`) — heredado del contrato del brief, low priority.

### `classifier/__init__.py` ✅

Implementación idéntica al contrato. Los tres criterios de selección implementados en el orden correcto: enabled → aggressiveness threshold → is_relevant. El threshold default `0.0` cuando el observer no aparece en `aggressiveness_map` hace que pase siempre si está en `enabled` y es relevante — correcto según el brief.

### `test_embeddings.py` ✅

El mock de `AsyncOpenAI` parchea en el namespace correcto (`chassis.embeddings.openai.AsyncOpenAI`). El `mock_create` async distingue entre `str` y `list` para devolver respuestas distintas según el método testeado. Correcto.

### `test_classifier.py` ✅ (corregido)

4 tests cubren todos los criterios de selección. La lógica de mocking con `patch("chassis.classifier.get_config")` está bien aplicada — parchea en el punto de consumo. Post-corrección, todos los `ConversationTurn` usan el helper `_make_turn()` con el schema real.

---

## Desviaciones del brief

- **`test_classifier.py` — schema incorrecto:** Gemini no verificó el modelo real de `ConversationTurn` antes de escribir los tests. Corregido en auditoría.

---

## Definición de Done — verificación

- [x] `from chassis.embeddings import EmbeddingProvider, OpenAIEmbeddingProvider` funciona
- [x] `from chassis.classifier import Classifier` funciona
- [x] `Classifier.classify()` respeta los 3 criterios de selección
- [x] Tests de embeddings pasan (2/2, con mock del cliente OpenAI)
- [x] Tests del clasificador pasan (4/4)
- [x] `openai>=1.0.0` ya estaba en dependencias (openai 2.33.0 instalado)
- [x] Sin credenciales hardcodeadas