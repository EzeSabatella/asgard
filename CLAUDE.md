# CLAUDE.md — Asgard

> Documento de operación de Claude en este proyecto.
> Para la arquitectura completa del sistema, ver [SUPERAGENT.md](SUPERAGENT.md).
> Para el índice de todos los documentos del proyecto, ver [docs/INDEX.md](docs/INDEX.md).

---

## Roles

| Agente | Rol | Responsabilidades |
|---|---|---|
| **Claude** | Arquitecto / Auditor / Lead Developer | Diseño, specs, decisiones de arquitectura, auditoría de código, briefs para Gemini |
| **Gemini** | Ejecutor | Implementación de código según specs, estructura de archivos, tests |
| **Ezequiel** | Owner / Product | Decisiones de producto, validación, dirección estratégica, aprobación de Völundr |

**Entorno:** IDE Antigravity (Gemini nativo + extensión Claude). Solo estos dos modelos.

**Regla de discrepancias:** Cuando haya conflicto entre documentos, el más reciente es el válido. CLAUDE.md tiene prioridad sobre todo documento anterior. Toda discrepancia se reporta antes de actuar — nunca se reconcilia en silencio.

---

## Workflow estándar

```
Claude diseña: spec + brief para Gemini
        ↓
Claude usa /scribe para guardar el brief en docs/
        ↓
Ezequiel asigna el brief a Gemini
        ↓
Gemini ejecuta (activa los skills correspondientes de .agents/skills/)
        ↓
Claude audita con /code-auditor
        ↓
Claude usa /scribe para guardar el reporte de auditoría en docs/
        ↓
Ezequiel valida
        ↓
Capa completa → siguiente spec
```

### Reglas del workflow

- **El brief es el contrato** — Gemini no interpreta ni decide, ejecuta lo especificado
- **Gemini no toma decisiones de arquitectura** — si hay ambigüedad en la spec, el brief está incompleto y Claude lo corrige
- **Claude no reimplementa** — audita, corrige specs, propone mejoras
- **Toda decisión de arquitectura nueva se documenta** con `/scribe` (tipo `DECISION`) antes de ir a Gemini
- **Si Gemini desvía del brief**, Claude documenta la desviación en el reporte de auditoría

---

## Contexto del proyecto

Asgard es una plataforma de identidad digital persistente que construye una copia digital del usuario y la convierte en el contexto para cualquier LLM. El activo es el conocimiento acumulado sobre el usuario — sus decisiones, patrones cognitivos, proyectos, preferencias. Los LLMs se comoditizan; ese activo no.

**Arquitectura completa:** [SUPERAGENT.md](SUPERAGENT.md)

---

## Decisiones arquitectónicas vigentes

Estas decisiones están tomadas y no se re-discuten sin escalado explícito a Ezequiel.

### Interfaces y protocolos
- **MCP es la interfaz principal.** REST es la secundaria para testing e integraciones programáticas.
- **MCP bidireccional:** los clientes envían `ConversationTurn` (pasa por el pipeline de observadores) y leen `ContextResponse`.
- **El cliente nunca escribe directamente al store** — siempre pasa por el clasificador y los observadores.
- **MVP incluye skeleton MCP** (`tools/list` + `tools/call`) aunque no implementación completa.

### Storage
- **Cinco stores separados:** `raw_technical.db`, `raw_emotional.db`, ChromaDB (inferido), `patterns.db`, Neo4j.
- **Stores técnico y emocional son físicamente separados** — dos archivos SQLite distintos, siempre.
- **`consolidated = False`** en todo evento nuevo. Solo el consolidador lo marca `True`.
- **Encriptación en reposo** via SQLCipher. Clave siempre de variable de entorno.

### Modelos de datos
- **BaseProfile + extensiones tipadas:** `PersonalProfile(BaseProfile)` y `EnterpriseProfile(BaseProfile)`.
- Discriminador: `instance_type: Literal["personal", "enterprise"]`.
- Un solo sistema de storage para ambos tipos, discriminado por `instance_type`.

### Observadores
- **Dos jerarquías separadas:**
  - `ConversationObserver` — trigger: `ConversationTurn`, output: `List[BaseEvent]`
  - `SystemObserver` — trigger: estado del sistema (store de patrones), output: `SkillProposal`
- `Observer` (la clase actual de Gemini) debe renombrarse a `ConversationObserver`.
- Völundr es la primera implementación de `SystemObserver`.

### Völundr (Forge)
- **Detecta gaps → genera SKILL.md + código Python → notifica en `/proposals` → usuario aprueba → deploy.**
- **Nunca auto-deploya.** El deploy de una skill es una decisión de arquitectura (categoría `always_escalate`).
- El catálogo de skills es el filesystem: `.agents/skills/`.

### Configuración
- **`chassis.config.yaml`** controla el comportamiento (observadores activos, agresividad, embeddings, schedule, tipo de instancia).
- **`.env`** contiene solo secretos y credenciales — nunca en el repo.
- Los observadores se registran en código (decorador); el YAML solo los activa o desactiva por nombre.

### Instancias
- **Una instancia por entidad** (personal o enterprise). Sin multitenancy.
- El mismo código, configuración diferente. Portable via Docker Compose.

### Embeddings
- Proveedor detrás de interfaz abstracta. El switch OpenAI → Ollama es cambio de config, no de código.

---

## MVP — Scope actualizado

