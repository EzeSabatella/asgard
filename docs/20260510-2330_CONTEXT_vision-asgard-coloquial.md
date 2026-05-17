# Asgard — Qué estamos construyendo y por qué importa

**Tipo:** CONTEXT  
**Fecha:** 2026-05-10  
**Autor:** Ezequiel Sabatella / Claude  
**Audiencia:** Cualquier persona, tenga o no perfil técnico  
**Uso:** Referencia personal y contexto para modelos de lenguaje

---

## El problema que nadie resolvió todavía

Cada vez que abrís una conversación nueva con una inteligencia artificial —ChatGPT, Claude, Gemini, cualquiera— el modelo no sabe nada de vos.

No sabe cómo pensás. No sabe en qué estás trabajando. No sabe qué decisiones tomaste la semana pasada ni por qué las tomaste así. No sabe cómo preferís que te hablen. No sabe qué proyectos tenés activos, qué te preocupa, qué te entusiasma.

Empezás de cero cada vez.

Entonces lo que hacés —lo que todos hacemos— es explicar el contexto de nuevo. "Soy desarrollador, estoy construyendo tal cosa, el stack es este, la semana pasada decidimos hacer así porque...". Y el modelo te responde bien, dentro de esa conversación. Pero al cerrarla, todo se pierde. La próxima vez, volvés a empezar de cero.

Esto no es un bug. Es una limitación de diseño. Los modelos de lenguaje fueron diseñados para ser herramientas de consulta, no compañeros que te conocen. Son muy buenos respondiendo preguntas. Son muy malos recordando a quién le están respondiendo.

**El resultado:** el usuario repite contexto constantemente, el modelo responde sin historia, y el trabajo es menos efectivo de lo que podría ser. No porque el modelo sea malo —es increíblemente capaz— sino porque no tiene a quién responderle realmente. Le respondés a una persona en blanco en lugar de responderte a vos.

Esto no se resuelve con ventanas de contexto más grandes. Se resuelve pensando el problema de otra manera.

---

## La intuición central

El cerebro humano no recuerda eventos. Recuerda patrones.

Cuando aprendés algo nuevo —digamos, a andar en bicicleta— no recordás cada pedalazo. Recordás el equilibrio. Recordás el reflejo. Lo que persiste no es el evento sino la configuración que el evento produjo en tu sistema nervioso.

Lo mismo con las personas. No recordás cada conversación que tuviste con tu mejor amigo. Recordás cómo es. Cómo piensa. Qué le importa. Cómo reacciona. Eso es lo que permite que cada conversación nueva sea diferente a hablar con un desconocido.

**Asgard parte de esa misma lógica:**

> Lo que debe persistir no son los hechos de una conversación sino los rasgos que esa conversación reveló. No se hereda el evento — se hereda la configuración que el evento produjo.

Cada conversación que tenés revela algo sobre vos. Cómo abordás los problemas. Qué tipo de soluciones preferís. Cuándo tomás riesgos y cuándo sos conservador. Cómo comunicás. Qué proyectos te apasionan. Qué te frena.

Asgard observa esas conversaciones, extrae esos rasgos, los acumula, los organiza, y los convierte en un perfil vivo de quién sos — para que cualquier modelo de lenguaje pueda recibirlo como contexto antes de responderte.

No más empezar de cero. El modelo sabe a quién le está respondiendo.

---

## Qué es Asgard exactamente

Asgard es una infraestructura de memoria persistente para personas.

No es un modelo de lenguaje. No es un chatbot. No es una app. Es la capa que vive entre vos y cualquier modelo de lenguaje — la que convierte cada interacción en conocimiento acumulado, y ese conocimiento en contexto para la próxima.

Una forma de pensarlo: los modelos de lenguaje son motores increíblemente potentes. Pero un motor sin datos del conductor no puede calibrarse. Asgard es el sistema que aprende al conductor — sus patrones, su estilo, su historia— y los entrega al motor antes de cada carrera.

