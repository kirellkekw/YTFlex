"""
Entry point for the project.
"""

import uvicorn
import config


if __name__ == "__main__":
    port = config.get("PORT")

    uvicorn.run(
        "engine.api_handler.app:app",
        host="0.0.0.0",  # listen on all interfaces, won't matter since it's running in a container
        port=port,  # check config.yaml for the port
        reload=True,  # reload the server when code changes,
        log_level="info",  # log level, change to "debug" for more verbose logging
        loop="asyncio"  # use asyncio event loop for sub-processes
    )
