"""
Utility file to extract metadata from a video.
"""

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from engine.downloader.utils.video_info import VideoInfo
from engine.downloader.utils.format_title import format_title
from config import SHOW_YT_DLP_OUTPUT


def extract_info(url: str):
    """Try to extract info, return None if the video is unavailable"""

    try:
        info = YoutubeDL({"quiet": not SHOW_YT_DLP_OUTPUT}).extract_info(
            url=url, download=False)
    except DownloadError:
        # if the video is unavailable, we'll just skip it
        return None

    # get the info we need
    try:
        title = info["title"]
    except KeyError:
        title = ""
    try:
        thumbnail = info["thumbnail"]
    except KeyError:
        thumbnail = ""
    try:
        duration = info["duration"]
    except KeyError:
        duration = -1

    title = format_title(title)
    return VideoInfo(title=title, duration=duration, url=url, thumbnail=thumbnail)
