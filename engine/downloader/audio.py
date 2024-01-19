import os
import yt_dlp
from engine.downloader.utils import *


def download_audios(urls: list[str] | str, download_directory: str = "./downloads", show_output: bool = True, max_file_size: int = 100, ip_or_domain: str = "localhost"):
    """
    Downloads audios from youtube using yt-dlp
    urls: list of urls to download, or a single url as a string. if you pass in a list, all of them will be downloaded
    download_directory: the directory to download the audio files to
    show_output: whether to print out the yt-dlp output or not
    max_file_size: the maximum filesize of the audio in megabytes
    ip_or_domain: the ip or domain of the server, used to generate the download link
    """

    is_playlist = False
    if isinstance(urls, str):
        # if it's a playlist, we'll just pass it to the playlist initializer
        if "playlist?list=" in urls:
            playlist_data = parse_playlist(urls)
            is_playlist = True
            if len(playlist_data) == 0:
                return {"message": "Given playlist link is either broken or unavailable."}
            urls = [video.url for video in playlist_data]
        else:
            urls = [urls]  # allows for single url to be passed in

    # this is the format string for yt-dlp
    # we'll just download the best audio quality available as long as it's not a gigantic file
    quality_str = f"bestaudio/best[filesize<{int(max_file_size)}M]"

    download_info = []
    for url in urls:  # Normally we can pass in a list of urls to yt-dlp, but we'll just loop through them instead for more control

        if is_playlist:
            # fetch from prefetched playlist data, no need to make another request
            if len(playlist_data) == 0:
                # this should never happen under normal circumstances
                # but if it does, we'll stop the loop by preempitvely returning
                return download_info
            current_video = playlist_data.pop(0)
            if not current_video.success:
                download_info += [{"link": "",
                                   "message": "Video is unavailable", "metadata": ""}]
                continue

            url = current_video.url
            title = current_video.title
            thumbnail = current_video.thumbnail
            duration = current_video.duration

        else:
            # we'll try to get the info about the video first, so we can format the title and check if file already exists
            info = extract_info(show_output, url)
            if info == None:  # if the video is unavailable, info will be None
                download_info += [{"link": "",
                                   "message": "Video is unavailable", "metadata": ""}]
                continue
            else:
                title = info.title
                thumbnail = info.thumbnail
                duration = info.duration

        # options for yt-dlp
        ydl_opts = {
            'format': quality_str,
            "outtmpl": os.path.join(download_directory, f"{title}"),
            "windowsfilenames": True,
            "quiet": not show_output,
            "postprocessors":
            [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3",
                "preferredquality": "192"}],
        }

        # check if the file already exists
        # if it does, we'll skip downloading it
        # we don't know the file extension yet, so we'll just check if the file exists without the extension
        # and if it does, we'll skip downloading it
        file = file_exists(title, download_directory)
        already_downloaded = False
        if file:
            # if the file exists, we'll just skip downloading it
            # and return the filename
            filename = os.path.basename(file)
            already_downloaded = True
        else:
            # download the audio
            # add a post processor to get the filename of the downloaded video
            filename_collector = FilenameCollectorPP()
            ydl = yt_dlp.YoutubeDL(ydl_opts)
            ydl.add_post_processor(filename_collector)
            ydl.download([url])
            last_downloaded_dir = filename_collector.filenames[-1]
            filename: str = os.path.basename(last_downloaded_dir)

        # encode the url with special characters to prevent errors
        download_link = create_download_link(ip_or_domain, filename)
        download_info += create_response_object(link=download_link, title=title,
                                                duration=duration, thumbnail=thumbnail, already_downloaded=already_downloaded, filename=filename)

    return download_info  # return the info about the downloaded audios for api to process


if __name__ == "__main__":
    # test to download the rick roll
    import jsonpickle

    a = download_audios(
        ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "https://www.youtube.com/watch?v=ub82Xb1C8os"])
    print(jsonpickle.encode(a, indent=4))
