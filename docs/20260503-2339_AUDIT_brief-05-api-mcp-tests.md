# Auditoría Brief 05 — API REST + MCP skeleton + tests de integración

**Tipo:** AUDIT  
**Fecha:** 2026-05-03 23:39  
**Autor:** Claude  
**Brief auditado:** [20260503-1850_BRIEF_gemini-05-api-mcp-tests.md](20260503-1850_BRIEF_gemini-05-api-mcp-tests.md)  
**Estado:** APROBADO

---

## Veredicto

**APROBADO sin correcciones.** 8/8 tests de integración pasando. Suite completa del MVP: 22/22 verde.

---

## Checklist de seguridad

- [x] Sin credenciales hardcodeadas
- [x] Sin rutas absolutas hardcodeadas
- [x] `api_key` no aparece en ningún endpoint ni log
- [x] Los stubs de Fase 1 devuelven 404 correctamente — no exponen datos inexistentes

## Checklist de arquitectura

- [x] `create_app()` como factory — testeable sin side effects globales
- [x] Estructura de routers separados por dominio (`health`, `turns`, `profile`, `proposals`)
- [x] MCP en router propio (`/mcp`) — desacoplado del REST
- [x] Configuración leída de `get_config()` — no hardcodeada en la app
- [x] `main.py` usa `config.api.host/port/debug` — entrypoint configurable
- [x] `reload=config.api.debug` — hot reload solo en modo debug ✅

## Checklist de código

- [x] Tipos completos en todas las signatures
- [x] Sin imports no utilizados
- [x] `routes/__init__.py` presente

---

## Análisis por componente

### `api/app.py` ✅

Factory `create_app()` limpia. Registra todos los routers con sus prefijos correctos. El objeto `app` global al final del archivo permite que uvicorn lo importe con `"chassis.api.app:app"`. Correcto.

### `api/mcp.py` ✅

Skeleton MCP bien implementado. Los dos tools (`get_context`, `record_turn`) tienen sus `inputSchema` con JSON Schema válido. `tools/call` devuelve `isError=True` para tools desconocidos — correcto para el protocolo MCP.

### `api/routes/health.py` ✅

Devuelve `status`, `version` e `instance_type`. El test verifica `instance_type` contra el config real.

### `api/routes/turns.py` ✅

`POST /turns` acepta `ConversationTurn` nativo de Pydantic — la validación de 422 es automática. Devuelve `turn_id` y `status: queued`. El endpoint no procesa el turn aún (correcto para MVP — el pipeline completo es Fase 1).

### `api/routes/profile.py` ✅

Stub correcto con 404. El `response_model=Union[PersonalProfile, EnterpriseProfile]` es un buen placeholder — documenta el contrato futuro sin implementarlo.

### `api/routes/proposals.py` ✅

Lista vacía en `GET /proposals`. 404 en `POST /proposals/{id}/approve`. Correcto para MVP.

### `test_api_integration.py` ✅

Los 8 tests usan `TestClient` síncrono — correcto para tests de integración FastAPI. Gemini aplicó el aprendizaje del Brief 04: `ConversationTurn` construido con todos los campos requeridos. El test de 422 verifica que la validación de Pydantic funciona correctamente en la capa HTTP.

---

## Observaciones (no bloquean)

1. **`POST /turns` no conecta con el pipeline todavía** — esperado. El brief lo especifica explícitamente como stub. El wire-up a `Classifier → Observers → RawStore` es trabajo de Fase 1.

2. **`GET /profile` sin `user_id` en la ruta** — el endpoint está montado en `/profile` sin `/{user_id}`. El contrato del SUPERAGENT.md define `GET /profile/{user_id}`. Esto es un detalle menor que deberá corregirse en Fase 1 cuando el endpoint se implemente realmente.

3. **Sin autenticación** — esperado para MVP. Los tres routers tienen `Note: Auth will be added in Phase 1` en sus docstrings.

---

## Estado del MVP completo

Suite al cierre del Brief 05:

```
22 passed in 1.34s
```

| Brief | Componente | Estado |
|---|---|---|
| 01 | ConversationObserver, BaseProfile, __init__.py | ✅ |
| 02 | chassis.config.yaml + config.py | ✅ |
| 03 | BaseStore + RawStore (SQLite) | ✅ |
| 04 | EmbeddingProvider + OpenAIEmbeddingProvider + Classifier | ✅ |
| 05 | FastAPI REST + MCP skeleton + tests integración | ✅ |

---

## Definición de Done — verificación

- [x] `GET /health` retorna 200 con `status=ok` e `instance_type`
- [x] `POST /turns` con payload válido retorna 202
- [x] `POST /turns` con payload inválido retorna 422
- [x] `GET /proposals` retorna lista vacía
- [x] `GET /mcp/tools/list` retorna exactamente 2 tools
- [x] `POST /mcp/tools/call` con tool válido retorna `isError=false`
- [x] `POST /mcp/tools/call` con tool desconocido retorna `isError=true`
- [x] 8/8 tests de integración pasan
- [x] Suite completa: 22/22 verde
- [x] Sin credenciales hardcodeadas