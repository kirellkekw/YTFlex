# YTFlex
![GitHub license](https://img.shields.io/github/license/kirellkekw/YTFlex?style=for-the-badge)


<div>
<img src="https://cdn.discordapp.com/attachments/889091145349623848/1193330729157922977/IMG_6589.png?ex=65ac52d8&is=6599ddd8&hm=7484a7c3b209a61d041556ba205946d5a4de355a8d0f715f01bdcc4151816250&" alt="yt_api" style="width: 300px;align:center;" />
</div>

*a better image is required here, pull requests are welcome

# Description
Deployment ready, easy to use, and fast YouTube downloader API written in Python using FastAPI.


# Powered by:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Nix](https://img.shields.io/badge/NIX-5277C3.svg?style=for-the-badge&logo=NixOS&logoColor=white)

### and ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) soon!

# Installation

## 1- Download the dependencies

* FFmpeg
* Docker
* Nginx

For detailed instructions on how to install those, please refer to the following links:

- [FFmpeg Downloads](https://ffmpeg.org/download.html)
- [Docker Install Guide](https://docs.docker.com/engine/install/)
- [Nginx Install Guide](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)


## 2- Download the repository and configure the settings

### 2.1- Clone the repository and move into the directory

* You need to have git installed on your machine to do this, but you can also download the repository as a zip file and extract it to skip this step.

```bash
git clone https://github.com/kirellkekw/yt_api.git
cd yt_api
```

### 2.2- Configure the settings

* Open the `config.py` file and change the settings according to your needs with your favorite text editor. Here's a quick explanation of what each setting does:

| Setting | Description | Default Value | Type |
| --- | --- | --- | --- |
| `res_list` | A list of resolutions that API can attempt to download. | `[1080, 720, 480, 360, 240, 144]` | `list[int]` |
| `max_file_size` | The maximum file size in megabytes that the API can download. | `100` | `int` |
| `download_path` | The path to the directory where the downloaded files will be stored. | `./downloads/` | `str` |
| `port` | The port the API server will listen on. | `2002` | `int` |
| `ip_or_domain` | The IP address or domain name the API server will listen on. | `5.178.111.177` | `str` |
| `max_file_age` | The maximum age of a file in seconds before it gets deleted. | `3600` | `int` |


## 3- Run the server with Docker

- Note: Tested on Podman backend, but should work with Docker as well.

### 3.1- Build the image
```bash
sudo docker build -t yt_api:1.0.0 . # including version number is optional, but recommended in case you want to update the image later
```

### 3.2- Run the image as a container

- Note: You need to change the `/designated/download/path/` to the path you want to download the files to.

```bash
sudo docker run -d -p 2002:2002 -v /designated/download/path/:/downloads yt_api:1.0.0
```

## 4- Run the CDN server with Nginx

* We recommend using Nginx not only as CDN, but also as a reverse proxy for the API server. This will allow you to use a domain name instead of an IP address and also allow you to use HTTPS. This won't be covered in this guide, but you can find a lot of tutorials online on how to do this.
* This guide will expect you to have Nginx installed and running on your machine.

### 4.1- Create a new server block in your Nginx configuration file, usually located at `/etc/nginx/nginx.conf`
```nginx
# use your favorite text editor add the following to your nginx.conf as you see fit
events {}
http {
	server {
		listen 80; 
		server_name your-ip-address; # add your ip address to here, or your domain name if you have one
	
		location /yt_api/ {
			proxy_pass http://your-ip-address:2002/; # add your ip address to here
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-Forwarded-Proto $scheme;
		}
		location /cdn/ {
			alias /designated/download/path/; # change this to your download path
			expires 1h;
		}
	}
}
```

### 4.2- Restart Nginx
* The way you restart Nginx depends on your distro, this guide will assume you are using a systemd based distro.
```bash
sudo systemctl restart nginx
```

### 4.3- Test the server
Try to access the following URL in your browser:

`http://localhost/yt_api/root`

or if you're running it without a reverse proxy:

`http://localhost:2002/root`

If you get a JSON response with the following content, then you are good to go!
```json
{"message": "Hello World"}
```

# TODO 
### (in no particular order)

- [x] Add support for multiple file resolutions
- [x] Add option to limit the file size of the downloaded files
- [x] Add support for Docker for easier deployment
- [x] Add support for Nginx for reverse proxying and CDN
- [x] Add CDN support
- [x] Write a proper readme(ironic, isn't it?)
- [x] Add option to purge files after a certain amount of time
- [x] Add option to download mp3 files(this is actually easier than video files, but i haven't gotten around to it yet)
- [ ] Add support for Postgres for various database operations
- [ ] Anonymize the file access links
- [ ] Add option to download playlists
- [ ] Add API key support for uncapped file size and higher resolution
- [ ] Add option to choose when a file will be purged to user
- [ ] Add a frontend
- [ ] Add a mechanism to limit the number of concurrent downloads per IP to prevent abuse
