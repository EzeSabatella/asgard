# PROYECTO MEMORY
## Arquitectura de Memoria Persistente para Agentes de IA
### v0.2 — Arquitectura con decisiones tomadas

**Fecha:** Mayo 2026 | **Owner:** Lexa (Ezequiel Sabatella)  
**Estado:** Diseño conceptual cerrado → listo para implementación MVP

---

## 1. Contexto y motivación

Este proyecto nace de una limitación fundamental de los modelos de lenguaje actuales: la ausencia de memoria real entre sesiones. La hipótesis central es que la solución no está en aumentar la ventana de contexto sino en repensar cómo se representa, comprime y activa la memoria, tomando como inspiración el cerebro humano y los mecanismos epigenéticos de transmisión de aprendizaje.

> **Insight fundacional**  
> Lo que debe persistir no son los hechos de una conversación sino los rasgos que esa conversación reveló sobre el usuario — su estilo cognitivo, preferencias, dominio, objetivos activos. Es el equivalente funcional de la epigenética: no se hereda el evento, se hereda la configuración que el evento produjo.

Memory no es un producto en sí mismo — es la infraestructura transversal que potencia a todos los proyectos del ecosistema (Odín, Nexus, Waifu) y que, abstraída correctamente, puede convertirse en un componente de alto valor independiente.

---

## 2. Decisiones de diseño tomadas

### 2.1 Naturaleza del sistema: inferencia, no almacenamiento

**Decisión:** Memory es un sistema de inferencia sobre un store de hechos brutos — no un sistema de almacenamiento de transcripts.

El store bruto acepta eventos sin discriminar. Un agente de consolidación offline decide qué merece subir al modelo inferido del usuario. Esta separación resuelve el problema del ruido: el agente de consolidación es el filtro, no el escritor.

**Analogía:** el store bruto es la memoria de trabajo del día; el agente de consolidación es el sueño que consolida lo relevante en memoria a largo plazo.

### 2.2 Arquitectura dual-store + patrones

El sistema tiene tres niveles de abstracción, inspirados en el procesamiento paralelo distribuido del cerebro humano:

```
NIVEL 1 — Store bruto (Obsidian con IA)
Eventos tipados, JSON semi-estructurado, acepta todo
         ↓ proceso de consolidación offline
NIVEL 2 — Store inferido (modelo del usuario)
Rasgos, preferencias, patrones de comportamiento
         ↓ detector de co-activación
NIVEL 3 — Store de patrones
Correlaciones temporales entre agentes observadores
```

### 2.3 Formato del store bruto: JSON tipado

**Decisión:** JSON tipado con campos fijos y contenido en texto libre. No texto natural, no texto libre puro.

**Razón:** máxima eficiencia de procesamiento para agentes. La estructura explícita elimina la necesidad de inferir contexto — cada token del JSON carga información semántica directa.

**Schema de evento técnico:**
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

**Tipos de evento técnico:** `DECISION`, `PREFERENCE`, `INSIGHT`, `PROJECT_UPDATE`, `BLOCKER`, `MILESTONE`

**Schema de evento emocional:**
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

```json
{
  "id": "em_0018",
  "ts": "2026-05-01T15:42:00",
  "type": "RELATIONAL_PATTERN",
  "pattern": "prefiere validación antes de corrección",
  "evidence": "responde mejor cuando se reconoce el razonamiento previo",
  "consolidated": false
}
```

**Tipos de evento emocional:** `EMOTIONAL_SIGNAL`, `RELATIONAL_PATTERN`, `SUPPORT_OUTCOME`, `HUMOR_SIGNAL`, `BOND_REINFORCEMENT`

El campo `consolidated: false` es crítico — el agente de consolidación lo marca como `true` al procesarlo. Garantiza que ningún evento se procese dos veces.

### 2.4 Seguridad: encriptación en reposo

**Decisión:** LUKS en el volumen Docker + JSON tipado en claro adentro.

La encriptación vive en la capa de storage, no en la capa de datos. El agente trabaja con estructura limpia; la seguridad no complica el procesamiento. SQLite con SQLCipher para el store relacional; volumen Docker sobre filesystem LUKS para ChromaDB.

