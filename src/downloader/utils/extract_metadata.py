"""
Utility file to extract metadata from a video.
"""

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from src.downloader.utils.video_info import VideoInfo
import config


def extract_info(url: str):
    """Try to extract info, return None if the video is unavailable"""

    show_yt_dlp_output = config.get("SHOW_YT_DLP_OUTPUT")
    bgutil_provider_url = config.get("BGUTIL_PROVIDER_URL")

    ydl_opts = {
        "quiet": not show_yt_dlp_output,
        "extractor_args": {
            "youtube": {"player_client": ["web_embedded"]},
            "youtubepot-bgutilhttp": {"base_url": [bgutil_provider_url]},
        },
        "remote_components": ["ejs:github"],
    }

    try:
        info = YoutubeDL(ydl_opts).extract_info(url=url, download=False)
    except DownloadError:
        # if the video is unavailable, we'll just skip it
        return None

    # get the info we need
    try:
        title = info["title"]
        # SECURITY: DO NOT REMOVE. This line is the ONLY defense against path
        # traversal via a crafted video title (e.g. a title containing "../../").
        # ydl_opts_builder.py inserts this title directly into the outtmpl
        # TEMPLATE STRING (an f-string), before yt-dlp ever parses it - so
        # yt-dlp's own field sanitization (e.g. "windowsfilenames") never runs
        # on it, since that only sanitizes %(field)s substitutions, not literal
        # text already baked into the template. Confirmed by direct test: without
        # this line, a title like "../../../etc/passwd" writes outside the
        # download folder. Removing this line reopens that hole. See runner.py's
        # DOWNLOAD_ROOT containment check for the (secondary, backstop) defense.
        title = title.replace("/", "-")
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

    return VideoInfo(title=title, duration=duration, url=url, thumbnail=thumbnail)
