from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.config_loader import config_loader
from app.services.game_content_service import GameContentService
from app.services.server_service import ServerService

router = APIRouter(
    prefix="/server",
    tags=["Server"],
)


@router.get("/status")
async def status():
    return ServerService.status()


@router.post("/start")
async def start():
    return ServerService.start()


@router.post("/stop")
async def stop():
    return ServerService.stop()


@router.post("/restart")
async def restart():
    return ServerService.restart()


@router.get("/{server_id}/maps")
async def get_server_maps(server_id: str):
    """Get available maps for a specific server."""
    server = config_loader.get(server_id)

    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")

    server_path = Path(server.install_path) if server.install_path else None
    if not server_path:
        raise HTTPException(status_code=404, detail="Server path not configured")

    maps = GameContentService.get_maps(server_path)
    return maps