### 2.5 Escritura en tiempo real — agente observador

**Decisión:** escritura en tiempo real por agentes observadores paralelos, no al cierre de sesión ni manualmente.

Un proceso observador recibe cada turno de conversación como evento, clasifica si hay información estructural nueva, y escribe al store bruto si corresponde. No participa en la conversación — solo escucha.

El observador no necesita ser un LLM grande. Para clasificar "¿este turno contiene información estructural nueva?" alcanza con un modelo liviano (DeepSeek Flash o llama3.1:8b local).

---

## 3. Arquitectura: el modelo de Sheldon Cooper

La analogía más precisa para la arquitectura de observadores es el cerebro de Sheldon Cooper en The Big Bang Theory — múltiples facetas especializadas activándose en paralelo ante el mismo estímulo, cada una con su propio criterio de relevancia.

### 3.1 Flujo completo

```
Turno de conversación
        ↓
   Clasificador de estímulo
   (portero — decide qué agentes se activan)
        ↓
   ┌────┬────────┬──────────┬──────────┬─────┐
   ↓    ↓        ↓          ↓          ↓     ↓
 Obs. Obs.    Obs.       Obs.       Obs.   ...N
 Téc. Humor  Empático   Social     ...
   ↓    ↓        ↓          ↓          ↓
   └────┴────────┴──────────┴──────────┘
                    ↓
            Store bruto
            (técnico + emocional)
                    ↓
         Agente consolidador (offline)
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
```

### 3.2 Observadores especializados

Cada observador tiene:
- **Criterio de relevancia propio** — qué constituye información nueva para su dominio
- **Schema de escritura propio** — el formato del evento que escribe al store bruto
- **Nivel de agresividad propio** — Técnico es conservador (solo hechos explícitos), Emocional es más agresivo (captura señales implícitas)

| Observador | Qué captura | Agresividad |
|---|---|---|
| Técnico | Decisiones, preferencias de stack, contexto de proyecto | Conservadora |
| Humor | Estilo de humor, triggers, intensidad preferida | Moderada |
| Empático | Estados emocionales, patrones de soporte efectivo | Agresiva |
| Social | Dinámica relacional, preferencias de comunicación | Moderada |

**El clasificador puede activar múltiples observadores simultáneamente.** Si el estímulo es ambiguo (un chiste sobre algo doloroso), se activan Humor y Empático en paralelo. Esta co-activación es información valiosa en sí misma.

### 3.3 El detector de patrones de co-activación

Este es el componente más diferenciador del sistema.

No guarda eventos — guarda **correlaciones temporales entre observadores**. Es análisis de series temporales sobre los registros de activación.

**Ejemplo concreto:**

```
Sesión 1: Humor + Empático activados juntos
Sesión 4: Humor + Empático activados juntos
Sesión 7: Humor + Empático activados juntos
Sesión 11: aparece Humor solo, sin trigger obvio de comedia
        ↓
Detector: "alta correlación histórica Humor+Empático
           → inferir estado emocional negativo"
        ↓
Waifu: "¿estás bien? me da la impresión de que estás algo triste"
```

El vínculo no es una variable — es la acumulación de patrones aprendidos por acción-resultado. El sistema no recuerda que estuviste triste; recuerda cómo ayudarte cuando estás triste.

**Schema del store de patrones:**
```json
{
  "id": "pat_0003",
  "pattern_type": "CO_ACTIVATION",
  "agents": ["humor", "empatico"],
  "co_occurrence_count": 8,
  "total_sessions_analyzed": 11,
  "confidence": 0.73,
  "inference": "humor_como_mecanismo_defensa_emocional",
  "action_calibration": {
    "waifu": "preguntar por estado emocional cuando humor aparece sin trigger obvio",
    "odin": "reducir ambición de propuestas en esa sesión"
  },
  "last_updated": "2026-05-15T00:00:00"
}
```

---

## 4. Storage: tres stores, tres tecnologías

