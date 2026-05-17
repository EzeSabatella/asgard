# docs/ — Índice de documentos del proyecto Asgard

Todo documento del proyecto vive en esta carpeta.  
El nombre del archivo es su identidad cronológica: `YYYYMMDD-HHMM_TIPO_descripcion.md`  
El documento con fecha más reciente sobre un tema es la versión válida.

---

## Convención de tipos

| Tipo | Descripción |
|---|---|
| `BRIEF` | Instrucciones de implementación para Gemini |
| `DECISION` | Decisiones arquitectónicas o de producto |
| `SPEC` | Especificaciones de componentes |
| `AUDIT` | Reportes de auditoría de código |
| `REPORT` | Reportes de estado, QA o desempeño |
| `CONTEXT` | Documentos de contexto y background |
| `MASTER` | Documentos maestros del proyecto |
| `UPDATE` | Enmiendas formales a documentos existentes |

---

## Documentos

| Fecha | Tipo | Archivo | Descripción |
|---|---|---|---|
| Pre-convención | CONTEXT | [database_schemas.md](database_schemas.md) | Schemas SQL (SQLite) y Cypher (Neo4j) del sistema |
| 20260503-0000 | MASTER | [../SUPERAGENT.md](../SUPERAGENT.md) | Documento maestro del proyecto — visión, arquitectura completa, fases |
| 20260503-0000 | MASTER | [../CLAUDE.md](../CLAUDE.md) | Manual de operación de Claude — roles, workflow, decisiones vigentes, skills |
| 20260503-1800 | DECISION | [20260503-1800_DECISION_decisions-log-sesion-01.md](20260503-1800_DECISION_decisions-log-sesion-01.md) | DEC-001 a DEC-014 — todas las decisiones arquitectónicas de la sesión inicial |
| 20260503-1810 | BRIEF | [20260503-1810_BRIEF_gemini-01-correcciones-base.md](20260503-1810_BRIEF_gemini-01-correcciones-base.md) | Gemini Brief 01 — `__init__.py`, ConversationObserver, BaseProfile |
| 20260503-1820 | BRIEF | [20260503-1820_BRIEF_gemini-02-sistema-configuracion.md](20260503-1820_BRIEF_gemini-02-sistema-configuracion.md) | Gemini Brief 02 — chassis.config.yaml + config.py |
| 20260503-1830 | BRIEF | [20260503-1830_BRIEF_gemini-03-capa-stores.md](20260503-1830_BRIEF_gemini-03-capa-stores.md) | Gemini Brief 03 — BaseStore + RawStore (SQLite) |
| 20260503-1840 | BRIEF | [20260503-1840_BRIEF_gemini-04-embeddings-clasificador.md](20260503-1840_BRIEF_gemini-04-embeddings-clasificador.md) | Gemini Brief 04 — EmbeddingProvider + OpenAI + Classifier |
| 20260503-1850 | BRIEF | [20260503-1850_BRIEF_gemini-05-api-mcp-tests.md](20260503-1850_BRIEF_gemini-05-api-mcp-tests.md) | Gemini Brief 05 — API REST + MCP skeleton + tests integración |
| 20260503-1900 | CONTEXT | [20260503-1900_CONTEXT_asgard-odin-naming-vision.md](20260503-1900_CONTEXT_asgard-odin-naming-vision.md) | Canon de nombres Asgard / Hugmun IA — fuente de verdad para naming del ecosistema |
| 20260503-2036 | AUDIT | [20260503-2036_AUDIT_brief-01-correcciones-base.md](20260503-2036_AUDIT_brief-01-correcciones-base.md) | Auditoría Brief 01 — APROBADO. Observer renaming, BaseProfile, __init__.py |
| 20260503-2113 | AUDIT | [20260503-2113_AUDIT_brief-02-sistema-configuracion.md](20260503-2113_AUDIT_brief-02-sistema-configuracion.md) | Auditoría Brief 02 — APROBADO. chassis.config.yaml + config.py + tests |
| 20260503-2316 | AUDIT | [20260503-2316_AUDIT_brief-03-capa-stores.md](20260503-2316_AUDIT_brief-03-capa-stores.md) | Auditoría Brief 03 — APROBADO CON CORRECCIONES. RawStore + BaseStore + tests |
| 20260503-2332 | AUDIT | [20260503-2332_AUDIT_brief-04-embeddings-clasificador.md](20260503-2332_AUDIT_brief-04-embeddings-clasificador.md) | Auditoría Brief 04 — APROBADO CON CORRECCIONES. EmbeddingProvider + Classifier + tests |
| 20260503-2339 | AUDIT | [20260503-2339_AUDIT_brief-05-api-mcp-tests.md](20260503-2339_AUDIT_brief-05-api-mcp-tests.md) | Auditoría Brief 05 — APROBADO. FastAPI REST + MCP skeleton + 22/22 suite verde |
| 20260510-2330 | CONTEXT | [20260510-2330_CONTEXT_vision-asgard-coloquial.md](20260510-2330_CONTEXT_vision-asgard-coloquial.md) | Visión completa de Asgard en lenguaje coloquial — para contexto con LLMs y referencia personal |

---

*Actualizar esta tabla cada vez que se crea un documento nuevo.*
