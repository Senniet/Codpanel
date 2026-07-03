from fastapi import APIRouter

from app.services.system_service import SystemService

router = APIRouter()


@router.get("/system")
async def system():

    return SystemService.get_system_info()
