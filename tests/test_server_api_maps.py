from fastapi.testclient import TestClient

from app.main import app
from app.models.server import ServerConfig


client = TestClient(app)


def test_get_server_maps_returns_maps_list(monkeypatch):
    server = ServerConfig(
        id="cod1",
        name="Call of Duty 1",
        systemd_unit="cod1.service",
        install_path="/opt/cod1",
    )

    monkeypatch.setattr("app.api.server.config_loader.get", lambda server_id: server if server_id == "cod1" else None)
    monkeypatch.setattr("app.api.server.GameContentService.get_maps", lambda _: ["mp_alpha", "mp_beta"])

    response = client.get("/api/v1/server/cod1/maps")

    assert response.status_code == 200
    assert response.json() == ["mp_alpha", "mp_beta"]


def test_get_server_maps_returns_404_for_unknown_server(monkeypatch):
    monkeypatch.setattr("app.api.server.config_loader.get", lambda server_id: None)

    response = client.get("/api/v1/server/unknown/maps")

    assert response.status_code == 404
    assert response.json() == {"detail": "Server not found"}
