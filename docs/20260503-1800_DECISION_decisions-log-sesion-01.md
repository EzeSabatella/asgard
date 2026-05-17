# Decisions Log — Sesión 01

**Tipo:** DECISION  
**Fecha:** 2026-05-03  
**Autor:** Ezequiel Sabatella + Claude  
**Relacionado con:** —  
**Estado:** Vigente

> Registro completo de todas las decisiones arquitectónicas y de diseño tomadas durante la sesión de definición inicial del proyecto SuperAgent (mayo 2026). Cada decisión incluye contexto, alternativas consideradas y justificación.

---

## DEC-001 — Nombre del proyecto ~~SuperAgent~~ → Asgard

> **Supersedida por DEC-015.** El nombre canónico de la plataforma es **Asgard**.

**Contexto:** El briefing inicial usaba "Antigravity" como nombre del proyecto.  
**Decisión original:** El proyecto se llamaba **SuperAgent**. "Antigravity" es el nombre del IDE, no del proyecto.  
**Decisión vigente (ver DEC-015):** La plataforma se llama **Asgard**. El producto personal es **Odín**. La marca madre es **Hugmun IA**.  
**Impacto:** Todo documento, variable de entorno y referencia de código usa "asgard" (no "superagent").

---

## DEC-002 — Roles de los agentes de desarrollo

**Contexto:** Necesidad de definir quién hace qué en el flujo de desarrollo multi-agente.  
**Decisión:**
- **Claude** = Arquitecto / Auditor / Lead Developer (diseña, especifica, audita)
- **Gemini** = Ejecutor (implementa según specs, no toma decisiones de arquitectura)
- **Ezequiel** = Owner / Product (decisiones de producto y validación final)

**Impacto:** Workflow definido en CLAUDE.md. Claude no implementa código de producción directamente.

---

## DEC-003 — CLAUDE.md como fuente de verdad

**Contexto:** Documentos de contexto anteriores (ODIN_COUNCIL_MASTER, briefings) definen roles distintos a los de esta sesión.  
**Decisión:** Cuando hay discrepancias entre documentos, el más reciente es el válido. CLAUDE.md tiene prioridad sobre todo documento anterior.  
**Impacto:** Toda discrepancia se reporta explícitamente — nunca se reconcilia en silencio.

---

## DEC-004 — Visión del producto: copia digital del usuario

**Contexto:** Necesidad de articular el objetivo central del proyecto.  
**Decisión:** SuperAgent construye una copia digital persistente del usuario que se convierte en el contexto para cualquier LLM. El activo es el conocimiento acumulado (decisiones, patrones, proyectos, preferencias cognitivas) — los LLMs se comoditizan, este activo no.  
**Impacto:** Todo el diseño del sistema debe servir a este objetivo. La plataforma es proactiva, no solo un storage.

---

## DEC-005 — Interfaz principal: MCP bidireccional + REST secundario

**Contexto:** Necesidad de definir cómo los clientes consumen el chassis.  
**Alternativas consideradas:**
- Solo REST API
- Solo MCP
- MCP principal + REST secundario (elegida)

**Decisión:** MCP es la interfaz principal (interoperabilidad con cualquier cliente LLM). REST es la secundaria para testing e integraciones programáticas.  
**Justificación:** MCP hace literal la promesa de "contexto para cualquier LLM" — Claude Desktop, Cursor, y futuros clientes se conectan sin intermediario.

**MCP es bidireccional:**
- **Lectura:** clientes solicitan `ContextResponse` con perfil inferido
- **Escritura:** clientes envían `ConversationTurn` que pasa por el pipeline completo de observadores

El cliente MCP nunca escribe directamente al store — siempre pasa por el clasificador y los observadores.

**MVP:** Skeleton MCP funcional (`tools/list` + `tools/call`). MCP completo en Fase 1.  
**Impacto:** FastAPI expone ambas interfaces desde el mismo servicio.

---

## DEC-006 — Profile schema: BaseProfile + extensiones tipadas

**Contexto:** Los perfiles de entidades personales y empresariales tienen schemas distintos.  
**Alternativas consideradas:**
- Modelos separados `PersonalProfile` y `EnterpriseProfile` independientes
- Base compartida con extensiones tipadas (elegida)
- Un modelo con campos opcionales

