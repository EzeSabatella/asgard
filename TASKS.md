# TASKS — Asgard

_Última actualización: 2026-05-17_

---

## En progreso

- [ ] Levantar chassis FastAPI en servidor `antigravity` (Dockerfile + docker-compose.yml)

---

## Próximas tareas (desbloqueadas tras el deploy)

### Fase 1 — Observadores emocionales y clasificador LLM

- [ ] Diseñar spec para `EmpathicObserver`
- [ ] Diseñar spec para `HumorObserver`
- [ ] Diseñar spec para `SocialObserver`
- [ ] Spec del clasificador LLM (llama3.2:3b vía Ollama)
- [ ] Spec del consolidador con LLM

### Fase 1 — Patrones y grafo

- [ ] Spec del detector de patrones de co-activación
- [ ] Alimentar Neo4j con eventos del store

### Fase 1 — MCP completo

- [ ] Spec MCP bidireccional (input `ConversationTurn` + output `ContextResponse`)

### Fase 1-2 — Handoff / Session Context

- [ ] Spec de Session Context export (paquete de contexto portable para inyectar en cualquier LLM)
- [ ] Endpoint o CLI: `asgard handoff --project X --to claude|gemini|chatgpt`

---

## Backlog (Fase 2+)

- [ ] Identity Layer del asistente (Odín) — nombre, tono, propósito, reglas; separado del perfil del usuario
- [ ] CLI `asgard context / handoff / list-projects` (primera interfaz de salida del sistema)
- [ ] `SystemObserver` (base)
- [ ] Völundr — detección de gaps y generación de skill proposals
- [ ] Embeddings Ollama (switch de config, sin cambio de código)
- [ ] `EnterpriseProfile` con `OrganizationalProfile`
- [ ] Integración con Odín, Freyja, Nexus
- [ ] Zero-knowledge cloud (prerequisito para distribución masiva)
- [ ] Sistema de decay temporal de perfil
- [ ] Contradiction detection en consolidador
- [ ] Periodic review proposals al usuario
- [ ] Model Router — rutear a Claude / Gemini / ChatGPT / modelo local según tipo de tarea (Fase 3)

---

## Congelado

- Nexus (vive en PC personal, pendiente de subir a GitHub)
- FrameworkForecast (pendiente de subir a GitHub)
- Hugmun IA (identidad definida, sistema comercial pendiente)

---

## Terminado ✅

- [x] Estructura del monorepo
- [x] `BaseProfile` + `PersonalProfile` + `EnterpriseProfile`
- [x] `BaseStore` + `RawStore` (SQLite + aiosqlite)
- [x] `ConversationObserver` base + `TechnicalObserver`
- [x] Clasificador heurístico (sin LLM)
- [x] ChromaDB + interfaz abstracta de embeddings + proveedor OpenAI
- [x] FastAPI REST completo
- [x] MCP skeleton (`tools/list` + `tools/call`)
- [x] `chassis.config.yaml` + config loader
- [x] Docker Compose (Neo4j + ChromaDB)
- [x] Suite de tests (22/22 verde)
- [x] Setup servidor `antigravity` (Tailscale + Ollama + ChromaDB)
