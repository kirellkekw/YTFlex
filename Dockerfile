FROM python:3.11

WORKDIR /app

COPY . ./

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "./main.py"]