Técnicamente, Asgard se llama **chassis** — la estructura base sobre la que se construyen los productos. Es el núcleo. Todo lo demás (los compañeros, los agentes especializados, las interfaces) se construye encima del chassis.

---

## Por qué importa más de lo que parece

Los modelos de lenguaje se están comoditizando.

Hoy GPT-4 parece magia. En seis meses hay algo mejor y más barato. En dos años, el modelo en sí va a ser tan barato que nadie va a pagar por él directamente. El valor no va a estar en el modelo — va a estar en el contexto que el modelo recibe.

El activo más valioso en el ecosistema de IA no es el modelo. Es el conocimiento acumulado sobre el usuario.

Sus decisiones. Sus patrones cognitivos. Su historia de proyectos. Su estilo de comunicación. Sus preferencias técnicas. Su forma de pensar los problemas. Ese conocimiento es personal, crece con el tiempo, y no puede replicarse ni comprarse.

Quien tenga ese activo tiene una ventaja que ningún modelo nuevo puede eliminar. Porque el modelo nuevo puede ser mejor que el anterior — pero no sabe nada del usuario. Asgard sí.

---

## Cómo funciona el sistema — el flujo completo

Imaginá el sistema como una fábrica con etapas muy claras. Cada etapa tiene un rol específico. Nada le hace el trabajo a la etapa siguiente — cada una hace exactamente lo suyo y pasa el resultado.

```
Vos hablás con un agente (Claude Desktop, Cursor, Odín, cualquier herramienta)
        │
        │  El agente le manda tu conversación a Asgard
        ▼
┌──────────────────────────────────────┐
│           FastAPI Chassis             │
│  (la puerta de entrada al sistema)   │
└──────────────────┬───────────────────┘
                   │
        ┌──────────▼──────────┐
        │     Clasificador     │
        │  (el portero)        │
        └──────────┬───────────┘
                   │  activa los observadores relevantes
        ┌──────────▼──────────┐
        │  Observer Registry   │
        │                      │
        │  • TechnicalObserver │
        │  • EmpathicObserver  │
        │  • HumorObserver     │
        │  • SocialObserver    │
        └──────────┬───────────┘
                   │  produce eventos tipados
        ┌──────────▼──────────┐
        │    Stores brutos     │
        │  raw_technical.db    │
        │  raw_emotional.db    │
        └──────────┬───────────┘
                   │  (proceso periódico / automático)
        ┌──────────▼──────────┐
        │     Consolidador     │
        └───┬──────┬───────┬───┘
            │      │       │
         Store   Store   Grafo de
        Inferido Patrones Conocimiento
        (ChromaDB)(SQLite) (Neo4j)
            │      │       │
            └──────┴───────┘
                   │
           ContextResponse
     (lo que el agente recibe antes
      de responderte a vos)
```

Ahora veamos cada pieza en detalle.

---

## Las piezas del sistema, explicadas

### La puerta de entrada — FastAPI Chassis

Es la interfaz del sistema. El lugar por donde entra y sale toda la información.

Cuando un agente (Claude Desktop, Cursor, o cualquier herramienta compatible) quiere hablarle a Asgard, le habla a esta puerta. La puerta recibe tu conversación, la manda adentro del pipeline, y cuando el agente necesita contexto sobre vos, se lo devuelve por acá.

Expone dos tipos de interfaces: una estándar para herramientas de IA (llamada MCP, que es el protocolo que usan Claude Desktop, Cursor, y otros), y una REST para integración programática y testing.

**Por qué importa:** la puerta es el contrato público del sistema. Lo que entra y lo que sale está perfectamente definido. Cualquier herramienta que entienda MCP puede conectarse a Asgard sin modificaciones.

---

### El portero — Clasificador

