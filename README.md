# compress
A python file and docker container to compress a video file down to a specific size

# Run

## Native
dependencies:
- python
- ffmpeg

With a specified path
```bash
python ./src/compress.py ./videos/example.mp4
```

With the default directory ```/compress/videos/```
```bash
python ./src/compress.py
```

## Docker or Podman

### Docker
Build the image
```bash
docker build -t compress_image .
```

Run the container with a specified path
```bash
docker run --rm --privileged -v ./videos/:/compress/videos/ compress_image /compress/videos/example.mp4
```

Run the container with the default directory ```/compress/videos/```
```bash
docker run --rm --privileged -v ./videos/:/compress/videos/ compress_image
```

### Podman
Build the image
```bash
podman build -t compress_image .
```

Run the container with a specified path
```bash
podman run --rm --privileged -v ./videos/:/compress/videos/ compress_image /compress/videos/example.mp4
```

Run the container with the default directory ```/compress/videos/```
```bash
podman run --rm --privileged -v ./videos/:/compress/videos/ compress_image
```
