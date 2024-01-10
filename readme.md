# YTFlex
<div>
<img src="https://cdn.discordapp.com/attachments/889091145349623848/1193330729157922977/IMG_6589.png?ex=65ac52d8&is=6599ddd8&hm=7484a7c3b209a61d041556ba205946d5a4de355a8d0f715f01bdcc4151816250&" alt="yt_api" style="width: 300px;align:center;" />
</div>

# Description
A simple API that downloads youtube videos to a server and returns a link to the video.

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

* Python 3.11 (or higher)
* FFmpeg
* Docker
* Nginx


For detailed instructions on how to install those, please refer to the following links:

- [Python Downloads](https://www.python.org/downloads/)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)
- [Docker Install Guide](https://docs.docker.com/engine/install/)
- [Nginx Install Guide](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)


## 2- Clone the repository and move into it

```bash
git clone https://github.com/kirellkekw/yt_api.git"
cd yt_api
```

## 3- Install the dependencies
### 3.1- Create a virtual environment and install the dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3.1(alternative)- Or, simply download the dependencies without creating a virtual environment

```bash
pip install -r requirements.txt
```

## 4- Run the server

```bash
python main.py
```

* At this point, the download server should be running on port 2002 if not specified otherwise. Rest of the instructions assume that the server is running on port 2002.

## 5- Run the server with Docker

- Note: Tested on Podman backend, but should work with Docker as well.

### 5.1- Build the image
```bash
sudo docker build -t yt_api:1.0.0 .
```

### 5.2- Run the image as a container
```bash
sudo docker run -d -p 2002:2002 -v /designated/download/path/:/downloads yt_api:1.0.0
```

### 6- Run the CDN server with Nginx

* We recommend using Nginx not only as CDN, but also as a reverse proxy for the API server. This will allow you to use a domain name instead of an IP address and also allow you to use HTTPS. This won't be covered in this guide, but you can find a lot of tutorials online on how to do this.
* This guide will expect you to have Nginx installed and running on your machine.

### 6.1- Create a new server block in your Nginx configuration file, usually located at `/etc/nginx/nginx.conf`
```nginx
# use your favorite text editor add the following to your nginx.conf as you see fit
events {}
http {
	server {
		listen 80; 
		server_name {your-ip-address};
	
		location /yt_api/ {
			proxy_pass http://your-ip-address:2002/; # add your ip address to here
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-Forwarded-Proto $scheme;
		}
		location /cdn/ {
			alias /designated/download/path/;
			expires 1h;
		}
	}
}
```

### 6.2- Restart Nginx
* The way you restart Nginx depends on your distro, this guide will assume you are using a systemd based distro.
```bash
sudo systemctl restart nginx
```

### 6.3- Test the server
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

- [x] Write a proper readme(kekw)
- [x] Add support for multiple file resolutions
- [x] Add option to limit the file size of the downloaded files
- [x] Add support for Docker
- [x] Add support for Nginx
- [x] Add CDN support
- [x] Add option to purge files after a certain amount of time
- [ ] Add support for Postgres for better scalability
- [ ] Anonymize the file access links
- [ ] Add option to download mp3 files
- [ ] Add option to download playlists
- [ ] Add API key support for uncapped file size and higher resolution
- [ ] Add option to choose when a file will be purged to user
- [ ] Add a frontend
- [ ] Add a mechanism to limit the number of concurrent downloads per IP to prevent abuse
