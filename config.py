# the resolutions api can attempt to download. remove or add more common resolutions to your liking.
res_list: list[int] = [1080, 720, 480, 360, 240, 144]

# in megabytes. if a resolution is not available by this limitation, it will download the next best resolution.
# this only limits the filesize of the video, not the audio.
# so if a video is 97mb and audio is 5mb, the video will be 102mb and will be downloaded anyway.
max_file_size: int = 100

# the directory to download the videos to(should be synced across nginx and docker run command), or it won't work.
download_path: str = "./downloads"

# the port to run the server on(should be synced across nginx and docker run command), or it won't work.
port = 2002

# the ip to run the API server on(should be the same as the one in nginx), or it may not work.
ip_or_domain = "5.178.111.177"

# in seconds, 3600 = 1 hour, 86400 = 1 day, 604800 = 1 week, 2592000 = 1 month
max_file_age = 3600

# sets if download jobs should be silent or not. if set to False, the download will be run in silent mode.
show_yt_dlp_output = True
