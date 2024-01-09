import yt_dlp
import os
from urllib.parse import quote
from config import *


class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
    """
    A post processor that collects the filename of the downloaded video.
    Access the last downloaded filename by using:

    obj.filenames[-1]

    You might need to use os.path.basename() to get the actual filename if you've set a custom directory
    """

    def __init__(self):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []

    def run(self, information):
        self.filenames.append(information['filepath'])
        return [], information


def download_vids(urls: list[str] | str, preferred_res: str | int, download_directory: str = ".", be_silent: bool = False):
    """
    Downloads videos from youtube using yt-dlp
    urls: list of urls to download, or a single url as a string. if you pass in a list, the preferred_res will be applied to all of them
    preferred_res: the preferred resolution to download the videos in, for a list of supported resolutions, see res_list
    """

    if isinstance(preferred_res, str):
        # someone might have accidentally passed with p at the end
        # being the good dev we are, we'll just remove it
        preferred_res = preferred_res.replace('p', '')
        try:
            preferred_res = int(preferred_res)  # convert to int
        except ValueError:
            # i sincerely hope you know how resolutions work if you're reading this
            print("Resolution must be an integer")
            return

    if isinstance(urls, str):
        urls = [urls]  # allows for single url to be passed in

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

    def format_the_title(title: str):
        # hot tip: if you're on windows, colons and backslashes are not allowed in filenames
        # so we'll just remove them for our precious windows users
        title = title.replace(':', '')
        title = title.replace("\\", '')

        # if spaces in filenames are not your thing, uncomment this line, the url will be encoded anyway
        # title = title.replace(" ", "_")

        # cyrillic letters are often problematic in filenames and urls, so we'll just convert them to latin
        # got you covered russian bros
        def cyrillic_to_latin(text: str):
            """
            Replaces cyrillic letters in the passed string with latin letters
            """
            CYRILLIC_TO_LATIN_MAP = {
                'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
                'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
                'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
                'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
                'ы': 'y', 'э': 'e', 'ю': 'iu', 'я': 'ia'
            }
            return ''.join(CYRILLIC_TO_LATIN_MAP.get(char.lower(), char) for char in text)
        title = cyrillic_to_latin(title)

        return title

    # this is the format string for yt-dlp
    res_str = f"bestvideo[height<={preferred_res}][filesize<{filesize_limit}M]+bestaudio/best[height<={preferred_res}]"

    # options for yt-dlp
    # this took me longer than i'd like to admit to figure out
    ydl_opts = {
        "outtmpl": os.path.join(download_directory, f"{title}-%(height)sp.%(ext)s"),
        "windowsfilenames": True,
        "format": res_str,
        "quiet": be_silent
    }

    for url in urls:  # Normally we can pass in a list of urls to yt-dlp, but we'll just loop through them instead for more control
        # we'll get the info about the video first, so we can format the title properly
        info = yt_dlp.YoutubeDL({"quiet": be_silent}).extract_info(
            url=url, download=False)

        # get the info we need
        title = info["title"]
        thumbnail = info["thumbnail"]
        duration = info["duration"]

        # formatting right before downloading
        title = format_the_title(title)

        # check if the file already exists
        # if it does, we'll skip downloading it
        # we don't know the file extension yet, so we'll just check if the file exists without the extension
        # and if it does, we'll skip downloading it
        def file_exists(file_address):
            """Checks if the file exists in the download directory. Returns the filename if it does, False if it doesn't"""
            # not the most efficient way, but it works
            for file in os.listdir(download_directory):
                # check if the file exists without the extension
                if file.startswith(file_address + "."):
                    return file
            return False

        file = file_exists(title)

        if file:
            # if the file exists, we'll just skip downloading it
            # and return the filename
            filename = os.path.basename(filename)
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
        download_link = quote(f"http://{ip_or_domain}/cdn/{filename}")
        download_info = ({
            "link": download_link,
            "message": f"{title} has been downloaded successfully",
            "metadata": {"duration": duration, "thumbnail": thumbnail, "filename": filename, "title": title}})

    return download_info  # return the info about the downloaded videos for further use


if __name__ == "__main__":
    # wanna give it a try?
    download_vids("https://www.youtube.com/watch?v=_o8Qqfu1pwQ",
                  144, "./downloads")
