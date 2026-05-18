# STATUS — Asgard

_Última actualización: 2026-05-17_

---

## Estado general

**Fase 0 — MVP completado ✅**
22/22 tests pasando. Todos los componentes auditados y aprobados.

---

## Completado

- Estructura del monorepo
- `BaseProfile` + `PersonalProfile` + `EnterpriseProfile`
- Store bruto SQLite técnico (`BaseStore` + `RawStore` con aiosqlite)
- `ConversationObserver` base + `TechnicalObserver`
- Clasificador heurístico (sin LLM)
- ChromaDB + interfaz abstracta de embeddings + proveedor OpenAI
- FastAPI endpoints REST completos
- MCP skeleton (`tools/list` + `tools/call`)
- `chassis.config.yaml` + carga de configuración al startup
- Docker Compose con Neo4j
- Suite de tests (22/22)

---

## En progreso

- Chassis FastAPI: pendiente de containerizar o correr con Python directamente en el servidor

---

## Infraestructura de deploy ✅ (2026-05-17)

- [x] Git instalado en laptop
- [x] Repo `asgard` en GitHub: https://github.com/EzeSabatella/asgard
- [x] `git init` + primer commit + `git push`
- [x] `git clone` en servidor `antigravity` (192.168.1.40)
- [x] `docker compose up -d` — Neo4j + ChromaDB corriendo
- [x] Ollama operativo: `nomic-embed-text` + `llama3.2:3b`
- [x] Proveedores actualizados: Ollama embeddings + DeepSeek LLM (28/28 tests)

---

## Pendientes menores (no bloquean Fase 1)

- `GET /profile` no tiene `/{user_id}` en la ruta (stub, se corrige en Fase 1)
- Import `Optional` no usado en `embeddings/openai.py`
- Import `ValidationError` no usado en `tests/test_config.py`

---

## Próxima entrega esperada

**Fase 1** — Observadores emocionales, clasificador LLM (llama3.2:3b vía Ollama), consolidador, Neo4j alimentado, MCP bidireccional.
