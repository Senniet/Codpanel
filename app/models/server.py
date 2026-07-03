from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ServerConfig(BaseModel):
    """Configuration for a managed server loaded from YAML.

    Fields are intentionally generic so different game adapters can be added later.
    """

    id: str
    name: str
    type: Optional[str] = None
    systemd_unit: str
    install_path: Optional[str] = None
    executable: Optional[str] = None
    config_path: Optional[str] = None
    rcon_host: Optional[str] = None
    rcon_port: Optional[int] = None
    rcon_password: Optional[str] = None


class ServerStatus(BaseModel):
    """Runtime status information for a configured server."""

    id: str
    name: str
    type: Optional[str] = None
    status: str
    active_state: Optional[str] = None
    pid: Optional[int] = None
    uptime: Optional[str] = None
    started_at: Optional[datetime] = None
    cpu_percent: Optional[float] = None
    memory_mb: Optional[float] = None
    players: Optional[int] = None
    max_players: Optional[int] = None
    map: Optional[str] = None
    version: Optional[str] = None

