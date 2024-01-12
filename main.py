import uvicorn

from config import *


if __name__ == "__main__":
    uvicorn.run("engine.api_handle:app", host="localhost", port=port,
                loop="asyncio")
