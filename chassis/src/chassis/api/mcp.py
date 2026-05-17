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
