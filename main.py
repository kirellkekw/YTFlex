"""
Entry point for the project.
"""

import uvicorn
import config


if __name__ == "__main__":
    port = config.get("PORT")
    root_path = config.get("ROOT_PATH", "/ytflex")

    uvicorn.run(
        "src.api_handler.app:app",
        host="0.0.0.0",  # listen on all interfaces, won't matter since it's running in a container
        port=port,  # check config.yaml for the port
        reload=False,  # reload when code changes, useful for development, disable otherwise
        log_level="debug",  # log level, "info" or "debug" recommended, "error" for production
        loop="asyncio",  # use asyncio event loop for sub-processes
        lifespan="on", # run startup and shutdown events, not really sure what this does
        root_path=root_path,  # root path for the API, useful for reverse proxies
    )