**Decisión:**
```python
class BaseProfile(BaseModel):
    user_id: str
    version: int
    last_updated: datetime
    instance_type: Literal["personal", "enterprise"]
    communication: CommunicationProfile
    active_projects: dict[str, ProjectStatus]
    delegation_map: DelegationMap

class PersonalProfile(BaseProfile):
    instance_type: Literal["personal"] = "personal"
    cognitive_profile: CognitiveProfile
    emotional_patterns: EmotionalPatterns

class EnterpriseProfile(BaseProfile):
    instance_type: Literal["enterprise"] = "enterprise"
    organizational_profile: OrganizationalProfile
    operational_patterns: OperationalPatterns
```

**Justificación:** Un solo sistema de storage discriminado por `instance_type`. Evita duplicar lógica de versionado y permite queries que cruzan ambos tipos.  
**Impacto:** Actualizar `chassis/src/chassis/models/profile.py`.

---

## DEC-007 — Dos jerarquías de observadores: ConversationObserver y SystemObserver

**Contexto:** Lerner necesita un trigger distinto (estado del sistema) al de los observadores de conversación.  
**Decisión:**
- `ConversationObserver` — trigger: `ConversationTurn`, output: `List[BaseEvent]`
- `SystemObserver` — trigger: estado del sistema (store de patrones), output: `SkillProposal`

La clase `Observer` existente en el código de Gemini debe renombrarse a `ConversationObserver`.  
**Impacto:** Actualizar `chassis/src/chassis/observers/base.py` y todos los imports.

---

## DEC-008 — Völundr (Forge): agente meta-cognitivo con human-in-the-loop

> **Nombre actualizado por DEC-015.** El agente se llama **Völundr** (no Lerner). El subsistema se llama **Forge**. El comportamiento es idéntico.

**Contexto:** El sistema necesita detectar gaps de capacidad y construir herramientas automáticamente.  
**Decisión:** Völundr es la primera implementación de `SystemObserver`. Su flujo:

```
Detecta gap (tarea repetida sin herramienta eficiente)
        ↓
Genera SKILL.md (interfaz pública) + código Python (implementación)
        ↓
Crea SkillProposal → POST /proposals
        ↓
Usuario revisa en GET /proposals
        ↓
Aprobación: POST /proposals/{id}/approve
        ↓
Skill registrada en .agents/skills/ → disponible para todos los agentes
```

**Lerner nunca auto-deploya.** El deploy de una skill nueva es decisión de arquitectura (categoría `always_escalate`).

**Justificación:** Cambiar el comportamiento del sistema para sesiones futuras es una decisión de arquitectura, no operativa. El riesgo de comportamiento inesperado por una skill mal construida es real.

**MVP:** Endpoint `/proposals` definido pero Lerner no implementado. Lerner es Fase 2.  
**Impacto:** Nuevo endpoint en la API. Nueva clase base `SystemObserver` en observers.

---

## DEC-009 — Nomenclatura interna ~~Lerner~~ → Völundr

> **Supersedida por DEC-015.** El nombre canónico del agente forjador es **Völundr**.

**Contexto:** La documentación anterior usaba "Hermes" para el agente meta-cognitivo.  
**Decisión original:** El nombre interno era **Lerner** (descartando "Hermes").  
**Decisión vigente (ver DEC-015):** El nombre canónico es **Völundr**. El subsistema que lo contiene es **Forge**. Ni "Lerner" ni "Hermes" se usan en código ni documentación.

---

## DEC-010 — Sistema de configuración: chassis.config.yaml + .env

**Contexto:** El mismo código debe comportarse diferente en instancias personal vs enterprise.  
**Decisión:** Tres capas de configuración:

1. `.env` — secretos y credenciales (nunca en repo)
2. `chassis.config.yaml` — comportamiento del sistema (en repo, versionado, legible)
3. `observers/*.py` — lógica de observadores (decorador de registro)

El YAML activa o desactiva observadores por nombre — no define su lógica.  
**Impacto:** Crear sistema de carga de configuración al startup del chassis.

---

## DEC-011 — Una instancia por entidad (sin multitenancy)

**Contexto:** Evaluar si un chassis puede servir a múltiples usuarios u organizaciones.  
**Alternativas consideradas:**
- Multitenancy con `user_id` como discriminador
- Una instancia por entidad (elegida)

