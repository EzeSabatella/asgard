# Asgard — Documento Maestro del Proyecto

**Owner:** Ezequiel Sabatella — Buenos Aires, Argentina  
**Fecha:** Mayo 2026  
**Estado:** Arquitectura definida — MVP en implementación  
**Versión:** 1.0

---

## Resumen ejecutivo

Asgard es una plataforma de identidad digital persistente que construye y mantiene una copia digital del usuario, convirtiéndola en el contexto que cualquier modelo de lenguaje recibe antes de responder.

Los LLMs se comoditizan. Cada seis meses hay uno mejor y más barato. Lo que no se comoditiza es el conocimiento acumulado sobre el usuario: sus decisiones, patrones cognitivos, proyectos activos, estilo de comunicación, preferencias técnicas. Ese activo es personal, crece con el tiempo, y no puede replicarse.

Asgard es la infraestructura que construye ese activo y lo hace accesible a cualquier agente, herramienta o modelo — hoy y en el futuro.

---

## El problema

Cada vez que un usuario abre una nueva conversación con un LLM, empieza de cero. El modelo no sabe quién es, qué está construyendo, qué decisiones tomó la semana pasada, cómo piensa, ni cómo prefiere que le hablen. El usuario repite contexto. El modelo responde sin historia. El trabajo es menos efectivo de lo que podría ser.

Esto no se resuelve con ventanas de contexto más grandes. Se resuelve repensando cómo se representa, comprime y activa la memoria del usuario — tomando como inspiración los mecanismos del cerebro humano.

> Lo que debe persistir no son los hechos de una conversación sino los rasgos que esa conversación reveló sobre el usuario — su estilo cognitivo, preferencias, dominio, objetivos activos. No se hereda el evento; se hereda la configuración que el evento produjo.

---

## La solución

Asgard observa cada interacción, extrae los rasgos estructurales relevantes, los consolida en un perfil inferido del usuario, y expone ese perfil como contexto para cualquier LLM a través de una interfaz estándar (MCP).

El sistema no es pasivo. Cuando el usuario encara un proyecto nuevo, la plataforma le permite al LLM entender que las primeras fases son similares a proyectos anteriores. El LLM toma ese contexto, lo adapta y lo deja listo. El mismo trabajo que tomaba horas de setup inicial se resuelve en segundos.

La plataforma también es meta-cognitiva: detecta cuándo una tarea se repite sin tener una herramienta eficiente para resolverla, diseña esa herramienta, y la propone al usuario para su aprobación.

---

## Arquitectura del sistema

### Flujo completo

```
Cliente (Claude Desktop, Cursor, Odín, Freyja, Nexus, cualquier MCP client)
        │
        │  MCP (primario) / REST (secundario)
        ▼
┌───────────────────────────────────────────┐
│              FastAPI Chassis              │
│                                           │
│  MCP: tools/list  tools/call             │
│  REST: /events  /context  /profile       │
│         /consolidate  /proposals  /health │
└──────────────────┬────────────────────────┘
                   │
          chassis.config.yaml
          (observadores activos, agresividad,
           embeddings, schedule, tipo de instancia)
                   │
       ┌───────────▼───────────┐
       │    Clasificador       │
       │  (portero de estímulo)│
       │  decide qué observers │
       │  se activan           │
       └───────────┬───────────┘
                   │  activa N observers en paralelo
       ┌───────────▼───────────┐
       │   Observer Registry   │
       │                       │
       │  ConversationObserver │  ← trigger: ConversationTurn
       │  • Technical          │
       │  • Empathic           │
       │  • Humor              │
       │  • Social             │
       │                       │
       │  SystemObserver       │  ← trigger: estado del sistema
       │  • Völundr             │  ← detecta gaps de capacidad
       └───────────┬───────────┘
                   │ produce eventos tipados
       ┌───────────▼───────────┐
       │      Store Bruto      │
       │  raw_technical.db     │  (SQLite + SQLCipher)
       │  raw_emotional.db     │  (SQLite + SQLCipher)
       └───────────┬───────────┘
                   │  cron (configurable) / trigger manual
       ┌───────────▼───────────┐
       │     Consolidador      │  (agente offline)
       └────────┬──────────────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
 Store       Store de    Grafo de
Inferido     Patrones   Conocimiento
(ChromaDB)  (SQLite)    (Neo4j)
    │           │           │
    └─────┬─────┘           │
          │                 │
    ContextResponse ←───────┘
    (entregado al cliente)
```

