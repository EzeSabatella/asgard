# Template — SPEC

```markdown
# Spec: [Nombre del componente]

**Tipo:** SPEC
**Fecha:** YYYY-MM-DD HH:MM
**Autor:** Claude
**Relacionado con:** [DECISION o BRIEF que origina esta spec, o "—"]
**Estado:** Vigente

---

## Objetivo

[Una oración: qué hace este componente y por qué existe.]

## Interfaz / Contrato

[El contrato exacto. Esto es lo que Gemini implementa.]

```python
# Ejemplo: clase abstracta, schema Pydantic, o endpoint HTTP
class NombreComponente:
    def metodo(self, param: Tipo) -> ReturnType:
        ...
```

## Dependencias

- `path/a/modulo.py` — [qué importa de ahí]

## Comportamiento esperado

### Caso principal
**Input:** [descripción o ejemplo]  
**Output:** [descripción o ejemplo]

### Casos edge
- [edge case 1]: [comportamiento esperado]
- [edge case 2]: [comportamiento esperado]

## Constraints

- [Qué NO puede hacer]
- [Qué NO puede modificar]
- [Restricciones de seguridad aplicables]

## Lo que NO entra en esta spec

- [Funcionalidad explícitamente fuera de scope]

## Archivos a crear/modificar

| Archivo | Acción | Descripción |
|---|---|---|
| `path/archivo.py` | Crear | [qué contiene] |
| `path/otro.py` | Modificar | [qué cambia] |
```