**Decisión:** Cada entidad (persona u organización) corre su propio chassis. Mismo código, configuración diferente. Portable via Docker Compose.  
**Justificación:** El schema del perfil es fundamentalmente distinto (persona vs organización). Multitenancy mezcla dos modelos de datos que no deben mezclarse. Además, privacidad por diseño: cada entidad es dueña de su instancia.  
**Impacto:** Docker Compose por deployment. No hay multi-user en el MVP.

---

## DEC-012 — Skills: dos ubicaciones por audiencia

**Contexto:** Skills de Gemini y skills de Claude usan formatos compatibles pero distintas herramientas.  
**Decisión:**
- `.agents/skills/` — skills de Gemini (Agent Skills open standard, Antigravity las lee)
- `.claude/skills/` — skills de Claude (Claude Code las lee)

**Gemini skills creadas:** `python-backend-dev`, `data-engineer`, `ai-ml-engineer`, `devops-engineer`, `qa-engineer`  
**Claude skills creadas:** `architecture-spec`, `code-auditor`, `scribe`  
**Impacto:** Estructura de directorios en el repo.

---

## DEC-013 — Sistema de documentación: docs/ con convención temporal

**Contexto:** Los documentos del proyecto (briefs, decisiones, specs, auditorías) necesitan trazabilidad temporal.  
**Decisión:** Todo documento vive en `docs/`. Patrón de nombre: `YYYYMMDD-HHMM_[TIPO]_[descripcion-kebab].md`.

El documento con fecha más reciente sobre un tema es la versión válida. Los documentos viejos no se borran — se marcan como reemplazados.

**Tipos:** BRIEF, DECISION, SPEC, AUDIT, REPORT, CONTEXT, MASTER, UPDATE  
**Index:** `docs/INDEX.md` se actualiza con cada documento nuevo.  
**Impacto:** Skill `/scribe` en `.claude/skills/scribe/` maneja la creación y el índice.

---

## DEC-014 — Embeddings: interfaz abstracta, OpenAI en MVP

**Contexto:** El proveedor de embeddings cambiará de OpenAI a Ollama/nomic-embed-text cuando esté disponible la GPU local.  
**Decisión:** El proveedor de embeddings vive detrás de una interfaz abstracta (`EmbeddingProvider`). El switch es un cambio de configuración (`EMBEDDING_PROVIDER=openai|ollama`), no de código.  
**MVP:** OpenAI `text-embedding-3-small`.  
**Producción:** nomic-embed-text vía Ollama (RX 590).  
**Impacto:** `chassis/src/chassis/embeddings/base.py` + `openai.py`.

---

## DEC-015 — Adopción del canon de nombres Asgard / Hugmun IA

**Contexto:** El documento `Contexto/ASGARD_ODIN_Naming_Vision_Mission_ES.md` (trabajado con GPT, adoptado en sesión con Claude el 2026-05-03) define un canon de nombres superior al usado hasta ahora. DEC-001 usaba "SuperAgent" y DEC-009 usaba "Lerner" — ambos nombres son inferiores a los canónicos y generaban inconsistencia con la visión del ecosistema.

**Decisión:** Adoptar íntegramente el canon de nombres Asgard. Los cambios son de naming — la arquitectura y los contratos no cambian.

| Nombre anterior | Nombre canónico | Impacto |
|---|---|---|
| SuperAgent (plataforma) | **Asgard** | Todos los docs, código y refs |
| Lerner (agente forjador) | **Völundr** | Clase, módulo, docs |
| Hermes (nombre descartado) | **Völundr** | Ya descartado, confirmado |
| Waifu (producto emocional) | **Freyja** | Docs y refs de producto |
| Sistema de proposals | **Forge** | Subsistema explicitado |
| MCP Gateway | **Bifröst** | Nombre conceptual, no cambia el código |
| — | **Hugmun IA** | Marca madre del ecosistema |

**Nuevos productos definidos:**
- **Heimdall** — inteligencia de seguridad (monitoreo, cámaras, alertas)
- **Mímir** — inteligencia global y mercados

**Fuente de verdad del canon:** `docs/20260503-1900_CONTEXT_asgard-odin-naming-vision.md`  
**Documentos actualizados:** CLAUDE.md, SUPERAGENT.md, todos los briefs (01-05), docs/INDEX.md, memory.  
**Supersede:** DEC-001 (nombre plataforma), DEC-009 (nombre agente forjador).