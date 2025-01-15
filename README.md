# compress
A python file and docker container to compress a video file down to a specific size

# Run

## Native
dependencies:
- python
- ffmpeg

```bash
python ./src/compress.py ./videos/example.mp4
```

## Docker or Podman

### Docker
```bash
docker build -t compress_image .
docker run --rm --privileged -v ./videos/:/compress/videos/ compress_image /compress/videos/example.mp4
```

### Podman
```bash
podman build -t compress_image .
podman run --rm --privileged -v ./videos/:/compress/videos/ compress_image /compress/videos/example.mp4
```
