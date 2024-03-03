"""
This file contains the FastAPI app and the routes for the API.
"""

import asyncio
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engine.api_handler.side_processes.base import purge_old_files
from engine.downloader.runner import download_files
import config


revision_hash = os.getenv("REV_HASH")

app = FastAPI()
origins = config.get("ALLOWED_DOMAINS")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


@app.on_event("startup")  # run this function when the server starts
async def startup_event():
    """Creates sub-processes to run in the background when the server starts."""
    asyncio.create_task(purge_old_files())


@app.get("/root")
async def root():
    """To check if the server is running without much hassle."""

    return {"message": "Hello World",
            "revision_hash": revision_hash[:7]}


@app.get("/download/audio")
async def audio_download(link: str):
    """API route for downloading audio files."""
    if "," in link:
        link = link.split(",")
    raw_dl_info = download_files(passed_urls=link, is_video_request=False)

    return raw_dl_info


@app.get("/download/video")
async def video_download(link: str, res: int, mp4: bool = False):
    """API route for downloading video files."""
    if "," in link:
        link = link.split(",")
    raw_dl_info = download_files(
        passed_urls=link, is_video_request=True, preferred_res=res, convert_to_mp4=mp4)

    return raw_dl_info
