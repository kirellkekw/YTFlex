from fastapi import FastAPI
import asyncio

from config import *
from engine.downloader import download_videos
from engine.purge_old_files import purge_old_files

app = FastAPI()


@app.get("/root")
async def root():
    # to check if the server is running without much hassle
    return {"message": "Hello World"}


@app.get("/download/audio")
async def audio_download(link: str):
    raw_dl_info = download_videos(
        urls=link, download_directory=download_path)

    return raw_dl_info


@app.get("/download/video")
async def video_download(link: str, res: int):
    raw_dl_info = download_videos(urls=link, preferred_res=res,
                                  download_directory=download_path)

    return raw_dl_info


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(purge_old_files())