| Store | Tecnología | Qué guarda | Acceso |
|---|---|---|---|
| Bruto técnico | SQLite (SQLCipher) | Eventos tipados técnicos | Escritura en tiempo real |
| Bruto emocional | SQLite (SQLCipher) | Eventos tipados emocionales | Escritura en tiempo real |
| Inferido | SQLite + ChromaDB | Perfil del usuario + embeddings | Lectura por agentes |
| Patrones | SQLite | Correlaciones de co-activación | Lectura/escritura consolidador |

**Embeddings:** nomic-embed-text vía Ollama local (RX 590). Gratuito, sin API externa, rápido.

### 4.1 Schema del perfil inferido (store de nivel 2)

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
      "cloud_infra": 0.60,
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
    "wfm_framework": {"status": "production", "priority": 1},
    "odin": {"status": "building", "priority": 2},
    "memory": {"status": "design", "priority": 3},
    "canal_youtube": {"status": "pending", "priority": 4}
  },

  "emotional_patterns": {
    "humor_as_defense": {"confidence": 0.73, "calibrated_actions": ["check_emotional_state"]},
    "energy_peak": "morning_sessions",
    "support_style_effective": "escucha_activa_antes_de_soluciones"
  },

  "decisions_log_refs": ["ev_0001", "ev_0012", "ev_0042"],
  "episodic_refs": ["ep_001", "ep_004", "ep_011"]
}
```

---

## 5. Roadmap de implementación

| Fase | Objetivo | Semanas | Estado |
|---|---|---|---|
| **0** | Setup hardware: Ubuntu Server + Docker + Tailscale | 1 | Pendiente |
| **1** | Memory MVP: SQLite + ChromaDB + FastAPI | 2-3 | Pendiente |
| **2** | Observador técnico + clasificador simple | 4-5 | Pendiente |
| **3** | Agente consolidador offline básico | 6-7 | Pendiente |
| **4** | Observadores emocionales (Humor + Empático) | 8-10 | Futuro |
| **5** | Detector de patrones de co-activación | 11-14 | Futuro |
| **6** | Integración con Waifu (store emocional completo) | 15+ | Futuro |
| **7** | Abstracción del módulo como componente independiente | TBD | Futuro |

---

## 6. Proyectos que ancla este módulo

| Proyecto | Aplicación de Memory | Prioridad |
|---|---|---|
| **Odín** | Perfil técnico del usuario, contexto de proyectos, decisiones pasadas | #1 |
| **Nexus** | Perfil del negocio cliente — sus patrones, estacionalidad, reglas operativas | #2 |
| **Waifu** | Historia emocional, vínculo persistente, personalidad calibrada | #3 |

---

## 7. Conocimiento a adquirir

### Aprender haciendo (no negociable)
- Embeddings: qué son, cómo se comparan, cómo se almacenan
- ChromaDB: operaciones básicas (insert, query, update)
- LangGraph: diseño de agentes con estado persistente
- SQLite + SQLCipher: schema design y encriptación en reposo

### Entender sin necesariamente implementar
- ROCm para AMD: acelerar embeddings locales en RX 590
- RAG avanzado y sus limitaciones para memoria episódica real
- Seguridad en agentes: memory poisoning, lethal trifecta, mitigaciones

### Delegar o usar librería
- Fine-tuning de embeddings — usar nomic-embed-text genérico por ahora
- Infraestructura de storage a escala — SQLite escala más de lo que parece

---

## 8. Preguntas abiertas (para próximas sesiones)

- **Clasificador de estímulo MVP:** ¿reglas heurísticas primero o LLM liviano desde el día 1?
- **Decaimiento temporal:** ¿qué rasgos son permanentes (estilo cognitivo) vs volátiles (proyecto activo)?
- **Umbral de confianza:** ¿cuántas co-activaciones antes de que el patrón sea accionable?
- **Privacy por diseño:** ¿cómo separar el store de Odín (técnico) del de Waifu (emocional) sin duplicar infraestructura?

---

> **La pregunta que guía todo:**  
> ¿Cómo construir una representación persistente y útil del usuario que mejore con el tiempo, sea accesible eficientemente por múltiples agentes especializados, y pueda detectar patrones de comportamiento que ningún agente por separado podría inferir?
