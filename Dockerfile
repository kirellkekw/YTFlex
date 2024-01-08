FROM python:3.10

RUN apt-get update

RUN apt-get install -y ffmpeg

COPY requirements.txt downloader.py main.py ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "./main.py"]
