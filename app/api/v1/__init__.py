from fastapi import APIRouter

from .server import router as server_router
from .auth import router as auth_router

router = APIRouter()

# Include sub-routers for v1 endpoints
router.include_router(server_router)
router.include_router(auth_router)
