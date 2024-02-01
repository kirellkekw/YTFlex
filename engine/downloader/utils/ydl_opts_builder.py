"""
Utility function to build the options for yt-dlp.
"""

import os
from config import MAX_FILE_SIZE, DOWNLOAD_PATH, SHOW_YT_DLP_OUTPUT
from engine.downloader.utils.find_appropriate_res import find_appropriate_res


def ydl_opts_builder(
        title: str,
        is_video_request: bool,
        preferred_res: int = 720,
        convert_to_mp4: bool = False):
    """
    Utility function for building the options for yt-dlp.

    Args:
        title: The title of the file to download.

        is_video_request: Whether the request is for a video or audio file.

        preferred_res: The preferred resolution to download. Defaults to 720p.
        Not used if downloading audio only.

        convert_to_mp4: Whether to convert the downloaded file to mp4 or not. Defaults to False.
        Will have no effect if downloading audio only.

    """
    if is_video_request:
        # format string for yt-dlp
        preferred_res = find_appropriate_res(preferred_res)

        ydl_opts = {
            "format": f"bestvideo[height<={preferred_res}][filesize<{MAX_FILE_SIZE}M]+" +
            "bestaudio/best[height<={preferred_res}][filesize<{int(MAX_FILE_SIZE/4)}M]",

            "outtmpl": os.path.join(DOWNLOAD_PATH, f"{title}-%(height)sp.%(ext)s"),
            "windowsfilenames": True,
            "quiet": not SHOW_YT_DLP_OUTPUT,
        }

        if convert_to_mp4:
            ydl_opts["postprocessors"] = [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}]

    else:
        ydl_opts = {
            'format': f"bestaudio/best[filesize<{int(MAX_FILE_SIZE)}M]",
            "outtmpl": os.path.join(DOWNLOAD_PATH, f"{title}"),
            "windowsfilenames": True,
            "quiet": not SHOW_YT_DLP_OUTPUT,
            "postprocessors":
                [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3",
                    "preferredquality": "192"}],
        }

    return ydl_opts