### Völundr — El agente meta-cognitivo

```
Völundr (SystemObserver)
        │
        │  observa store de patrones
        │  detecta tarea repetida sin herramienta eficiente
        ▼
  genera SkillProposal
  ├── SKILL.md        ← interfaz pública (qué hace, cuándo se activa)
  └── código Python   ← implementación ejecutable
        │
        ▼
  POST /proposals     ← se acumula, espera aprobación
        │
        │  usuario revisa y aprueba
        ▼
  POST /proposals/{id}/approve
        │
        ▼
  skill registrado en catálogo
  disponible para todos los agentes
```

Völundr nunca auto-deploya. El deploy de una skill nueva es una decisión de arquitectura — siempre pasa por el usuario.

---

## Componentes del sistema

### ConversationObserver (base class)
Trigger: `ConversationTurn`  
Output: `List[BaseEvent]`  
Implementaciones: Technical, Empathic, Humor, Social

Cada observador tiene:
- **Criterio de relevancia propio** — `is_relevant(turn)` decide si hay información para capturar
- **Schema de escritura propio** — el formato del evento que escribe al store bruto
- **Nivel de agresividad propio** — qué tan implícita puede ser la señal para que la capture

| Observador | Qué captura | Agresividad | MVP |
|---|---|---|---|
| Technical | Decisiones, stack, contexto de proyecto | Conservadora (0.3) | ✅ |
| Empathic | Estados emocionales, patrones de soporte | Agresiva (0.7) | Fase 1 |
| Humor | Estilo de humor, triggers, intensidad | Moderada (0.5) | Fase 1 |
| Social | Dinámica relacional, comunicación | Moderada (0.5) | Fase 1 |

### SystemObserver (base class)
Trigger: estado del sistema (store de patrones, catálogo de skills)  
Output: `SkillProposal`  
Implementación: Völundr

### Clasificador de estímulo
Portero del pipeline. Recibe cada `ConversationTurn` y decide qué observadores activar. Puede activar múltiples en paralelo. La co-activación es información en sí misma.

MVP: heurísticas de keywords  
Fase 1: LLM liviano (llama3:8b / DeepSeek Flash local)

### Consolidador
Proceso offline que lee eventos brutos con `consolidated = false`, extrae rasgos, actualiza el perfil inferido, y marca los eventos como procesados. Ningún evento se procesa dos veces.

Schedule: configurable via YAML (default: cron 3am)  
MVP: reglas determinísticas  
Fase 1: LLM para consolidación semántica

---

## Storage: cinco stores, tres tecnologías

| Store | Archivo | Tecnología | Qué guarda | Acceso |
|---|---|---|---|---|
| Bruto técnico | `raw_technical.db` | SQLite + SQLCipher | Eventos técnicos sin consolidar | Escritura en tiempo real |
| Bruto emocional | `raw_emotional.db` | SQLite + SQLCipher | Eventos emocionales sin consolidar | Escritura en tiempo real |
| Inferido | ChromaDB collection | ChromaDB + SQLite | Perfil del usuario + embeddings | Lectura por agentes |
| Patrones | `patterns.db` | SQLite | Correlaciones de co-activación | Consolidador |
| Grafo | Neo4j | Neo4j | Relaciones conceptos/proyectos/decisiones | Lectura/escritura consolidador |

