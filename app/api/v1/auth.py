from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me")
async def me():
    """Return a minimal auth status. This is a placeholder to ensure the
    endpoints are registered for the frontend; authentication is handled
    elsewhere in the application.
    """
    return {"authenticated": False, "user": None}


@router.post("/login")
async def login():
    """Placeholder login endpoint. The real implementation is out of scope
    for this change; keep a deterministic, safe response so the frontend
    routes resolve successfully.
    """
    return {"success": False, "message": "not_implemented"}
