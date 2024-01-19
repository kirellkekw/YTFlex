import os
import yt_dlp
from urllib.parse import quote


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


def format_the_title(title: str, remove_spaces: bool = False):
    """
    Formats the title to be suitable for filenames
    title: the string to format
    remove_spaces: whether to remove spaces from the title or not, will be replaced with underscores
    """
    # not adding these three lines are a great way learn from mistakes, trust me
    title = title.replace(':', '')
    title = title.replace("\\", '')
    title = title.replace("/", '')

    # luckily spaces are allowed in filenames, but i'll leave the choice to you
    if remove_spaces:
        title = title.replace(" ", "_")

    # cyrillic characters work fine, but for the sake of consistency, we'll replace them with latin characters
    # might remove this in the future depending on how much of a pain it is to deal with
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


def file_exists(file_address: str, download_path: str = "./downloads"):
    """Checks if the file exists in the download directory. Returns the filename if it does, False if it doesn't"""
    # not the most efficient way, but it works
    for file in os.listdir(download_path):
        # check if the file exists without the extension
        if file.startswith(file_address + "."):
            print(f"File already exists, name: {file}")
            return file
    return False


def extract_info(show_output: bool, url: str):
    class ExtractedInfo:
        def __init__(self, title: str, thumbnail: str, duration: int):
            self.title = title
            self.thumbnail = thumbnail
            self.duration = duration
    """Try to extract info, return None if the video is unavailable"""
    try:
        info = yt_dlp.YoutubeDL({"quiet": not show_output}).extract_info(
            url=url, download=False)
    except yt_dlp.utils.DownloadError:
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

    title = format_the_title(title)
    return ExtractedInfo(title, thumbnail, duration)


def create_download_link(ip_or_domain: str, filename: str):
    """
    Creates a download link for the file
    ip_or_domain: the ip or domain of the server
    filename: FULL filename of the file, including the extension
    """
    return f"http://{ip_or_domain}/cdn/{quote(filename)}"


def create_response_object(link: str, title: str, thumbnail: str, filename: str, duration: int, already_downloaded: bool, resolution: int | None = None):
    """
    Creates a response object for the client
    resolution: the resolution of the file, if it's audio, it'll be None
    link: the download link of the file
    title: the title of the file
    thumbnail: the thumbnail of the file
    duration: the duration of the file
    filename: the filename of the file
    already_downloaded: whether the file was already downloaded or not
    """

    if already_downloaded:
        message = "File is already downloaded"
    else:
        message = f"File has been downloaded successfully"

    response = [
        {
            "link": link,
            "message": message,
            "metadata": {
                "title": title,
                "duration": duration,
                "thumbnail": thumbnail,
                "already_downloaded": already_downloaded,
                "filename": filename,
                "extension": os.path.splitext(filename)[1]
            }
        }
    ]
    if isinstance(resolution, int):
        response[0]["metadata"]["resolution"] = resolution

    return response


def parse_playlist(link: str):
    """Parses the playlist and returns a list of VideoInfo objects"""
    print("Parsing playlist...")
    class VideoInfo:
        def __init__(self, title: str, duration: int, url: str, thumbnail: str, success: bool = True):
            self.url = url
            self.title = title
            self.duration = duration
            self.thumbnail = thumbnail
            self.success = success

    parsed_data: list[VideoInfo] = []
    try:
        data = yt_dlp.YoutubeDL().extract_info(link, download=False)
        for index in range(len(data["entries"])):
            try:
                title = data["entries"][index]["title"]
                duration = data["entries"][index]["duration"]
                vid_link = data["entries"][index]["webpage_url"]
                thumbnail = data["entries"][index]["thumbnail"]
                success = True
            except KeyError:
                title = ""
                duration = ""
                vid_link = ""
                thumbnail = ""
                success = False
            parsed_data.append(
                VideoInfo(title, duration, vid_link, thumbnail, success))
    except yt_dlp.utils.DownloadError:
        return []
    return parsed_data

# test zone
if __name__ == "__main__":
    link = "https://www.youtube.com/playlist?list=PLqVvJJMWXY-VcWIDeePQXkA54Ehj8dy1X"
    parsed_data = parse_playlist(link)
    import jsonpickle
    print(jsonpickle.encode(parsed_data, indent=4))