**Regla invariante:** Los stores técnico y emocional son físicamente separados — dos archivos SQLite distintos. La encriptación vive en la capa de storage (SQLCipher), no en la lógica de la aplicación.

---

## API: MCP + REST

### MCP (interfaz principal)

Asgard expone un servidor MCP. Cualquier cliente compatible (Claude Desktop, Cursor, herramientas propias) puede conectarse y consumir el contexto del usuario sin intermediario.

**Bidireccional:**
- **Lectura:** el cliente solicita `ContextResponse` con el perfil inferido
- **Escritura:** el cliente envía `ConversationTurn` → pasa por el pipeline completo de observadores → el chassis decide qué extraer

El cliente MCP nunca escribe directamente al store. Siempre pasa por el clasificador y los observadores.

```
MCP tools expuestos:
  tools/list     ← descubrimiento de capacidades
  tools/call     ← ejecución (mapeado a /mcp/context y /mcp/turn)
```

### REST (interfaz secundaria)

```
POST   /events              ← recibir ConversationTurn
GET    /context/{user_id}   ← obtener ContextResponse
GET    /profile/{user_id}   ← perfil inferido completo
POST   /consolidate         ← trigger manual del consolidador
GET    /patterns/{user_id}  ← patrones de co-activación
GET    /proposals           ← skills pendientes de aprobación (Völundr)
POST   /proposals/{id}/approve ← aprobar y deployar una skill
GET    /health              ← estado del sistema
```

---

## Perfil del usuario: schema

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

Un solo sistema de storage, discriminado por `instance_type`. El consolidador instancia el modelo correcto según la configuración.

---

## Configuración del chassis

Tres capas con responsabilidades distintas:

```
.env                    ← secretos y credenciales (nunca en repo)
chassis.config.yaml     ← comportamiento del sistema (en repo, versionado)
observers/*.py          ← lógica de observadores (decorador de registro)
```

Ejemplo de `chassis.config.yaml`:

```yaml
instance:
  type: personal          # personal | enterprise
  user_id: lexa

observers:
  technical:
    enabled: true
    aggressiveness: conservative
  empathic:
    enabled: true
    aggressiveness: aggressive
  humor:
    enabled: true
    aggressiveness: moderate
  social:
    enabled: false

embeddings:
  provider: openai        # openai | ollama
  model: text-embedding-3-small

consolidation:
  schedule: "0 3 * * *"
  min_events_to_consolidate: 10

mcp:
  enabled: true
  bidirectional: true
```

Para una instancia enterprise (Nexus), el mismo archivo tendría `type: enterprise`, observadores distintos (financiero, operativo), y `bidirectional: false`.

---

## Una instancia por entidad

Cada entidad (persona u organización) corre su propio chassis. No hay multitenancy. El mismo código — configuración diferente.

**Por qué:**
- El schema del perfil inferido es fundamentalmente distinto (persona vs organización)
- Los observadores son distintos
- Los patrones que se buscan son distintos
- La privacidad es por diseño: cada entidad es dueña de su instancia

**Portabilidad:** una empresa puede llevarse su chassis con todos sus datos igual que una persona se lleva el pendrive. Docker Compose por deployment.

---

## El ecosistema de productos

Asgard es la plataforma. Los productos son consumidores distintos del mismo chassis con objetivos distintos.

### Odín — Compañero personal (técnico + bienestar)
Consume el chassis con `instance_type: personal`. Conoce el contexto técnico del usuario, sus proyectos, decisiones pasadas, estilo cognitivo. Y va más allá: detecta patrones de agotamiento, sugiere pausas, celebra logros. Diseñado para que el usuario lo necesite cada vez menos.

### Freyja — Compañero emocional
Consume el mismo chassis personal pero con énfasis en el store emocional. Conoce el estilo de humor del usuario, sus patrones de soporte efectivo, su historia. El objetivo no es productividad — es vínculo y bienestar.