Antes de que tu conversación llegue a los observadores, pasa por el clasificador. Su trabajo es decidir qué observadores deben activarse para este turno de conversación específico.

¿Estás hablando de código y decisiones técnicas? → activa el `TechnicalObserver`.  
¿Estás expresando frustración o entusiasmo? → activa el `EmpathicObserver`.  
¿Estás usando humor? → activa el `HumorObserver`.  
¿Estás hablando de relaciones con otras personas? → activa el `SocialObserver`.

Puede activar varios al mismo tiempo, y eso también es información — la co-activación de ciertos observadores revela patrones que ninguno de los dos revelaría por separado.

En el MVP, el clasificador usa reglas heurísticas simples (keywords, estructura del texto). En Fase 1, lo reemplaza un modelo de lenguaje liviano que entiende contexto más sutil.

**Por qué importa:** sin el clasificador, todos los observadores procesan todo, y el sistema llena el store de ruido. El clasificador es el filtro que hace que solo entre la información relevante.

---

### Los observadores — ConversationObservers

Los observadores son los oídos del sistema. Cada uno escucha la conversación buscando un tipo específico de información. Si la encuentran, extraen un evento tipado y lo mandan al store.

**TechnicalObserver** — captura decisiones técnicas. Qué stack usás, qué arquitectura elegiste y por qué, qué problemas encontraste, qué soluciones probaste. Es el más conservador: solo actúa cuando hay evidencia clara de que estás tomando una decisión técnica o documentando contexto técnico.

**EmpathicObserver** — captura estados emocionales y patrones de soporte. Cuándo estás bajo presión, qué tipo de apoyo funciona con vos, cómo reaccionás ante el fracaso o el éxito. Es el más agresivo porque las señales emocionales son frecuentemente implícitas.

**HumorObserver** — captura el estilo de humor. Si usás ironía, si usás humor negro, si te gusta el absurdo, cómo reaccionás al humor ajeno. Esto permite que los agentes se adapten a tu estilo sin parecer forzados.

**SocialObserver** — captura dinámica relacional. Cómo comunicás con distintos tipos de personas, qué rol ocupás en grupos, cómo gestionás conflictos.

Cada observador tiene tres propiedades clave:
- **Criterio de relevancia propio**: decide si el turno de conversación tiene algo para capturar.
- **Schema de escritura propio**: el formato del evento que escribe (no todos los eventos tienen la misma estructura).
- **Nivel de agresividad propio**: qué tan implícita puede ser la señal para que la capture igual.

**Por qué importa:** los observadores son la diferencia entre un sistema que acumula logs y un sistema que aprende. No guardan lo que dijiste — guardan lo que eso reveló sobre vos.

---

### Los stores brutos — raw_technical.db y raw_emotional.db

Cuando los observadores capturan algo, lo escriben acá. Son dos archivos separados: uno para eventos técnicos, otro para eventos emocionales.

¿Por qué separados? Porque la lógica de procesamiento es diferente, los patrones que buscamos son distintos, y —más importante— la privacidad es diferente. Un perfil técnico podría compartirse con un colaborador; un perfil emocional es estrictamente personal.

Ambos están encriptados en reposo (SQLCipher), lo que significa que si alguien accede al archivo físico sin la clave correcta, no puede leer nada. La clave vive en una variable de entorno, nunca en el código.

Todo evento que llega acá queda marcado como `consolidated = False`. Eso significa que fue capturado pero todavía no fue procesado. El consolidador lo procesa después.

**Por qué importa:** los stores brutos son la materia prima del sistema. La separación técnico/emocional no es un detalle de implementación — es una decisión de diseño que protege la privacidad y hace el sistema más mantenible.

---

### El consolidador

El consolidador es un proceso que corre periódicamente (por defecto a las 3am, configurable). Lee todos los eventos brutos marcados como `consolidated = False`, los procesa, extrae los rasgos estructurales, actualiza el perfil inferido, y marca los eventos como procesados.

