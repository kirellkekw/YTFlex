# YTFlex

[![Pylint](https://github.com/kirellkekw/YTFlex/actions/workflows/pylint.yml/badge.svg)](https://github.com/kirellkekw/YTFlex/actions/workflows/pylint.yml)

Deployment ready, easy to use and fast YouTube downloader API written in Python with CDN setup guide.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Nix](https://img.shields.io/badge/NIX-5277C3.svg?style=for-the-badge&logo=NixOS&logoColor=white)

and ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) soon!

# Installation

## 1- Download the dependencies

* Docker
* Nginx

For detailed instructions on how to install those, please refer to the following links:

* [Docker Install Guide](https://docs.docker.com/engine/install/)
* [Nginx Install Guide](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)

## 2- Download the repository and configure the settings

### 2.1- Clone the repository and move into the directory

* You need to have git installed on your machine to do this, but you can also download the repository as a zip file and extract it to skip this step.

```bash
git clone https://github.com/kirellkekw/YTFlex.git
cd YTFlex
```

### 2.2- Configure the settings

* Open the `config.yaml` file and change the settings according to your needs with your favorite text editor. Here's a quick explanation of what each setting does:

| Setting | Description | Default Value | Type |
| --- | --- | --- | --- |
| `res_list` | A list of resolutions API can attempt to download. | `[1080, 720, 480, 360, 240, 144]` | `list[int]` |
| `max_file_size` | The maximum file size in megabytes the API can download. | `100` | `int` |
| `download_path` | Path to the directory where the downloaded files will be stored. | `./downloads/` | `str` |
| `port` | The port the API server will listen on. | `2002` | `int` |
| `ip_or_domain` | The address API will use to create a CDN link. | `5.178.111.177` | `str` |
| `max_file_age` | Maximum age of a file in seconds before it gets deleted. | `3600` | `int` |
| `show_yt_dlp_output` | Decides if yt_dlp output is printed to the console or not. | `True` | `bool` |

## 3- Run the server with Docker

* Note: Tested on Podman backend, but should work with Docker as well.

### 3.1- Build the image

```bash
sudo docker build -t yt_api:1.0.0 . # including version number is optional, but recommended in case you want to update the image later
```

### 3.2- Run the image as a container

* Note: You need to change the `/designated/download/path/` to the path you want to download the files to.

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
   proxy_pass http://127.0.0.1:2002/;
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

***(in no particular order)***

***currently working on:***

* custom messages for different errors
* control block to prevent redownloading same files
* figuring out how pylint config works

***the rest:***

* [x] Add support for multiple file resolutions
* [x] Add option to limit the file size of the downloaded files
* [x] Add support for Docker for easier deployment
* [x] Add support for Nginx for reverse proxying and CDN
* [x] Add CDN support
* [x] Write a proper readme(ironic, isn't it?)
* [x] Add option to purge files after a certain amount of time
* [x] Add option to download mp3 files(this is actually easier than video files ~~,but i haven't gotten around to it yet~~)
* [x] Handle multiple file links more gracefully
* [x] Add graceful error handling for invalid links
* [x] Open source the project
* [x] Restructure the backend to be more modular
* [x] Add option to download playlists
* [x] Allow passing video or playlist id's as a parameter instead of a link
* [ ] Add a control block before downloads to prevent redownloading same files(this was broken, i'll fix it soon)
* [ ] Anonymize the file access links
* [ ] Add a frontend
* [ ] Create a special message if:
  * [x] The file is not available for download, or if the link is invalid
  * [ ] If the file is already downloaded and not expired
  * [ ] The file is too large
  * [ ] The file is too long
  * [ ] The file is not available in the requested resolution
* [ ] Add support to Postgres for:
  * [ ] Logging downloads
  * [ ] Logging errors
  * [ ] Logging file purges
  * [ ] Adding API key support for uncapped file size and higher resolution
  * [ ] Adding option to choose when a file will be purged to user
  * [ ] Adding a mechanism to limit the number of concurrent downloads per IP to prevent abuse
