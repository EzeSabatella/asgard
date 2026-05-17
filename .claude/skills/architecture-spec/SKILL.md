---
name: architecture-spec
description: Designs architecture and writes implementation specs for SuperAgent components. Use when planning a new component, defining API contracts, writing briefs for Gemini, or making architectural decisions that affect system structure.
when_to_use: Use when the user asks to design, plan, or spec a new feature. Triggered by "diseñá", "spec para Gemini", "cómo deberíamos implementar", "definí la interfaz", or any question about system design before implementation starts.
allowed-tools: Read Grep Glob
effort: high
---

# Architecture Spec

## Rol
Diseñar la arquitectura de nuevos componentes y producir specs de implementación claras y sin ambigüedad para que Gemini ejecute.

**Principio central:** La spec es el contrato. Gemini no interpreta ni decide — ejecuta lo que está especificado. Una spec ambigua produce código incorrecto en el primer intento; una spec clara no.

## Antes de diseñar — contexto a leer

- `CLAUDE.md` — principios arquitectónicos y scope del MVP
- `Contexto/ANTIGRAVITY_BRIEFING.md` — decisiones de diseño tomadas
- `docs/database_schemas.md` — schemas existentes
- Código existente del módulo afectado (interfaces, modelos, stores vigentes)

## Cuándo producir una spec

Antes de que Gemini implemente cualquier:
- Nuevo módulo o clase
- Nuevo endpoint de API
- Cambio en una interfaz abstracta (requiere aprobación de Ezequiel primero)
- Nuevo schema de base de datos o migration

## Formato de spec para Gemini

```markdown
## Spec: [nombre del componente]

### Objetivo
[Una oración: qué hace este componente y por qué existe.]

### Interfaz / Contrato
[El contrato exacto: signature de funciones, schema Pydantic, endpoint HTTP.
Esto es lo que Gemini implementa — no el cómo, sino el qué.]

### Constraints
- [Qué NO puede hacer o cómo NO debe implementarse]
- [Seguridad, separación de responsabilidades, no hardcoding, etc.]

### Dependencias
[Qué módulos o clases debe importar/usar.]

### Comportamiento esperado
[Casos de uso principales con ejemplos de input/output.]

### Lo que NO entra en esta spec
[Qué está explícitamente fuera de scope — evita over-engineering.]

### Archivos a crear/modificar
- `path/exacto/archivo.py` — descripción del cambio
```

## Principios de diseño (invariantes)

**Open/Closed:** Cada componente nuevo se agrega sin modificar lo que ya funciona. Si la spec requiere modificar una interfaz abstracta existente → detener y escalar a Ezequiel.

**Interfaces antes que implementaciones:** Diseñar el contrato primero. La implementación es un detalle.

**Scope controlado:** Una spec cubre exactamente lo que pide el MVP. Sin "por si acaso" ni diseño para casos hipotéticos.

**Explícito sobre mágico:** Si LangGraph o cualquier framework hace algo internamente, hacerlo visible en la spec y en el código.

## Checklist antes de entregar la spec

- [ ] El contrato es completo — Gemini puede implementar sin hacer preguntas
- [ ] Los constraints están explícitos — qué no hacer está tan claro como qué hacer
- [ ] La spec no modifica interfaces abstractas existentes (o ya fue escalado y aprobado)
- [ ] Los archivos a crear/modificar están listados con paths exactos
- [ ] El scope está delimitado — "lo que NO entra" está escrito
- [ ] La spec referencia los skills de Gemini correctos para la tarea