Un evento nunca se procesa dos veces.

En el MVP, el consolidador usa reglas determinísticas simples. En Fase 1, usa un modelo de lenguaje para hacer consolidación semántica — puede entender que "elegí usar SQLite porque quiero portabilidad" y "prefiero no depender de servicios en la nube para datos sensibles" son la misma preferencia expresada de maneras distintas.

**Por qué importa:** el consolidador es donde los eventos brutos se convierten en conocimiento. Sin él, tenés un log. Con él, tenés un perfil.

---

### Los stores de conocimiento

Acá vive el perfil inferido del usuario. Son tres stores con roles distintos:

**ChromaDB (Store Inferido)** — guarda el perfil como vectores. Un vector es una representación matemática del significado de un texto. Esto permite hacer búsquedas semánticas: "dame el contexto más relevante para esta conversación" sin tener que buscar palabra por palabra. Es la memoria que el agente consulta antes de responderte.

**patterns.db (Store de Patrones)** — guarda correlaciones de co-activación entre observadores. Si cada vez que el TechnicalObserver se activa por "decisiones de arquitectura" también se activa el EmpathicObserver por "presión", eso es un patrón. El sistema aprende que las decisiones de arquitectura son estresantes para vos — y puede anticiparlo.

**Neo4j (Grafo de Conocimiento)** — guarda relaciones explícitas entre conceptos, proyectos y decisiones. "El proyecto Asgard usa FastAPI porque la decisión DEC-003 estableció que el MCP y REST deben compartir servidor". Las relaciones entre cosas son tan importantes como las cosas mismas.

**Por qué importa:** tres stores con tres tecnologías distintas porque cada tipo de conocimiento tiene su estructura natural. Forzar todo en una base de datos relacional sería como guardar un mapa de rutas, una lista de ingredientes, y un árbol genealógico en la misma planilla de cálculo.

---

### Los embeddings — el lenguaje de la similitud

Los embeddings son la tecnología que permite comparar significados, no palabras.

"Quiero algo portátil" y "prefiero no depender de infraestructura externa" significan lo mismo en muchos contextos pero no comparten ninguna palabra en común. Un sistema basado en keywords no puede relacionarlos. Un sistema basado en embeddings sí — porque los convierte a un espacio matemático donde la distancia entre puntos representa similitud semántica.

Asgard usa embeddings para dos cosas:
1. Guardar el perfil inferido de forma buscable por significado (ChromaDB)
2. Encontrar el contexto más relevante para una conversación dada

El proveedor de embeddings vive detrás de una interfaz abstracta. Hoy puede ser OpenAI, mañana puede ser un modelo local en tu propio hardware. El cambio es de configuración, no de código.

**Por qué importa:** sin embeddings, el sistema no puede entender que dos frases distintas dicen lo mismo. Los embeddings son la diferencia entre un sistema que busca palabras y un sistema que entiende conceptos.

---

### El protocolo de conexión — MCP

MCP (Model Context Protocol) es el estándar que permite a los agentes de IA comunicarse con sistemas externos de forma estructurada.

Es el lenguaje común. Claude Desktop, Cursor, y cualquier herramienta compatible hablan MCP. Asgard expone un servidor MCP. Eso significa que cualquier herramienta compatible puede conectarse a Asgard y empezar a recibirle el perfil del usuario sin ninguna integración especial.

La comunicación es bidireccional:
- El agente le manda conversaciones a Asgard (entrada al pipeline)
- El agente le pide contexto a Asgard (el perfil inferido del usuario)

**Por qué importa:** MCP es lo que hace que Asgard sea independiente del modelo. No está atado a Claude, ni a GPT, ni a Gemini. Cualquier modelo que hable MCP puede usar el contexto de Asgard. Los modelos se van a seguir mejorando — Asgard funciona con todos.

---

### Völundr — el agente meta-cognitivo (Fase 2)