### Nexus — Inteligencia operativa empresarial
Consume el chassis con `instance_type: enterprise`. El "usuario" es la organización: sus patrones operativos, estacionalidad, presupuestos, decisiones pasadas. Planifica, proyecta y presupuesta operaciones. Primer vertical: contact centers.

### Heimdall — Inteligencia de seguridad
Monitoreo de cámaras, detección de eventos visuales, alertas y asistencia operativa. Consume el chassis con `instance_type: enterprise`. Audiencia: equipos de seguridad, edificios, empresas, barrios.

### Mímir — Inteligencia global y mercados
Monitoreo de eventos mundiales, geopolítica, commodities, noticias y mercados. Detecta relaciones causales y genera inteligencia accionable. Consume el chassis con `instance_type: enterprise`. Audiencia: analistas, inversores, traders, investigadores.

---

> La arquitectura está diseñada para que mañana se pueda construir un nuevo producto sobre el chassis sin modificar lo que ya funciona.

---

## Stack técnico

| Componente | Tecnología | Razón |
|---|---|---|
| Lenguaje | Python 3.11+ | Legibilidad, ecosistema ML/AI |
| API de superficie | FastAPI | Async nativo, tipado, MCP + REST desde el mismo servicio |
| Orquestación de agentes | LangGraph | Diseñado para agentes con estado persistente |
| Store relacional | SQLite + SQLCipher | Encriptación en reposo, sin servidor, portable |
| Store vectorial | ChromaDB | Local, sin API externa, simple |
| Store de grafos | Neo4j | Relaciones explícitas, transferencia de conocimiento |
| Embeddings (MVP) | OpenAI text-embedding-3-small | Placeholder hasta tener GPU local |
| Embeddings (producción) | nomic-embed-text vía Ollama | Local, gratuito, RX 590 |
| Containerización | Docker + Docker Compose | Aislamiento, portabilidad, una instancia por entidad |
| Configuración | YAML + variables de entorno | Legible, versionable, separación secretos/comportamiento |
| Protocolo principal | MCP | Interoperabilidad con cualquier cliente LLM |

**Nota sobre embeddings:** el proveedor está detrás de una interfaz abstracta. El switch de OpenAI a Ollama es un cambio de configuración, no de código.

---

## Fases de desarrollo

### Fase 0 — MVP del Chassis (en curso)

**Objetivo:** Un chassis funcional que capture eventos técnicos y exponga contexto básico via REST + MCP skeleton.

| Componente | Estado |
|---|---|
| Estructura del monorepo | ✅ Completado |
| Schemas Pydantic (BaseProfile + extensiones) | 🔄 Requiere actualización |
| Store bruto SQLite técnico | ⏳ Pendiente |
| ConversationObserver base + TechnicalObserver | ✅ Completado |
| Clasificador heurístico | ⏳ Pendiente |
| ChromaDB + interfaz de embeddings OpenAI | ⏳ Pendiente |
| FastAPI endpoints REST | ⏳ Pendiente |
| MCP skeleton (tools/list + tools/call) | ⏳ Pendiente |
| chassis.config.yaml + carga de configuración | ⏳ Pendiente |
| Docker Compose | ✅ Completado (parcial) |
| Tests básicos del observer técnico | ⏳ Pendiente |

### Fase 1 — Inteligencia completa del chassis

- Observadores emocionales (Empathic, Humor, Social)
- Clasificador LLM liviano (reemplaza heurísticas)
- Consolidador con LLM para consolidación semántica
- Detector de patrones de co-activación
- Neo4j alimentado con decisiones y conceptos
- MCP completo (bidireccional)

### Fase 2 — Forge / Völundr

- `SystemObserver` base class
- Völundr: detección de gaps, generación de `SkillProposal`
- Endpoint `/proposals` con flujo de aprobación humana
- Pipeline de deployment de skills aprobadas
- Forge: catálogo versionado de skills del chassis (`.agents/skills/`)

### Fase 3 — Productos de superficie

