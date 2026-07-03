from fastapi.testclient import TestClient
from unittest.mock import Mock

from app.main import app
from app.models.server import ServerStatus


client = TestClient(app)


def test_server_status_success(monkeypatch):
    mock_mgr = Mock()
    mock_mgr.get_servers.return_value = [ServerStatus(id="s1", name="S1", status="running")]

    # override dependency
    from app.api.v1.server import get_server_manager
    app.dependency_overrides[get_server_manager] = lambda: mock_mgr

    resp = client.get("/api/v1/server/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert isinstance(data["servers"], list)
    assert data["servers"][0]["id"] == "s1"

    app.dependency_overrides.clear()


def test_server_status_error(monkeypatch):
    mock_mgr = Mock()
    mock_mgr.get_servers.side_effect = RuntimeError("boom")

    from app.api.v1.server import get_server_manager
    app.dependency_overrides[get_server_manager] = lambda: mock_mgr

    resp = client.get("/api/v1/server/status")
    assert resp.status_code == 500
    data = resp.json()
    # When HTTPException raised with detail set to dict, FastAPI returns that dict
    assert data.get("detail", {}).get("success") is False

    app.dependency_overrides.clear()
