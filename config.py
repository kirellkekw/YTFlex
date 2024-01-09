# add more values to provide more options, or remove some to provide less options
res_list: list[int] = [1080, 720, 480, 360, 240, 144]

# in megabytes, if a resolution is not available by this limitation, it will download the next best resolution
filesize_limit: int = 100

# the directory to download the videos to in container
download_directory: str = "/softdisk/beer/cdn_root/"

# the port to run the server on
port = 2002
