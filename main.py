from fastapi import FastAPI
import uvicorn
from downloader import download_vids

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
                                download_directory="/softdisk/beer/cdn_root/")

    # not actually needed, but for future use when error handling is implemented
    dl_info = DownloadInfo(raw_dl_info)

    return dl_info

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2002)
