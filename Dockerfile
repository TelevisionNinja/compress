FROM ubuntu:rolling

RUN apt-get update -y && apt-get install ffmpeg python3 -y

WORKDIR /compress
COPY ./ ./

ENTRYPOINT [ "python3", "/compress/src/compress.py" ]
