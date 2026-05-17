# ANTIGRAVITY — Briefing para Claude Code
## Contexto completo del proyecto para iniciar implementación

**Fecha:** Mayo 2026 | **Owner:** Ezequiel Sabatella  
**Stack principal:** Python + FastAPI + LangGraph + SQLite + ChromaDB + Neo4j  
**Repo:** monorepo `/antigravity`

---

## 1. Qué es este proyecto

Antigravity es una **plataforma de identidad digital persistente y portable**. Su componente central es un chasis de memoria que aprende quién es el usuario — su estilo cognitivo, patrones emocionales, decisiones pasadas, proyectos activos — y lo hace accesible a múltiples agentes especializados.

El chasis no es un producto en sí mismo. Es la infraestructura que potencia productos:

- **Odín** — compañero profesional/técnico con memoria persistente
- **Waifu** — compañero emocional/social con memoria persistente  
- **Nexus** — sistema de forecasting operativo (perfil de negocio cliente)

La analogía correcta: **los LLMs son el motor, el chasis es todo lo demás**. El motor es intercambiable; el chasis es el activo que crece con el tiempo.

> Lo que debe persistir no son los hechos de una conversación sino los rasgos que esa conversación reveló sobre el usuario — su estilo cognitivo, preferencias, dominio, objetivos activos. Es el equivalente funcional de la epigenética: no se hereda el evento, se hereda la configuración que el evento produjo.

---

## 2. Principio arquitectónico fundamental

**El chasis es extensible por diseño desde el día 1.**

Open/Closed Principle aplicado: abierto para extensión, cerrado para modificación. Cada nueva capa de funcionalidad se agrega sin tocar lo que ya funciona. Esto no es una intención futura — es un requisito de diseño que debe reflejarse en la estructura del código desde el inicio.

Implicaciones concretas:
- Los observadores se registran en un catálogo, no se hardcodean
- Los stores tienen interfaces abstractas, no se acceden directamente
- La API expone contratos estables aunque el internals cambie
- El grafo de conocimiento (Neo4j) empieza vacío pero su schema está definido desde el inicio

---

## 3. Arquitectura del chasis

### 3.1 Flujo completo

```
Turno de conversación
        ↓
   Clasificador de estímulo
   (decide qué observadores se activan)
        ↓
   ┌─────────┬──────────┬──────────┬─────┐
   ↓         ↓          ↓          ↓     ↓
 Obs.      Obs.      Obs.       Obs.   ...N
 Técnico   Humor     Empático   Social
   ↓         ↓          ↓          ↓
   └─────────┴──────────┴──────────┘
                    ↓
            Store bruto
            (técnico + emocional)
                    ↓
         Agente consolidador (proceso offline)
                    ↓
         ┌──────────┴──────────┐
         ↓                     ↓
   Store inferido        Store de patrones
   (modelo usuario)      (co-activaciones)
         ↓                     ↓
         └──────────┬──────────┘
                    ↓
        Agentes de superficie
        (Odín, Waifu, Nexus)
                    ↓
         API única (FastAPI)
```

### 3.2 Observadores especializados

Cada observador tiene:
- **Criterio de relevancia propio** — qué constituye información nueva para su dominio
- **Schema de escritura propio** — el formato del evento que escribe al store bruto
- **Nivel de agresividad propio** — qué tan implícita puede ser la señal para que la capture

| Observador | Qué captura | Agresividad |
|---|---|---|
| Técnico | Decisiones, stack, contexto de proyecto | Conservadora |
| Humor | Estilo de humor, triggers, intensidad | Moderada |
| Empático | Estados emocionales, patrones de soporte | Agresiva |
| Social | Dinámica relacional, comunicación | Moderada |
| Hermes (futuro) | Gaps de capacidad del sistema | Moderada |

**El clasificador puede activar múltiples observadores simultáneamente.** La co-activación es información valiosa en sí misma.

### 3.3 El detector de patrones de co-activación

No guarda eventos — guarda **correlaciones temporales entre observadores**. Es el componente más diferenciador del sistema.

