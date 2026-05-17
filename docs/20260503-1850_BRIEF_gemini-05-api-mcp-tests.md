# Brief 05 — API REST + MCP Skeleton + Tests de integración

**Tipo:** BRIEF  
**Fecha:** 2026-05-03 18:50  
**Autor:** Claude  
**Relacionado con:** DEC-005 (docs/20260503-1800_DECISION_decisions-log-sesion-01.md)  
**Estado:** Vigente

---

## Objetivo

Implementar la capa de exposición del chassis: API REST con FastAPI (endpoints del MVP) y un skeleton MCP funcional (`tools/list` + `tools/call`). Incluye tests de integración del pipeline completo.

## Skills a activar

- [ ] `python-backend-dev` — FastAPI, Pydantic, endpoints REST, async
- [ ] `qa-engineer` — tests de integración, httpx TestClient, coverage >70%

## Contexto — documentos a leer primero

- `CLAUDE.md` — sección "API" y "MCP"
- `SUPERAGENT.md` — sección "Interfaces: MCP + REST"
- `docs/20260503-1800_DECISION_decisions-log-sesion-01.md` — DEC-005
- Todos los módulos de briefs anteriores (01-04) deben estar implementados antes de este brief
- `chassis/src/chassis/config.py` — `get_config()` para configuración de la app

---

## Tareas

### Tarea 1: Aplicación FastAPI principal

**Archivo a crear:**
- `chassis/src/chassis/api/app.py`

**Contrato — estructura de la app:**

```python
from fastapi import FastAPI
from chassis.config import get_config
from chassis.api.routes import turns, profile, proposals, health
from chassis.api.mcp import mcp_router

def create_app() -> FastAPI:
    config = get_config()
    app = FastAPI(
        title="Asgard Chassis",
        version=config.mcp.server_version,
        docs_url="/docs",
        redoc_url=None,
    )
    app.include_router(health.router)
    app.include_router(turns.router, prefix="/turns")
    app.include_router(profile.router, prefix="/profile")
    app.include_router(proposals.router, prefix="/proposals")
    app.include_router(mcp_router, prefix="/mcp")
    return app

app = create_app()
```

**Constraints:**
- `create_app()` es una factory — facilita el testing (cada test crea su propia instancia)
- No hacer startup logic en el módulo top-level (usar `lifespan` de FastAPI para inicialización)

---

### Tarea 2: Endpoints REST

**Archivos a crear:**
- `chassis/src/chassis/api/routes/health.py`
- `chassis/src/chassis/api/routes/turns.py`
- `chassis/src/chassis/api/routes/profile.py`
- `chassis/src/chassis/api/routes/proposals.py`
- `chassis/src/chassis/api/routes/__init__.py` (vacío)

**Contratos de endpoints:**

#### `GET /health`
```
Response 200:
{
  "status": "ok",
  "version": "0.1.0",
  "instance_type": "personal"
}
```

#### `POST /turns`
```
Request body (ConversationTurn):
{
  "user_id": "string",
  "content": "string",
  "role": "user" | "assistant",
  "timestamp": "ISO 8601"
}

Response 202 (Accepted — procesamiento async):
{
  "turn_id": "uuid",
  "status": "queued"
}
```

#### `GET /profile`
```
Response 200: PersonalProfile | EnterpriseProfile (según instance_type del config)
Response 404: {"detail": "Profile not found"} si no hay perfil inicializado
```

#### `GET /proposals`
```
Response 200:
[
  {
    "proposal_id": "uuid",
    "skill_name": "string",
    "gap_description": "string",
    "created_at": "ISO 8601",
    "status": "pending" | "approved" | "rejected"
  }
]
```

#### `POST /proposals/{proposal_id}/approve`
```
Response 200: {"proposal_id": "uuid", "status": "approved"}
Response 404: {"detail": "Proposal not found"}
```

**Constraints para este MVP:**
- `POST /turns` encola el turn pero NO procesa — retorna 202 sin ejecutar el pipeline completo (el pipeline completo es Fase 1)
- `GET /profile` puede retornar un perfil mock/vacío — lo importante es que el endpoint existe y responde correctamente
- `GET /proposals` puede retornar lista vacía `[]` — lo importante es el contrato
- `POST /proposals/{id}/approve` puede retornar 404 siempre en MVP — lo importante es el endpoint
- Sin autenticación en MVP — agregar nota en código indicando que auth va en Fase 1

---

### Tarea 3: MCP Skeleton

**Archivo a crear:**
- `chassis/src/chassis/api/mcp.py`

**Contrato — dos endpoints MCP mínimos:**

