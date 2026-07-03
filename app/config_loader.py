"""Configuration loader for CodPanel servers.

This module provides ConfigLoader which loads server configurations from a YAML
file into typed ServerConfig objects and keeps them in memory. It supports
reloading and environment variable substitution.
"""
from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any, List, Optional

import yaml
from pydantic import ValidationError

from app.models.server import ServerConfig

logger = logging.getLogger(__name__)

_ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")


class ConfigLoader:
    """Loads and stores server configuration from a YAML file.

    The loader performs environment variable substitution for values of the
    form ${ENV_VAR}. The parsed ServerConfig objects are kept in memory and can
    be reloaded using `reload()`.
    """

    def __init__(self, path: Optional[Path] = None) -> None:
        # Default to app/config/servers.yaml relative to this module file
        self._path = Path(path) if path is not None else Path(__file__).parent / "config" / "servers.yaml"
        self._servers: List[ServerConfig] = []
        self._loaded: bool = False

    def load(self) -> List[ServerConfig]:
        """Load the configuration file and return the list of parsed servers."""
        if not self._path.exists():
            logger.warning("Server configuration file not found: %s", self._path)
            self._servers = []
            self._loaded = True
            return self._servers

        try:
            with self._path.open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
        except Exception as exc:  # yaml errors, permission errors, etc.
            logger.exception("Failed to read server config %s: %s", self._path, exc)
            self._servers = []
            self._loaded = True
            return self._servers

        raw_servers = data.get("servers") if isinstance(data, dict) else None
        if not raw_servers:
            logger.info("No servers configured in %s", self._path)
            self._servers = []
            self._loaded = True
            return self._servers

        parsed: List[ServerConfig] = []
        for idx, entry in enumerate(raw_servers):
            if not isinstance(entry, dict):
                logger.warning("Skipping invalid server entry at index %d: not a mapping", idx)
                continue

            try:
                substituted = self._substitute_env(entry)
                # Pydantic v2: use model_validate
                server = ServerConfig.model_validate(substituted)
                parsed.append(server)
            except ValidationError as ve:
                server_id = entry.get("id") if isinstance(entry, dict) else None
                logger.warning(
                    "Server config validation failed for id=%s index=%d: %s",
                    server_id,
                    idx,
                    ve,
                )
            except Exception as e:
                server_id = entry.get("id") if isinstance(entry, dict) else None
                logger.exception("Unexpected error parsing server id=%s index=%d: %s", server_id, idx, e)

        self._servers = parsed
        self._loaded = True
        logger.info("Loaded %d server(s) from %s", len(self._servers), self._path)
        return self._servers

    def reload(self) -> List[ServerConfig]:
        """Reload the configuration from disk and return the new server list."""
        return self.load()

    def get_all(self) -> List[ServerConfig]:
        """Return the in-memory list of ServerConfig objects."""
        return list(self._servers)

    def get(self, server_id: str) -> Optional[ServerConfig]:
        """Return a ServerConfig by id or None if not found."""
        for s in self._servers:
            if s.id == server_id:
                return s
        return None

    def _substitute_env(self, value: Any) -> Any:
        """Recursively substitute environment variables in the provided value."""
        if isinstance(value, dict):
            return {k: self._substitute_env(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._substitute_env(v) for v in value]
        if isinstance(value, str):
            def _repl(match: re.Match) -> str:
                env_name = match.group(1)
                return os.environ.get(env_name, "")
            return _ENV_PATTERN.sub(_repl, value)
        return value


# Module-level loader instance used by the application. Importing this module
# does not perform I/O; the application must explicitly call config_loader.load()
config_loader = ConfigLoader()