Völundr es el componente más ambicioso del sistema.

Su trabajo es observar cómo usás el sistema y detectar cuándo una tarea se repite sin tener una herramienta eficiente para resolverla.

Ejemplo: si Asgard detecta que cada vez que arrancás un proyecto nuevo, pasás tres horas haciendo el mismo proceso de setup (mismas decisiones, mismos pasos, mismo orden), Völundr lo detecta, diseña una herramienta que automatiza ese proceso, y te la propone para que la apruebes.

No la deploya automáticamente. Te la muestra, te explica qué hace y por qué la creó, y espera tu aprobación. El deploy es una decisión tuya.

Este ciclo —detectar, diseñar, proponer, esperar aprobación— es lo que hace que el sistema sea meta-cognitivo: no solo conoce tus patrones, sino que actúa sobre ellos para mejorar tu eficiencia.

**Por qué importa:** Völundr es la diferencia entre un sistema que te conoce y un sistema que mejora activamente tu capacidad de trabajar. Es la capa donde Asgard deja de ser pasivo y empieza a ser un colaborador real.

---

### La configuración — chassis.config.yaml

Todo el comportamiento del sistema es configurable sin tocar código.

Un archivo YAML controla qué observadores están activos, con qué nivel de agresividad, qué modelo de embeddings usar, con qué frecuencia corre el consolidador, si el MCP está activo, y más.

```yaml
instance:
  type: personal
  user_id: ezequiel

observers:
  technical:
    enabled: true
    aggressiveness: conservative
  empathic:
    enabled: true
    aggressiveness: aggressive

embeddings:
  provider: ollama
  model: nomic-embed-text

consolidation:
  schedule: "0 3 * * *"
```

Esto significa que el mismo código puede correr de maneras completamente distintas para distintos usuarios o casos de uso — solo cambiando la configuración.

Los secretos (claves de encriptación, API keys) viven en un archivo `.env` separado, nunca en el código y nunca en el repositorio.

**Por qué importa:** la configuración es lo que hace al sistema adaptable. No necesitás ser desarrollador para cambiar el comportamiento de Asgard — necesitás entender qué hacen los parámetros.

---

## Una instancia por persona. Sin excepciones.

Asgard no es un servicio en la nube donde todos los usuarios comparten infraestructura. Cada persona tiene su propia instancia corriendo en su propio hardware (o en hardware que controla).

Por qué:
- El perfil de una persona es fundamentalmente distinto al de otra — no comparten estructura, no comparten lógica, no comparten nada.
- La privacidad es por diseño. Tus datos nunca salen de tu infraestructura.
- La portabilidad es total. Tu instancia de Asgard con todos tus datos puede moverse de un servidor a otro como un contenedor Docker.

El mismo código, configuración diferente. Una empresa puede tener su propia instancia de Asgard con observadores enfocados en patrones operativos. Una persona tiene la suya con observadores técnicos y emocionales. La arquitectura es la misma.

---

## El stack tecnológico — por qué cada tecnología

| Componente | Tecnología | Por qué esta y no otra |
|---|---|---|
| API de superficie | FastAPI (Python) | Async nativo, tipado estricto, MCP y REST desde el mismo servicio |
| Orquestación de agentes | LangGraph | Diseñado para agentes con estado persistente — no es una cadena de llamadas, es un grafo |
| Stores brutos | SQLite + SQLCipher | Encriptación en reposo, sin servidor, portable — el archivo se mueve con vos |
| Store vectorial | ChromaDB | Local, sin API externa, simple de operar |
| Grafo de conocimiento | Neo4j | Las relaciones entre conceptos son ciudadanos de primera clase, no columnas adicionales |
| Embeddings local | nomic-embed-text vía Ollama | Corre en tu hardware, gratuito, sin enviar datos a terceros |
| LLM local | llama3.2 vía Ollama | Para clasificador y consolidador — mismo principio: local, sin dependencia externa |
| Containerización | Docker + Docker Compose | Una instancia = un Compose. Portable, aislado, reproducible |
| Protocolo principal | MCP | El estándar emergente de interoperabilidad entre agentes y herramientas |