- Odín MVP: agente técnico + bienestar sobre el chassis
- Nexus MVP: inteligencia operativa para contact centers
- Freyja: store emocional completo

### Fase 4 — Escala y enterprise

- `EnterpriseProfile` completo con `OrganizationalProfile` y `OperationalPatterns`
- Observadores enterprise (Financial, Operational)
- Multi-instancia management
- Nexus full implementation

---

## Principios de diseño (invariantes)

**Open/Closed:** Abierto para extensión, cerrado para modificación. Cada nueva capa se agrega sin tocar lo que ya funciona. Los observadores se registran en un catálogo; las interfaces abstractas no se modifican sin aprobación explícita.

**Privacy by design:** Una instancia por entidad. Los datos nunca salen de la infraestructura del dueño. Encriptación en reposo (SQLCipher). Sin logs de contenido en claro.

**Human-in-the-loop:** Las decisiones que cambian el comportamiento del sistema para sesiones futuras siempre pasan por el usuario. Völundr propone — nunca auto-deploya. Los handoffs manuales son una feature, no una limitación.

**LLM-agnostic:** MCP como interfaz principal hace que Asgard funcione con cualquier modelo. El chassis no sabe ni le importa qué LLM consume su contexto.

**Explícito sobre mágico:** El código es legible. Si LangGraph hace algo internamente, se documenta y se hace visible. Los nombres describen el qué; los comentarios explican el porqué cuando no es obvio.

**Construcción en capas:** Cada capa funciona antes de agregar la siguiente. No volar demasiado alto demasiado rápido.

---

## Workflow de desarrollo

```
Ezequiel define el objetivo
        ↓
Claude diseña: spec, contratos, interfaces, decisiones de arquitectura
        ↓
Gemini ejecuta: implementa según la spec
        ↓
Claude audita: verifica correctitud, seguridad, alineación arquitectónica
        ↓
Ezequiel valida
        ↓
Capa completa → siguiente spec
```

**Herramientas:**
- IDE: Antigravity (Gemini nativo + extensión Claude)
- Skills de Gemini: `.agents/skills/` (python-backend-dev, data-engineer, ai-ml-engineer, devops-engineer, qa-engineer)
- Skills de Claude: `.claude/skills/` (architecture-spec, code-auditor)
- Fuente de verdad de roles y workflow: `CLAUDE.md`

---

## Glosario mínimo

| Término | Definición |
|---|---|
| **Chassis** | La infraestructura de memoria persistente. El producto central de Asgard. |
| **ConversationObserver** | Agente que procesa turnos de conversación y extrae eventos tipados. |
| **SystemObserver** | Agente que observa el estado del sistema y detecta gaps de capacidad. |
| **Hugmun IA** | Marca madre del ecosistema. Laboratorio, marca y futura empresa que contiene todo. |
| **Völundr** | Implementación concreta de SystemObserver. Detecta gaps y forja nuevas skills. |
| **Forge** | Subsistema de creación, revisión, aprobación y versionado de skills del chassis. |
| **Bifröst** | Nombre conceptual del MCP Gateway — puente entre Asgard y clientes externos. |
| **Store bruto** | Storage de eventos sin procesar (raw). Entrada del pipeline. |
| **Store inferido** | Perfil del usuario construido por el consolidador. Salida del pipeline. |
| **Consolidador** | Proceso offline que transforma eventos brutos en perfil inferido. |
| **SkillProposal** | Output de Völundr: SKILL.md + código Python + metadata de la skill propuesta. |
| **instance_type** | Discriminador del perfil: `personal` (Odín, Freyja) o `enterprise` (Nexus). |
| **MCP** | Model Context Protocol. Interfaz principal del chassis con clientes externos. |
| **Antigravity** | El IDE utilizado para el desarrollo (Gemini + extensión Claude). No es el nombre del proyecto. |

---

*Documento vivo — se actualiza con cada decisión arquitectónica relevante.*  
*Última actualización: Mayo 2026*
