# Template — BRIEF para Gemini

```markdown
# [Título del Brief]

**Tipo:** BRIEF
**Fecha:** YYYY-MM-DD HH:MM
**Autor:** Claude
**Relacionado con:** [spec o decisión que origina este brief, o "—"]
**Estado:** Vigente

---

## Objetivo

[Una oración: qué debe producir Gemini al completar este brief.]

## Skills a activar

Gemini debe activar los siguientes skills antes de implementar:
- [ ] `[skill-name]` — [por qué aplica]
- [ ] `[skill-name]` — [por qué aplica]

## Contexto — documentos a leer primero

- `CLAUDE.md` — principios y constraints del proyecto
- `SUPERAGENT.md` — arquitectura completa
- `[otros archivos relevantes]`

## Tareas

### Tarea 1: [nombre]

**Archivos a crear/modificar:**
- `path/exacto/archivo.py` — descripción del cambio

**Contrato / interfaz:**
[El qué, no el cómo. Signatures, schemas Pydantic, endpoints.]

**Constraints:**
- [Qué NO puede hacer]
- [Qué NO puede romper]

**Comportamiento esperado:**
[Input → output con ejemplos concretos]

### Tarea 2: [nombre]
[mismo formato]

## Lo que NO entra en este brief

- [Funcionalidad explícitamente fuera de scope]

## Definición de Done

- [ ] [Criterio verificable 1]
- [ ] [Criterio verificable 2]
- [ ] Tests presentes para los componentes nuevos
- [ ] Sin credenciales hardcodeadas
- [ ] Sin modificaciones a interfaces abstractas existentes
```
