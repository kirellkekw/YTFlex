from fastapi import FastAPI
import asyncio
from engine.api_handler.side_processes.base import *
from engine.downloader.base import *
from config import download_path, show_yt_dlp_output, max_file_size, ip_or_domain, res_list


app = FastAPI()


@app.on_event("startup")  # run this function when the server starts
async def startup_event():
    asyncio.create_task(purge_old_files())


@app.get("/root")
async def root():
    # to check if the server is running without much hassle
    # can't go wrong with a hello world
    return {"message": "Hello World"}


@app.get("/download/audio")
async def audio_download(link: str):
    link = link.split(",")
    raw_dl_info = download_audios(urls=link, download_directory=download_path,
                                  show_output=show_yt_dlp_output, max_file_size=max_file_size, ip_or_domain=ip_or_domain)

    return raw_dl_info


@app.get("/download/video")
async def video_download(link: str, res: int):
    link = link.split(",")
    raw_dl_info = download_videos(urls=link, preferred_res=res, download_directory=download_path,
                                  show_output=show_yt_dlp_output, max_file_size=max_file_size, ip_or_domain=ip_or_domain, res_list=res_list)

    return raw_dl_info
