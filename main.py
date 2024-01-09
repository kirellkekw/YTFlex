from fastapi import FastAPI
import uvicorn
from downloader import download_vids
from config import *
import asyncio

from check_file_age import purge_old_files

app = FastAPI()


class DownloadInfo():  # download info model
    def __init__(self, info: dict):
        self.title = info['title']
        self.link = info['link']
        self.message = info['message']
        self.metadata = info['metadata']


@app.get("/root")
async def root():
    return {"message": "Hello World"}


@app.get("/download")
async def get_download_link(link: str, res: int):
    raw_dl_info = download_vids(urls=link, preferred_res=res,
                                download_directory=download_directory)

    # not actually needed, but for future use when error handling is implemented
    dl_info = DownloadInfo(raw_dl_info)

    return dl_info


async def side_process():
    while True:
        await asyncio.sleep(5)
        with open("info.txt", "w") as f:
            f.write("hello")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(purge_old_files())


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port,
                loop="asyncio")
