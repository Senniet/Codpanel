from fastapi import APIRouter

# Aggregate sub-routers and expose them at both /api and /api/v1 so frontend can use either prefix.
# This file is intentionally placed in app/api/v1/ per repository structure requirements.

from . import auth, dashboard, servers

router = APIRouter()

# Register endpoints under both /api and /api/v1 prefixes to maximize compatibility with frontend expectations.
for prefix in ('/api', '/api/v1'):
    router.include_router(auth.router, prefix=prefix)
    router.include_router(dashboard.router, prefix=prefix)
    router.include_router(servers.router, prefix=prefix)
