import os
import yt_dlp
from engine.downloader.utils import *


def download_videos(urls: list[str] | str, preferred_res: str | int = 720, download_directory: str = "./downloads", show_output: bool = True, max_file_size: int = 100, ip_or_domain: str = "localhost", res_list: list[int] = [1080, 720, 480, 360, 240, 144]):
    """
    Downloads videos from youtube using yt-dlp
    urls: list of urls to download, or a single url as a string. if you pass in a list, the preferred_res will be applied to all of them
    preferred_res: the preferred resolution to download the videos in, for a list of supported resolutions, see res_list
    show_output: whether to print out the yt-dlp output or not
    max_file_size: the maximum filesize of the video in megabytes
    ip_or_domain: the ip or domain of the server, used to generate the download link
    res_list: the list of resolutions to choose from.
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

    if isinstance(preferred_res, str):
        # someone might have accidentally passed with p at the end
        # being the good dev we are, we'll just remove it
        preferred_res = preferred_res.replace('p', '')
        try:
            preferred_res = int(preferred_res)  # convert to int
        except ValueError:
            # i sincerely hope you know how resolutions and integers work if you're reading this
            print("Resolution must be an integer")
            return

    if preferred_res not in res_list:
        # find a resolution that is lower than the preferred resolution
        for res in res_list:
            if preferred_res > res:
                preferred_res = res
                break
        # i really hope you're not desperate enough to download 144p
        # but if you are, here you go
        if preferred_res < res_list[-1]:
            preferred_res = res_list[-1]

    # this is the format string for yt-dlp
    res_str = f"bestvideo[height<={preferred_res}][filesize<{max_file_size}M]+bestaudio/best[height<={preferred_res}][filesize<{int(max_file_size/5)}M]"

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
            if info == None:
                download_info += [{"link": "",
                                   "message": "Video is unavailable", "metadata": ""}]
                continue
            else:
                title = info.title
                thumbnail = info.thumbnail
                duration = info.duration

        # options for yt-dlp
        # this took me longer than i'd like to admit to figure out
        ydl_opts = {
            "outtmpl": os.path.join(download_directory, f"{title}-%(height)sp.%(ext)s"),
            "windowsfilenames": True,
            "format": res_str,
            "quiet": not show_output,
            "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        }

        # check if the file already exists
        # if it does, we'll skip downloading it
        # we don't know the file extension yet, so we'll just check if the file exists without the extension
        # and if it does, we'll skip downloading it
        file = file_exists(title+"-"+str(preferred_res)+"p")
        already_downloaded = False

        if file:
            # if the file exists, we'll just skip downloading it
            # and return the filename
            filename = os.path.basename(file)
            already_downloaded = True
        else:
            # download the video
            # add a post processor to get the filename of the downloaded video
            filename_collector = FilenameCollectorPP()
            ydl = yt_dlp.YoutubeDL(ydl_opts)
            ydl.add_post_processor(filename_collector)
            ydl.download([url])
            last_downloaded_dir = filename_collector.filenames[-1]
            filename: str = os.path.basename(last_downloaded_dir)

        # encode the url with special characters to prevent errors
        download_link = create_download_link(ip_or_domain, filename)
        # create the response object with explicit arguments
        download_info += create_response_object(link=download_link, title=title, thumbnail=thumbnail,
                                                filename=filename, duration=duration, already_downloaded=already_downloaded, resolution=preferred_res)

    return download_info  # return the info about the downloaded videos for api to process


if __name__ == "__main__":
    # test to download rick roll
    import jsonpickle

    a = download_videos(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ", preferred_res=144)
    print(jsonpickle.encode(a, indent=4))
