"""
Entry point for the project.
"""

import uvicorn
from config import PORT


if __name__ == "__main__":
    uvicorn.run("engine.api_handler.app:app", host="0.0.0.0", port=PORT,
                loop="asyncio")
