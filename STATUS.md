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

- Setup de infraestructura de deploy:
  - [ ] Instalar Git en la laptop
  - [ ] Crear repo `asgard` en GitHub (privado)
  - [ ] `git init` + primer commit
  - [ ] `git push`
  - [ ] `git clone` en el servidor `antigravity` (192.168.1.43)
  - [ ] `docker compose up -d` en el servidor

---

## Bloqueado

- Deploy en servidor — bloqueado hasta completar el setup de Git/GitHub

---

## Pendientes menores (no bloquean Fase 1)

- `GET /profile` no tiene `/{user_id}` en la ruta (stub, se corrige en Fase 1)
- Import `Optional` no usado en `embeddings/openai.py`
- Import `ValidationError` no usado en `tests/test_config.py`

---

## Próxima entrega esperada

**Fase 1** — Observadores emocionales, clasificador LLM (llama3.2:3b vía Ollama), consolidador, Neo4j alimentado, MCP bidireccional.
