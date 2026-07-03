import os
import logging
import textwrap
import pytest
from pathlib import Path

from app.config_loader import ConfigLoader
from app.models.server import ServerConfig


def write_yaml(path: Path, content: str) -> None:
    path.write_text(textwrap.dedent(content), encoding="utf-8")


def test_valid_configuration(tmp_path, caplog):
    caplog.set_level(logging.INFO)
    yaml = """
    servers:
      - id: cod1
        name: Call of Duty 1
        systemd_unit: cod1.service
        install_path: /opt/cod1
        executable: /opt/cod1/cod_lnxded
        config_path: /opt/cod1/main/server.cfg
        rcon_host: 127.0.0.1
        rcon_port: 28960
        rcon_password: secret
    """
    p = tmp_path / "servers.yaml"
    write_yaml(p, yaml)

    loader = ConfigLoader(path=p)
    servers = loader.load()
    assert len(servers) == 1
    s = servers[0]
    assert isinstance(s, ServerConfig)
    assert s.id == "cod1"
    assert s.name == "Call of Duty 1"
    assert s.systemd_unit == "cod1.service"
    assert s.rcon_password == "secret"


def test_missing_file(tmp_path, caplog):
    caplog.set_level(logging.WARNING)
    p = tmp_path / "does_not_exist.yaml"
    loader = ConfigLoader(path=p)
    servers = loader.load()
    assert servers == []
    assert any("not found" in rec.message for rec in caplog.records)


def test_invalid_yaml(tmp_path, caplog):
    caplog.set_level(logging.ERROR)
    p = tmp_path / "bad.yaml"
    p.write_text("!!! this is : not: valid: yaml", encoding="utf-8")
    loader = ConfigLoader(path=p)
    servers = loader.load()
    assert servers == []
    assert any("Failed to read server config" in rec.message for rec in caplog.records)


def test_invalid_server_entry(tmp_path, caplog):
    caplog.set_level(logging.WARNING)
    yaml = """
    servers:
      - id: valid
        name: Valid Server
        systemd_unit: valid.service
      - not_a_mapping
      - id: bad_missing_unit
        name: Bad Server
    """
    p = tmp_path / "mixed.yaml"
    write_yaml(p, yaml)
    loader = ConfigLoader(path=p)
    servers = loader.load()
    # Only the valid mapping with required fields should be returned
    assert any(s.id == "valid" for s in servers)
    assert not any(s.id == "bad_missing_unit" for s in servers)
    assert any("Skipping invalid server entry" in rec.message or "validation failed" in rec.message.lower() for rec in caplog.records)


def test_env_substitution(tmp_path, monkeypatch):
    monkeypatch.setenv("RCON_PASSWORD", "env-secret")
    yaml = """
    servers:
      - id: cod1
        name: CoD1
        systemd_unit: cod1.service
        rcon_password: ${RCON_PASSWORD}
    """
    p = tmp_path / "env.yaml"
    write_yaml(p, yaml)
    loader = ConfigLoader(path=p)
    servers = loader.load()
    assert len(servers) == 1
    assert servers[0].rcon_password == "env-secret"
