"""
This file contains all the configuration options for the API.
"""

# the resolutions api can attempt to download. remove or add more common resolutions to your liking.
RES_LIST: list[int] = [1080, 720, 480, 360, 240, 144]

# in megabytes. if a resolution is not available by this limitation,
# it will download the next best resolution.
# this only limits the filesize of the video, not the audio.
# so if a video is 97mb and audio is 5mb, the video will be 102mb and will be downloaded anyway.
# max audio file size is the same when downloading audio only.
MAX_FILE_SIZE: int = 100

# the directory to download the videos to.
# should be the same as the one in nginx and docker command, or it won't work.
DOWNLOAD_PATH: str = "./downloads"

# the port to run the API server on.
# should be the same as the one in nginx and docker command, or it won't work.
PORT: int = 2002

# the ip or domain to use when generating the download link.
# has no effect on nginx or docker command, but is used in the API message returned.
IP_OR_DOMAIN: str = "5.178.111.177"

# in seconds, 3600 = 1 hour, 86400 = 1 day, 604800 = 1 week, 2592000 = 1 month
MAX_FILE_AGE: int = 3600

# sets if download jobs should be silent or not.
# if set to false, the output from youtube-dl will not be shown.
SHOW_YT_DLP_OUTPUT: bool = True
