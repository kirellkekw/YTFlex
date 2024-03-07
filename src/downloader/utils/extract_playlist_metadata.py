"""
Utility function to parse a playlist and return a list of VideoInfo objects(see below).
"""

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import config
from src.downloader.utils.video_info import VideoInfo


def parse_playlist(link: str):
    """Parses the playlist and returns a list of VideoInfo objects"""

    show_yt_dlp_output = config.get("SHOW_YT_DLP_OUTPUT")

    parsed_data: list[VideoInfo] = []
    try:
        data = YoutubeDL({"quiet": not show_yt_dlp_output}).extract_info(
            link, download=False
        )
        for index in range(len(data["entries"])):
            try:
                title = data["entries"][index]["title"]
                duration = data["entries"][index]["duration"]
                vid_link = data["entries"][index]["webpage_url"]
                thumbnail = data["entries"][index]["thumbnail"]
                parsed_data.append(VideoInfo(title, duration, vid_link, thumbnail))
            except KeyError:
                # if the video is unavailable, we'll just skip it
                parsed_data.append(None)
    except DownloadError:
        return []
    return parsed_data