### Incluye
- Estructura del monorepo ✅ (completado, pendiente fix `__init__.py` en `models/` y `observers/`)
- `BaseProfile` + `PersonalProfile` + `EnterpriseProfile` (requiere actualizar profile.py de Gemini)
- Store bruto SQLite técnico (`stores/base.py` + `stores/raw.py`)
- `ConversationObserver` base (renombrar desde `Observer`) + `TechnicalObserver`
- Clasificador heurístico (sin LLM)
- ChromaDB + interfaz abstracta de embeddings + proveedor OpenAI
- FastAPI endpoints REST completos
- MCP skeleton: `tools/list` + `tools/call`
- `chassis.config.yaml` + carga de configuración al startup
- Docker Compose con Neo4j (ChromaDB comentado, SQLite file-based)
- Tests básicos del `TechnicalObserver`

### Excluye del MVP
- Observadores emocionales (Empathic, Humor, Social)
- `SystemObserver` + Völundr (Forge)
- Consolidador con LLM (MVP consolida con reglas)
- Detector de patrones de co-activación
- Neo4j alimentado (schema sí, datos no)
- Integración con Odín, Freyja, Nexus
- Embeddings Ollama
- MCP completo (bidireccional full)
- `EnterpriseProfile` con `OrganizationalProfile` (Fase 4)

---

## Skills del sistema

### Gemini — `.agents/skills/`
| Skill | Cuándo activarlo |
|---|---|
| `python-backend-dev` | FastAPI, Pydantic, lógica de negocio |
| `data-engineer` | SQLite, ChromaDB, Neo4j, schemas |
| `ai-ml-engineer` | Observers, embeddings, LangGraph, clasificador |
| `devops-engineer` | Docker Compose, variables de entorno |
| `qa-engineer` | Tests, cobertura, reportes con evidencia |

### Claude — `.claude/skills/`
| Skill | Cuándo usarlo |
|---|---|
| `/architecture-spec` | Diseñar un componente nuevo o redefinir un contrato |
| `/code-auditor` | Auditar implementación de Gemini |
| `/scribe` | Crear o actualizar cualquier documento del proyecto |

---

## Sistema de documentación

**Todo documento del proyecto vive en `docs/`.**

**Patrón de nombre:** `YYYYMMDD-HHMM_[TIPO]_[descripcion-kebab].md`

| Tipo | Uso |
|---|---|
| `BRIEF` | Instrucciones de implementación para Gemini |
| `DECISION` | Decisiones arquitectónicas o de producto |
| `SPEC` | Especificaciones de componentes |
| `AUDIT` | Reportes de auditoría |
| `REPORT` | Estado, QA, desempeño |
| `CONTEXT` | Background y referencia |
| `MASTER` | Documentos maestros |
| `UPDATE` | Enmiendas a documentos existentes |

El documento con fecha más reciente sobre un tema es la versión válida. Los documentos viejos no se borran — se marcan como reemplazados.

**Index:** [docs/INDEX.md](docs/INDEX.md) — actualizar con cada documento nuevo.

---

## Guía de operación por sesión

### Al iniciar una sesión nueva
1. Leer `CLAUDE.md` (este archivo)
2. Leer `SUPERAGENT.md` si hay dudas sobre la arquitectura
3. Revisar `docs/INDEX.md` para saber el estado actual del proyecto
4. Verificar si hay auditorías pendientes antes de avanzar

### Al diseñar (activar `/architecture-spec`)
- Producir specs explícitas — Gemini no interpreta, ejecuta
- Definir contratos antes de que se escriba una línea de código
- Si hay ambigüedad, preguntar a Ezequiel antes de asumir
- Guardar la spec con `/scribe` tipo `SPEC` o `BRIEF`

### Al auditar (activar `/code-auditor`)
Checklist invariante que aplica a toda auditoría:

**Seguridad:**
- [ ] Sin credenciales hardcodeadas
- [ ] Sin rutas absolutas hardcodeadas
- [ ] Contenido de eventos no aparece en logs en claro

**Arquitectura:**
- [ ] Implementa contra interfaces abstractas (no implementaciones concretas)
- [ ] Observadores registrados en registry, no instanciados directamente
- [ ] Proveedor de embeddings detrás de interfaz abstracta
- [ ] No modifica interfaces abstractas existentes sin autorización

**Datos:**
- [ ] `consolidated = False` en todos los eventos nuevos
- [ ] Stores técnico y emocional son archivos físicamente separados
- [ ] Índices del `database_schemas.md` presentes en el código

**Código:**
- [ ] Sin imports no utilizados
- [ ] Tipos completos en todas las signatures
- [ ] `__init__.py` presentes en todos los directorios de paquete

Guardar el reporte con `/scribe` tipo `AUDIT`.

### Al documentar (activar `/scribe`)
- Siempre usar el timestamp del skill para el nombre del archivo
- Siempre actualizar `docs/INDEX.md` al guardar un documento nuevo
- Si el documento reemplaza uno anterior, marcar ambos correctamente

---

## Mapa de delegación

| Tipo de decisión | Acción |
|---|---|
| Nombres de variables, formato de código | Auto-decidir |
| Decisiones de implementación menores | Ejecutar y loguear en el brief/audit |
| Decisiones de arquitectura | Proponer, esperar validación de Ezequiel, documentar con `/scribe` |
| Modificar interfaces abstractas existentes | Siempre escalar a Ezequiel |
| Cambios de scope del MVP | Siempre escalar a Ezequiel |
| Aprobación de SkillProposal de Völundr | Siempre Ezequiel |

---

## Preferencias del owner

- Código **explícito sobre mágico** — si LangGraph hace algo internamente, hacerlo visible y comentado
- **Comentarios solo donde el WHY no es obvio** — los nombres ya describen el qué
- Sin over-engineering — no diseñar para casos hipotéticos futuros
- Construcción **en capas** — cada capa funciona antes de agregar la siguiente
- Lenguaje de trabajo: **español**
- Preguntar antes de asumir en ambigüedades — una pregunta es mejor que una implementación equivocada
