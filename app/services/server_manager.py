"""ServerManager: combine configuration, systemd state, and process stats.

This module implements ServerManager which is constructed with its
dependencies injected: a ConfigLoader instance, a systemd service helper, and
a ProcessStatsService. It provides methods to list all servers and fetch a
single server's runtime status. All failures are logged and isolated so a
problem with one server will not prevent reporting on others.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Optional

from app.models.server import ServerStatus, ServerConfig

logger = logging.getLogger(__name__)


class ServerManager:
    """Combine configuration, systemd, and process stats into ServerStatus objects.

    Dependencies are injected to keep this class testable and decoupled from
    concrete implementations.
    """

    def __init__(self, config_loader, systemd_service, process_stats_service) -> None:
        self.config_loader = config_loader
        self.systemd = systemd_service
        self.proc_stats = process_stats_service

    def get_servers(self) -> List[ServerStatus]:
        """Return the list of ServerStatus for all configured servers."""
        configs = []
        try:
            configs = self.config_loader.get_all()
        except Exception as exc:
            logger.exception("Failed to fetch server configs: %s", exc)
            return []

        statuses: List[ServerStatus] = []
        for cfg in configs:
            st = self._build_status(cfg)
            if st is not None:
                statuses.append(st)
        return statuses

    def get_server(self, server_id: str) -> Optional[ServerStatus]:
        """Return ServerStatus for a single server id, or None if not found."""
        try:
            cfg = self.config_loader.get(server_id)
        except Exception as exc:
            logger.exception("Failed to fetch server config for %s: %s", server_id, exc)
            return None

        if cfg is None:
            return None

        return self._build_status(cfg)

    def _build_status(self, cfg: ServerConfig) -> Optional[ServerStatus]:
        """Build a ServerStatus for a single ServerConfig. Never raises."""
        try:
            unit = getattr(cfg, "systemd_unit", None)
            active_state = None
            pid = None
            cpu_percent = None
            memory_mb = None
            started_at = None
            uptime = None

            if unit is None:
                status = "no_unit"
            else:
                try:
                    exists = self.systemd.unit_exists(unit)
                except Exception as exc:
                    logger.exception("systemd.unit_exists failed for %s: %s", unit, exc)
                    exists = False

                if not exists:
                    status = "unit_missing"
                else:
                    try:
                        active_state = self.systemd.get_active_state(unit)
                    except Exception as exc:
                        logger.exception("systemd.get_active_state failed for %s: %s", unit, exc)
                        active_state = None

                    try:
                        pid = self.systemd.get_main_pid(unit)
                    except Exception as exc:
                        logger.exception("systemd.get_main_pid failed for %s: %s", unit, exc)
                        pid = None

                    if pid is not None:
                        try:
                            ps = self.proc_stats.get_process_stats(pid)
                        except Exception as exc:
                            logger.exception("proc_stats.get_process_stats failed for pid=%s: %s", pid, exc)
                            ps = None

                        if ps is not None:
                            cpu_percent = ps.cpu_percent
                            memory_mb = ps.memory_mb
                            if ps.create_time:
                                try:
                                    started_at = datetime.fromtimestamp(ps.create_time)
                                except Exception:
                                    started_at = None
                            uptime = ps.uptime_seconds

                    # Decide status based on active_state / pid
                    if active_state == "active":
                        status = "running"
                    elif pid is not None:
                        status = "running"
                    else:
                        status = "offline"

            server_status = ServerStatus(
                id=cfg.id,
                name=cfg.name,
                type=getattr(cfg, "type", None),
                status=status,
                active_state=active_state,
                pid=pid,
                uptime=(f"{int(uptime)}s" if uptime is not None else None),
                started_at=started_at,
                cpu_percent=cpu_percent,
                memory_mb=memory_mb,
            )
            return server_status
        except Exception as exc:
            logger.exception("Failed to build status for server %s: %s", getattr(cfg, "id", None), exc)
            return None
