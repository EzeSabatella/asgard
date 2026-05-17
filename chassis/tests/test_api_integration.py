from fastapi.testclient import TestClient
from chassis.api.app import create_app
from chassis.config import get_config
import uuid
from datetime import datetime

# Initialize the test client
app = create_app()
client = TestClient(app)

def test_health_returns_200():
    """GET /health retorna 200 con status=ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_health_includes_instance_type():
    """GET /health incluye el instance_type del config."""
    response = client.get("/health")
    config = get_config()
    assert response.json()["instance_type"] == config.instance.type

def test_post_turn_returns_202():
    """POST /turns con payload válido retorna 202."""
    payload = {
        "user_id": "u1",
        "session_id": "s1",
        "turn_id": "t1",
        "timestamp": datetime.now().isoformat(),
        "role": "user",
        "content": "hello"
    }
    response = client.post("/turns", json=payload)
    assert response.status_code == 202
    assert "turn_id" in response.json()

def test_post_turn_invalid_payload_returns_422():
    """POST /turns sin campos requeridos retorna 422."""
    payload = {
        "user_id": "u1",
        # missing content, role, timestamp, session_id, turn_id
    }
    response = client.post("/turns", json=payload)
    assert response.status_code == 422

def test_get_proposals_returns_list():
    """GET /proposals retorna una lista (puede estar vacía)."""
    response = client.get("/proposals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_mcp_tools_list_returns_two_tools():
    """GET /mcp/tools/list retorna exactamente 2 tools."""
    response = client.get("/mcp/tools/list")
    assert response.status_code == 200
    data = response.json()
    assert "tools" in data
    assert len(data["tools"]) == 2

def test_mcp_tools_call_get_context():
    """POST /mcp/tools/call con name=get_context retorna isError=false."""
    payload = {
        "name": "get_context",
        "arguments": {"user_id": "u1"}
    }
    response = client.post("/mcp/tools/call", json=payload)
    assert response.status_code == 200
    assert response.json()["isError"] is False

def test_mcp_tools_call_unknown_tool_returns_error():
    """POST /mcp/tools/call con tool desconocido retorna isError=true."""
    payload = {
        "name": "unknown_tool",
        "arguments": {}
    }
    response = client.post("/mcp/tools/call", json=payload)
    assert response.status_code == 200
    assert response.json()["isError"] is True
