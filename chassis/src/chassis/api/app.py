from fastapi import FastAPI
from chassis.config import get_config
from chassis.api.routes import turns, profile, proposals, health
from chassis.api.mcp import mcp_router

def create_app() -> FastAPI:
    config = get_config()
    app = FastAPI(
        title="Asgard Chassis",
        version=config.mcp.server_version,
        docs_url="/docs",
        redoc_url=None,
    )
    app.include_router(health.router)
    app.include_router(turns.router, prefix="/turns")
    app.include_router(profile.router, prefix="/profile")
    app.include_router(proposals.router, prefix="/proposals")
    app.include_router(mcp_router, prefix="/mcp")
    return app

app = create_app()
