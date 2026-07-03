from fastapi import APIRouter

# Aggregate sub-routers. These will be included in the main app under the /api/v1 prefix.

from . import auth, dashboard, servers

router = APIRouter()

router.include_router(auth.router)
router.include_router(dashboard.router)
router.include_router(servers.router)
