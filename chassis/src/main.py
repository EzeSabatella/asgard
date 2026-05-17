import uvicorn
from chassis.api.app import app
from chassis.config import get_config


if __name__ == "__main__":
    config = get_config()
    uvicorn.run(
        "chassis.api.app:app",
        host=config.api.host,
        port=config.api.port,
        reload=config.api.debug,
    )
