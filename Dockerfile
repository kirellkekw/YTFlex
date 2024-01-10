FROM python:3.11

RUN apt-get update

RUN apt-get install -y ffmpeg

COPY requirements.txt downloader.py main.py check_file_age.py config.py ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "./main.py"]
