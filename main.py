from fastapi import FastAPI
import uvicorn
from downloader import download_vids
from config import *
import asyncio

from check_file_age import purge_old_files

app = FastAPI()


@app.get("/root")
async def root():
    return {"message": "Hello World"}


@app.get("/download")
async def get_download_link(link: str, res: int):
    raw_dl_info = download_vids(urls=link, preferred_res=res,
                                download_directory=download_directory)

    return raw_dl_info


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(purge_old_files())


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port,
                loop="asyncio")
