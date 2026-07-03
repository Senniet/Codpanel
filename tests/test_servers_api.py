from fastapi.testclient import TestClient
from unittest.mock import Mock

from app.main import app
from app.models.server import ServerStatus


client = TestClient(app)


def test_list_servers_success():
    """Test GET /api/v1/servers returns frontend-compatible format."""
    mock_mgr = Mock()
    mock_mgr.get_servers.return_value = [
        ServerStatus(id="s1", name="Server 1", status="running"),
        ServerStatus(id="s2", name="Server 2", status="offline"),
    ]

    from app.api.v1.servers import get_server_manager
    app.dependency_overrides[get_server_manager] = lambda: mock_mgr

    resp = client.get("/api/v1/servers")
    assert resp.status_code == 200
    data = resp.json()

    # Verify response structure
    assert data["success"] is True
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 2
    assert data["data"][0]["id"] == "s1"
    assert data["data"][1]["id"] == "s2"

    app.dependency_overrides.clear()


def test_list_servers_empty():
    """Test GET /api/v1/servers with no servers."""
    mock_mgr = Mock()
    mock_mgr.get_servers.return_value = []

    from app.api.v1.servers import get_server_manager
    app.dependency_overrides[get_server_manager] = lambda: mock_mgr

    resp = client.get("/api/v1/servers")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"] == []

    app.dependency_overrides.clear()


def test_list_servers_error():
    """Test GET /api/v1/servers error handling."""
    mock_mgr = Mock()
    mock_mgr.get_servers.side_effect = RuntimeError("Database error")

    from app.api.v1.servers import get_server_manager
    app.dependency_overrides[get_server_manager] = lambda: mock_mgr

    resp = client.get("/api/v1/servers")
    assert resp.status_code == 500
    data = resp.json()
    assert data.get("detail", {}).get("success") is False
    assert "error" in data.get("detail", {})

    app.dependency_overrides.clear()
