---
name: scribe
description: Creates and manages all project documents for SuperAgent. Enforces naming convention, saves to docs/, and updates docs/INDEX.md. Use when creating any project document — briefs for Gemini, architecture decisions, specs, audit reports, context documents, or master documents.
when_to_use: Activate for any document creation or update. Triggered by "creá un brief", "documentá esta decisión", "escribí la spec", "guardá esto", "actualizá el documento maestro", or any task that produces a document meant to persist beyond the current session.
allowed-tools: Read Write Bash
---

# Scribe — Gestor de documentos del proyecto

## Propósito
Todo documento que se cree en el proyecto SuperAgent debe ser trazable en el tiempo. El nombre del archivo es su identidad cronológica: si dos documentos tratan el mismo tema, el de fecha más reciente es la versión válida. Sin ambigüedad, sin buscar entre chats.

## Timestamp actual
!`date +%Y%m%d-%H%M`

## Patrón de nombre obligatorio

```
YYYYMMDD-HHMM_[TIPO]_[descripcion-en-kebab-case].md
```

**Ejemplos:**
```
20260503-1430_BRIEF_gemini-phase0-stores.md
20260503-1445_DECISION_mcp-bidireccional.md
20260504-0900_SPEC_base-profile-extensions.md
20260504-1100_AUDIT_phase0-observers.md
20260505-0830_REPORT_qa-fase0-resultados.md
```

**Reglas del nombre:**
- Fecha y hora: del timestamp inyectado arriba (ya calculado, solo copiar)
- Tipo: mayúsculas, sin espacios (ver tabla abajo)
- Descripción: minúsculas, palabras separadas por guion, máximo 5 palabras, en español o inglés según el contenido

## Tipos de documento

| Tipo | Qué es | Quién lo produce |
|---|---|---|
| `BRIEF` | Instrucciones para Gemini — qué implementar, spec completa | Claude |
| `DECISION` | Decisión arquitectónica o de producto — contexto, alternativas, elección, impacto | Claude / Ezequiel |
| `SPEC` | Especificación de un componente — contrato, interfaz, comportamiento esperado | Claude |
| `AUDIT` | Resultado de auditoría de código — qué está bien, qué corregir | Claude |
| `REPORT` | Reporte de estado, QA, desempeño, o avance | Claude / Gemini |
| `CONTEXT` | Documento de contexto o background — no es accionable, es referencia | Cualquiera |
| `MASTER` | Documento maestro del proyecto — visión, arquitectura completa | Claude |
| `UPDATE` | Enmienda formal a un documento existente | Claude |

## Proceso al crear un documento

### 1. Determinar tipo y nombre
Usando el timestamp inyectado arriba:
```
[timestamp del skill]_[TIPO]_[descripcion].md
```

### 2. Header estándar del documento
Todo documento empieza con este header:

```markdown
# [Título descriptivo]

**Tipo:** [TIPO]
**Fecha:** YYYY-MM-DD HH:MM
**Autor:** Claude / Gemini / Ezequiel
**Relacionado con:** [archivo anterior si aplica, o "—"]
**Estado:** [Borrador | Vigente | Reemplazado por: filename]

---
```

### 3. Guardar en `docs/`
Ruta completa: `docs/[nombre-con-patron].md`

### 4. Actualizar `docs/INDEX.md`
Agregar una línea al final de la sección correspondiente:
```markdown
| 20260503-1430 | BRIEF | [gemini-phase0-stores.md](gemini-phase0-stores.md) | Instrucciones para implementar stores SQLite |
```

## Regla de supersesión

Cuando un documento nuevo reemplaza a uno anterior:
1. El nuevo documento lo declara en su header: `**Relacionado con:** 20260503-1430_DECISION_mcp-unidireccional.md`
2. El documento anterior NO se borra — se actualiza su header: `**Estado:** Reemplazado por: 20260504-0900_DECISION_mcp-bidireccional.md`

Los documentos viejos son historia. La historia no se borra.

## Templates disponibles

Para estructura detallada de cada tipo, ver:
- [templates/BRIEF.md](templates/BRIEF.md) — estructura de briefs para Gemini
- [templates/DECISION.md](templates/DECISION.md) — estructura de decisiones arquitectónicas
- [templates/SPEC.md](templates/SPEC.md) — estructura de specs de componentes
- [templates/AUDIT.md](templates/AUDIT.md) — estructura de reportes de auditoría
- [templates/REPORT.md](templates/REPORT.md) — estructura de reportes de estado