```python
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, List

mcp_router = APIRouter(tags=["MCP"])


class McpTool(BaseModel):
    name: str
    description: str
    inputSchema: Dict[str, Any]


class McpToolsListResponse(BaseModel):
    tools: List[McpTool]


class McpToolCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any] = {}


class McpToolCallResponse(BaseModel):
    content: List[Dict[str, Any]]
    isError: bool = False


@mcp_router.get("/tools/list", response_model=McpToolsListResponse)
async def mcp_tools_list() -> McpToolsListResponse:
    """
    MCP tools/list — returns available tools.
    MVP: returns 2 stub tools. Full implementation in Phase 1.
    """
    return McpToolsListResponse(tools=[
        McpTool(
            name="get_context",
            description="Retrieves the user's digital context profile for LLM consumption",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "detail_level": {"type": "string", "enum": ["summary", "full"]}
                },
                "required": ["user_id"]
            }
        ),
        McpTool(
            name="record_turn",
            description="Records a conversation turn for context learning",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "role": {"type": "string", "enum": ["user", "assistant"]}
                },
                "required": ["content", "role"]
            }
        )
    ])


@mcp_router.post("/tools/call", response_model=McpToolCallResponse)
async def mcp_tools_call(request: McpToolCallRequest) -> McpToolCallResponse:
    """
    MCP tools/call — executes a tool.
    MVP: stub responses. Real implementation in Phase 1.
    """
    if request.name == "get_context":
        return McpToolCallResponse(content=[{
            "type": "text",
            "text": "Context stub — Phase 1 will return real profile data"
        }])
    elif request.name == "record_turn":
        return McpToolCallResponse(content=[{
            "type": "text",
            "text": "Turn recorded (stub)"
        }])
    else:
        return McpToolCallResponse(
            content=[{"type": "text", "text": f"Unknown tool: {request.name}"}],
            isError=True
        )
```

**Constraints:**
- El MCP skeleton usa HTTP (no stdio) — suficiente para testing. La transport stdio es Fase 1
- Los nombres de tools (`get_context`, `record_turn`) son los nombres finales — no cambiarlos
- `isError: bool` sigue la spec MCP — no cambiar el nombre del campo

---

### Tarea 4: Entrypoint de la aplicación

**Archivo a crear:**
- `chassis/src/main.py`

**Contrato:**

```python
import uvicorn
from chassis.api.app import app
from chassis.config import get_config


if __name__ == "__main__":
    config = get_config()
    uvicorn.run(
        "chassis.api.app:app",
        host=config.api.host,
        port=config.api.port,
        reload=config.api.debug,
    )
```

**Constraints:**
- `uvicorn` debe agregarse a `requirements.txt`
- La lógica de inicialización (stores, registry) va en el `lifespan` de FastAPI — no aquí

---

### Tarea 5: Tests de integración

**Archivo a crear:**
- `chassis/tests/test_api_integration.py`

**Contrato (usar `httpx.AsyncClient` con `TestClient` de FastAPI):**

```python
def test_health_returns_200():
    """GET /health retorna 200 con status=ok."""

def test_health_includes_instance_type():
    """GET /health incluye el instance_type del config."""

def test_post_turn_returns_202():
    """POST /turns con payload válido retorna 202."""

def test_post_turn_invalid_payload_returns_422():
    """POST /turns sin campos requeridos retorna 422."""

def test_get_proposals_returns_list():
    """GET /proposals retorna una lista (puede estar vacía)."""

def test_mcp_tools_list_returns_two_tools():
    """GET /mcp/tools/list retorna exactamente 2 tools."""

def test_mcp_tools_call_get_context():
    """POST /mcp/tools/call con name=get_context retorna isError=false."""

def test_mcp_tools_call_unknown_tool_returns_error():
    """POST /mcp/tools/call con tool desconocido retorna isError=true."""
```

**Constraints:**
- Usar `fastapi.testclient.TestClient` (síncrono) — no necesita `pytest-asyncio` para estos tests
- No mockear los endpoints — testear el stack completo con la app real
- `httpx` debe estar en `requirements.txt`

---

## Lo que NO entra en este brief

- Pipeline completo (clasificar → observar → guardar) — es Fase 1
- Autenticación / autorización — es Fase 1
- MCP stdio transport — es Fase 1
- ChromaDB ni Neo4j — son Fase 1
- WebSocket / SSE — es Fase 1

## Definición de Done

- [ ] `uvicorn chassis.api.app:app` arranca sin error
- [ ] `GET /health` → 200
- [ ] `POST /turns` con payload válido → 202
- [ ] `GET /mcp/tools/list` → 200 con 2 tools
- [ ] `POST /mcp/tools/call` con `get_context` → `isError: false`
- [ ] Los 8 tests de integración pasan
- [ ] `uvicorn`, `httpx`, `fastapi` en `requirements.txt`
- [ ] Sin credenciales hardcodeadas
- [ ] Cobertura de tests ≥ 70% del código nuevo