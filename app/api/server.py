from fastapi import APIRouter

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