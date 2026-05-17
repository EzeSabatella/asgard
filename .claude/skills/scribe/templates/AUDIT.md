# Template — AUDIT

```markdown
# Auditoría: [Nombre del componente o fase]

**Tipo:** AUDIT
**Fecha:** YYYY-MM-DD HH:MM
**Autor:** Claude
**Relacionado con:** [BRIEF o SPEC que originó la implementación auditada]
**Estado:** Vigente

---

## Resultado general

**Veredicto:** [APROBADO | APROBADO CON CORRECCIONES | RECHAZADO]

**Resumen en una oración:** [qué se encontró]

---

## ✅ Lo que está bien

- [hallazgo positivo con referencia al archivo si aplica]
- [hallazgo positivo]

---

## 🔴 Crítico — bloqueante

> Debe corregirse antes de continuar.

### [Título del problema]
**Archivo:** `path/archivo.py:línea`  
**Problema:** [descripción del problema]  
**Corrección:** [qué debe cambiar exactamente]

---

## 🟡 Importante — no bloqueante

> Debe corregirse en esta iteración pero no bloquea avanzar.

### [Título del problema]
**Archivo:** `path/archivo.py:línea`  
**Problema:** [descripción]  
**Corrección sugerida:** [qué cambiar]

---

## 🟢 Menor

> Observaciones que no requieren acción inmediata.

- [observación]

---

## Correcciones para Gemini

| # | Archivo | Línea | Acción requerida |
|---|---|---|---|
| 1 | `path/archivo.py` | 42 | [descripción precisa] |
| 2 | `path/otro.py` | 17 | [descripción precisa] |

---

## Próximo paso

[ ] Gemini aplica correcciones  
[ ] Claude re-audita los puntos críticos  
[ ] Ezequiel valida y aprueba  
```
