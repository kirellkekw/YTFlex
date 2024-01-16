import uvicorn

from config import port


if __name__ == "__main__":
    uvicorn.run("engine.api_handle:app", host="localhost", port=port,
                loop="asyncio")
