from fastapi import APIRouter
from chassis.config import get_config

router = APIRouter()

@router.get("/health")
async def health_check():
    config = get_config()
    return {
        "status": "ok",
        "version": config.mcp.server_version,
        "instance_type": config.instance.type
    }