**El principio que guía el stack:** nada que no sea necesario, nada que genere dependencia que no podamos controlar. Los datos del usuario no deberían pasar por un servidor de terceros para ser procesados.

---

## Qué está construido hoy

**Fase 0 — Completada ✅**

El chassis base funciona. 22 tests automáticos pasan. Todo el pipeline de observación está operativo para eventos técnicos.

| Componente | Estado |
|---|---|
| Estructura del monorepo | ✅ |
| Modelos de datos (BaseProfile, PersonalProfile) | ✅ |
| Store bruto SQLite con encriptación | ✅ |
| ConversationObserver base + TechnicalObserver | ✅ |
| Clasificador heurístico | ✅ |
| ChromaDB + interfaz de embeddings OpenAI | ✅ |
| FastAPI endpoints REST completos | ✅ |
| MCP skeleton (tools/list + tools/call) | ✅ |
| chassis.config.yaml + carga de configuración | ✅ |
| Docker Compose (Neo4j + ChromaDB) | ✅ |
| Servidor de cómputo local (antigravity) | ✅ |
| Ollama con nomic-embed-text + llama3.2:3b | ✅ |

---

## Qué viene después

**Fase 1 — Inteligencia completa del chassis**

- Observadores emocionales (Empathic, Humor, Social)
- Clasificador LLM liviano — reemplaza heurísticas con comprensión semántica real
- Consolidador con LLM — entiende que dos frases distintas dicen lo mismo
- Detector de patrones de co-activación
- Neo4j alimentado con decisiones y conceptos del usuario
- MCP completo bidireccional

**Fase 2 — Völundr / Forge**

El agente meta-cognitivo. Detecta gaps, propone herramientas, espera aprobación humana.

**Fase 3 — Productos de superficie**

- **Odín**: compañero técnico y de bienestar para desarrolladores
- **Freyja**: compañero emocional, enfocado en vínculo y bienestar
- **Nexus**: inteligencia operativa para empresas (contact centers primero)

---

## La visión en una oración

**Asgard es la infraestructura que convierte cada interacción con una IA en conocimiento acumulado sobre vos — para que ningún modelo de lenguaje vuelva a responderte como si fueras un desconocido.**

---

## Glosario para orientarse

| Término | Qué es en lenguaje simple |
|---|---|
| **Chassis** | La infraestructura central. El motor del sistema. |
| **ConversationObserver** | Un agente que escucha una conversación buscando un tipo específico de información. |
| **Clasificador** | El portero que decide qué observadores procesan cada conversación. |
| **Store bruto** | Donde caen los eventos capturados antes de ser procesados. |
| **Consolidador** | El proceso que convierte eventos brutos en conocimiento estructurado. |
| **Store inferido** | El perfil del usuario después de ser procesado — lo que el agente consulta. |
| **Embeddings** | Representación matemática del significado — permite comparar conceptos, no palabras. |
| **ChromaDB** | La base de datos que guarda el perfil como vectores buscables por significado. |
| **Neo4j** | La base de datos de relaciones — no solo qué, sino cómo se relaciona con qué. |
| **MCP** | El protocolo estándar para que herramientas de IA hablen con sistemas externos. |
| **Völundr** | El agente que detecta cuando algo podría ser más eficiente y propone herramientas. |
| **Ollama** | El servidor que corre modelos de lenguaje localmente, en tu propio hardware. |
| **antigravity** | El nombre del servidor local donde corre el stack de producción. |
| **Hugmun IA** | La empresa / laboratorio que contiene todo el ecosistema. |

---

*Documento vivo — se actualiza con cada fase completada.*  
*Última actualización: Mayo 2026*