Ejemplo: si Humor + Empático se co-activan en 8 de 11 sesiones, y en una sesión aparece Humor solo sin trigger obvio de comedia → el sistema infiere estado emocional negativo y actúa en consecuencia.

### 3.4 Grafo de conocimiento (Neo4j)

Captura **transferencia de conocimiento entre contextos**. No solo qué sabe el usuario sino cómo se conecta lo que sabe. Qué conceptos son isomorfos entre proyectos. Qué soluciones ya resolvió que reaparecen con distinto nombre.

Ejemplo de uso: "Lo que estás construyendo en Waifu es isomorfo a lo que construiste en Nexus en esta parte. Si cambiás esto nada más, queda adaptado."

---

## 4. Storage: tres stores, tres tecnologías

| Store | Tecnología | Qué guarda |
|---|---|---|
| Bruto técnico | SQLite + SQLCipher | Eventos tipados técnicos |
| Bruto emocional | SQLite + SQLCipher | Eventos tipados emocionales |
| Inferido | SQLite + ChromaDB | Perfil del usuario + embeddings |
| Patrones | SQLite | Correlaciones de co-activación |
| Grafo de conocimiento | Neo4j | Relaciones entre conceptos/proyectos/decisiones |

### Schema de evento técnico

```json
{
  "id": "ev_0042",
  "ts": "2026-05-01T14:23:00",
  "type": "DECISION",
  "project": "odin",
  "tags": ["hardware", "infra"],
  "content": "Ubuntu Server sobre Windows en PC gamer",
  "rationale": "fricción operativa Docker/ROCm",
  "source": "conversation",
  "consolidated": false
}
```

Tipos técnicos: `DECISION`, `PREFERENCE`, `INSIGHT`, `PROJECT_UPDATE`, `BLOCKER`, `MILESTONE`

### Schema de evento emocional

```json
{
  "id": "em_0017",
  "ts": "2026-05-01T15:40:00",
  "type": "EMOTIONAL_SIGNAL",
  "signal": "entusiasmo",
  "trigger": "hablar de arquitectura de agentes",
  "intensity": 0.8,
  "context": "planificación de proyectos propios",
  "consolidated": false
}
```

Tipos emocionales: `EMOTIONAL_SIGNAL`, `RELATIONAL_PATTERN`, `SUPPORT_OUTCOME`, `HUMOR_SIGNAL`, `BOND_REINFORCEMENT`

El campo `consolidated: false` es crítico. El agente consolidador lo marca `true` al procesarlo. Garantiza que ningún evento se procese dos veces.

### Schema del perfil inferido

```json
{
  "user_id": "lexa",
  "version": 12,
  "last_updated": "2026-05-01T14:23:00",
  "cognitive_profile": {
    "learning_style": "conceptual_then_practical",
    "decision_making": "pragmatic_over_ideological",
    "prefers_analogies": true,
    "domain_expertise": {
      "forecasting": 0.85,
      "ml_engineering": 0.70,
      "agent_systems": 0.40
    }
  },
  "communication": {
    "tone_preferred": "informal_direct",
    "humor_style": ["sarcasmo", "referencias_culturales"],
    "responds_well_to": "validacion_antes_de_correccion",
    "language": "es"
  },
  "active_projects": {
    "nexus": {"status": "production", "priority": 1},
    "odin": {"status": "building", "priority": 2},
    "chassis": {"status": "design", "priority": 3}
  },
  "emotional_patterns": {
    "humor_as_defense": {"confidence": 0.73, "calibrated_actions": ["check_emotional_state"]},
    "energy_peak": "morning_sessions",
    "support_style_effective": "escucha_activa_antes_de_soluciones"
  },
  "delegation_map": {
    "auto_execute": ["documentacion", "refactoring_menor", "kickoff_docs"],
    "execute_with_log": ["decisiones_de_implementacion_menores"],
    "recommend_only": ["decisiones_de_arquitectura"],
    "always_escalate": ["decisiones_de_producto", "comunicacion_externa"]
  },
  "decisions_log_refs": ["ev_0001", "ev_0012", "ev_0042"],
  "episodic_refs": ["ep_001", "ep_004"]
}
```

---

