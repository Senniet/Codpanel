from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Dict, List
import logging
from functools import lru_cache

from app.services.server_manager import ServerManager
from app.services.process_stats import ProcessStatsService
from app.services import systemd_service as systemd_module
from app.config_loader import config_loader

logger = logging.getLogger(__name__)

router = APIRouter()


@lru_cache()
def get_server_manager() -> ServerManager:
    """Create (and cache) a ServerManager instance for DI.

    We keep construction here so the route does not instantiate the manager
    directly. Using lru_cache ensures we reuse the same instance across calls
    while still allowing tests to override the dependency.
    """
    return ServerManager(config_loader, systemd_module, ProcessStatsService())


@router.get("/server/status")
async def server_status(manager: ServerManager = Depends(get_server_manager)) -> Dict[str, Any]:
    """Return runtime status for all configured servers.

    Response envelope:
    {
        "success": true,
        "servers": [...]
    }

    On error:
    {
        "success": false,
        "error": "..."
    }
    """
    try:
        servers = manager.get_servers()
        # Convert Pydantic models to plain dicts (model_dump for Pydantic v2)
        def to_dict(s):
            if hasattr(s, "model_dump"):
                return s.model_dump()
            if hasattr(s, "dict"):
                return s.dict()
            return dict(s)

        return {"success": True, "servers": [to_dict(s) for s in servers]}
    except Exception:
        logger.exception("Failed to fetch server status")
        raise HTTPException(status_code=500, detail={"success": False, "error": "Internal server error"})
