"""Frontend-compatible servers endpoint.

Exposes GET /servers to return the response format expected by the frontend.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Dict
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
    """Construct and cache ServerManager for DI."""
    return ServerManager(config_loader, systemd_module, ProcessStatsService())


@router.get("/servers")
async def list_servers(manager: ServerManager = Depends(get_server_manager)) -> Dict[str, Any]:
    """Return all configured servers in frontend-compatible format.

    Response:
    {
        "success": true,
        "data": [...]
    }

    On error:
    HTTP 500
    {
        "detail": {
            "success": false,
            "error": "Internal server error"
        }
    }
    """
    try:
        servers = manager.get_servers()

        # Convert Pydantic models to plain dicts
        def to_dict(s):
            if hasattr(s, "model_dump"):
                return s.model_dump()
            if hasattr(s, "dict"):
                return s.dict()
            return dict(s)

        return {"success": True, "data": [to_dict(s) for s in servers]}
    except Exception:
        logger.exception("Failed to fetch servers")
        raise HTTPException(status_code=500, detail={"success": False, "error": "Internal server error"})