## 5. Stack técnico — decisiones tomadas

| Componente | Tecnología | Razón |
|---|---|---|
| Lenguaje | Python 3.11+ | Legibilidad, ecosistema ML/AI |
| API de superficie | FastAPI | Async nativo, tipado, estándar |
| Orquestación de agentes | LangGraph | Diseñado para agentes con estado persistente |
| Store relacional | SQLite + SQLCipher | Encriptación en reposo, sin servidor |
| Store vectorial | ChromaDB | Local, sin API externa, simple |
| Store de grafos | Neo4j | Relaciones explícitas, transferencia de conocimiento |
| Embeddings (MVP) | OpenAI text-embedding-3-small | Placeholder hasta tener Ollama local |
| Embeddings (producción) | nomic-embed-text vía Ollama | Local, gratuito, RX 590 |
| Containerización | Docker + Docker Compose | Aislamiento, reproducibilidad |

**Nota sobre embeddings:** el código debe abstraer el proveedor de embeddings detrás de una interfaz. El switch de OpenAI a Ollama debe ser un cambio de configuración, no de código.

---

## 6. Estructura del monorepo

```
/antigravity
├── README.md
├── docker-compose.yml
├── .env.example
│
├── /chassis                    ← producto independiente
│   ├── README.md
│   ├── pyproject.toml
│   ├── /src
│   │   └── /chassis
│   │       ├── __init__.py
│   │       ├── /api            ← FastAPI, endpoints únicos
│   │       ├── /observers      ← observadores especializados
│   │       │   ├── base.py     ← clase abstracta Observer
│   │       │   ├── technical.py
│   │       │   ├── empathic.py
│   │       │   └── registry.py ← catálogo de observadores
│   │       ├── /classifier     ← clasificador de estímulo
│   │       ├── /consolidator   ← agente consolidador offline
│   │       ├── /stores
│   │       │   ├── base.py     ← interfaces abstractas
│   │       │   ├── raw.py      ← SQLite store bruto
│   │       │   ├── inferred.py ← ChromaDB + SQLite
│   │       │   ├── patterns.py ← SQLite patrones
│   │       │   └── knowledge.py← Neo4j grafo
│   │       ├── /embeddings
│   │       │   ├── base.py     ← interfaz abstracta
│   │       │   ├── openai.py   ← proveedor OpenAI
│   │       │   └── ollama.py   ← proveedor Ollama (futuro)
│   │       └── /models         ← schemas Pydantic
│   └── /tests
│
├── /odin                       ← producto superficie
│   ├── README.md
│   ├── pyproject.toml
│   └── /src
│       └── /odin
│           ├── /agents         ← agentes de superficie Odín
│           ├── /tools          ← herramientas disponibles
│           └── /api            ← API propia de Odín
│
├── /waifu                      ← producto superficie
│   └── (misma estructura que odin)
│
├── /nexus                      ← producto superficie
│   └── (misma estructura que odin)
│
└── /shared                     ← utilidades comunes
    └── /src
        └── /shared
            ├── /config         ← configuración centralizada
            ├── /logging        ← logging estructurado
            └── /types          ← tipos compartidos
```

---

## 7. Contratos de la API (FastAPI)

La API del chasis es **única y opaca** para los productos de superficie. Odín no sabe si está hablando con ChromaDB o Neo4j — solo pide contexto y lo recibe.

### Endpoints principales (MVP)

```
POST   /events              ← recibir turno de conversación
GET    /context/{user_id}   ← obtener contexto relevante para prompt
GET    /profile/{user_id}   ← perfil inferido completo
POST   /consolidate         ← trigger manual del consolidador (para testing)
GET    /patterns/{user_id}  ← patrones de co-activación detectados
GET    /health              ← estado del sistema
```

### Contrato de entrada (evento)

```python
class ConversationTurn(BaseModel):
    user_id: str
    session_id: str
    turn_id: str
    timestamp: datetime
    role: Literal["user", "assistant"]
    content: str
    metadata: dict = {}
```

### Contrato de salida (contexto para prompt)

