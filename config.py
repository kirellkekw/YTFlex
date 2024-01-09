
# add common resolutions here as you see fit in descending order
res_list: list[int] = [1080, 720, 480, 360, 240, 144]

# in megabytes. if a resolution is not available by this limitation, it will download the next best resolution
# this only limits the filesize of the video, not the audio.
# so if a video is 97mb and audio is 5mb, the video will be 102mb and will be downloaded anyway
filesize_limit: int = 100

# the directory to download the videos to in container(should be the same as the one in nginx for CDN)
download_directory: str = "./downloads"

# the port to run the server on(should be the same as the one in nginx)
port = 2002

# the ip or domain to run the server on(should be the same as the one in nginx)
ip_or_domain = "5.178.111.177"

max_file_age = 3600  # in seconds
