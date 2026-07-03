from fastapi import APIRouter

from .server import router as server_router
from .servers import router as servers_router
from .auth import router as auth_router

router = APIRouter()

# Include all v1 sub-routers
router.include_router(server_router)
router.include_router(servers_router)
router.include_router(auth_router)