```python
class ContextResponse(BaseModel):
    user_id: str
    profile_summary: str        # texto comprimido para inyectar en prompt
    relevant_memories: list[Memory]
    active_patterns: list[Pattern]
    delegation_hints: dict      # qué puede hacer autónomamente en esta sesión
```

---

## 8. Decisiones de implementación para el MVP

### Qué entra en el MVP

- [ ] Setup del monorepo con estructura completa de carpetas
- [ ] Schema de base de datos SQLite (store bruto técnico)
- [ ] Schema Neo4j (vacío pero definido)
- [ ] Interfaz abstracta de Observer + registro
- [ ] Observador técnico (el más simple, el primero)
- [ ] Clasificador de estímulo básico (heurísticas, sin LLM)
- [ ] FastAPI con los endpoints principales
- [ ] Interfaz abstracta de embeddings + implementación OpenAI
- [ ] ChromaDB setup básico
- [ ] Docker Compose con todos los servicios
- [ ] Tests básicos del observador técnico

### Qué NO entra en el MVP

- Observadores emocionales (Humor, Empático, Social)
- Agente consolidador con LLM (el MVP consolida con reglas)
- Detector de patrones de co-activación
- Neo4j alimentado (schema sí, datos no)
- Integración con Odín, Waifu, Nexus
- Implementación Ollama de embeddings
- Piloto automático y mapa de delegación

### Orden de implementación sugerido

1. Setup monorepo + Docker Compose
2. Schemas Pydantic (modelos de datos)
3. Store bruto SQLite
4. Interfaz Observer + Observador técnico
5. Clasificador heurístico
6. ChromaDB + interfaz embeddings OpenAI
7. FastAPI endpoints
8. Tests

---

## 9. Consideraciones de seguridad

- SQLite con SQLCipher — encriptación en reposo, clave por variable de entorno
- Sin datos en claro en logs — el contenido de los eventos se loguea hasheado
- Neo4j con autenticación habilitada desde el inicio
- Variables de entorno para todas las credenciales — nunca hardcodeadas
- El store emocional y técnico están físicamente separados (dos archivos SQLite distintos)

---

## 10. Contexto del owner (para decisiones de diseño)

- **Nombre:** Ezequiel Sabatella, Buenos Aires
- **Nivel técnico:** Python legible pero no experto. Entiende arquitectura conceptualmente. Prefiere código explícito sobre magia de frameworks.
- **Objetivo de aprendizaje paralelo:** está implementando LangGraph en el proyecto pero construyendo los agentes a mano en paralelo para entender qué hace el framework. No simplificar el código para ocultar LangGraph — al contrario, hacerlo visible y comentado.
- **Preferencia de código:** comentarios explicativos en decisiones no obvias. Nombres de variables descriptivos. Sin over-engineering.
- **Hardware pendiente:** PC gamer con GPU AMD RX 590 en setup. Por ahora todo corre en máquina de desarrollo sin GPU. Embeddings usan OpenAI API como placeholder.
- **Filosofía del proyecto:** construir en capas. Cada capa debe funcionar antes de agregar la siguiente. No volar demasiado alto demasiado rápido.

---

## 11. Primera tarea para Claude Code

Con todo este contexto, la primera tarea es:

1. **Crear la estructura completa del monorepo** `/antigravity` con todos los archivos y carpetas definidos en la sección 6
2. **Inicializar los archivos base**: `pyproject.toml` para cada módulo, `docker-compose.yml` con SQLite + ChromaDB + Neo4j, `.env.example` con todas las variables necesarias
3. **Implementar los schemas Pydantic** de la sección 4 (eventos técnicos, emocionales, perfil inferido, respuesta de contexto)
4. **Implementar la interfaz abstracta Observer** con el Observador técnico como primera implementación concreta
5. **Proponer el schema SQL** para el store bruto (técnico y emocional) y el schema Cypher para Neo4j

No implementar nada que no esté en esta lista. Si hay ambigüedad en algún punto, preguntar antes de asumir.

---

*Este documento es el punto de partida, no el destino. Cada sesión de implementación puede refinar una sección. Las decisiones tomadas acá están razonadas — si hay razón técnica para cambiarlas, argumentar antes de cambiar.*
