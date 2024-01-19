import uvicorn
from config import port


if __name__ == "__main__":
    uvicorn.run("engine.api_handler.app:app", host="0.0.0.0", port=port,
                loop="asyncio")
