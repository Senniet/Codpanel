import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import server
from app.api import system
from app.api.v1 import router as api_v1_router
from app.config_loader import config_loader


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load server configuration once during application startup. The loader
    # keeps the parsed servers in memory and supports reload() for future use.
    try:
        config_loader.load()
    except Exception:
        # Config loader handles its own errors and logs; safeguard here so the
        # lifespan does not raise and prevent the app from starting.
        pass
    yield


app = FastAPI(
    title="CodPanel",
    version="0.2.0",
    docs_url="/api/docs",
    redoc_url=None,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Register the API v1 endpoints first so they take precedence over legacy routes
app.include_router(
    api_v1_router,
    prefix="/api/v1",
    tags=["APIv1"],
)

app.include_router(
    system.router,
    prefix="/api/v1",
    tags=["System"],
)

app.include_router(
    server.router,
    prefix="/api/v1",
    tags=["Server"],
)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "title": "CodPanel",
            "version": app.version,
        },
    )


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "version": app.version,
    }
