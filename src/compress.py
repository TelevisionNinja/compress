import sys
import os
import pathlib
import math
import platform


def main():
    if len(sys.argv) != 2:
        print("wrong args")
        return

    filePath = sys.argv[1]
    filePathCheck = pathlib.Path(filePath)

    sizeLimit = 10 # mb
    sizeLimitBytes = sizeLimit * 1024 * 1024 # to megabytes

    if not(filePathCheck.exists() and filePathCheck.is_file()):
        print("file / path invalid")
        return

    if filePathCheck.stat().st_size <= sizeLimitBytes and filePathCheck.suffix == "mp4": # binary not metric
        print("file size already small")
        return

    filePath = f"\"{filePathCheck.absolute()}\""
    durationCommand = f"ffprobe -i {filePath} -show_entries format=duration -v quiet -of csv=\"p=0\""
    seconds = float(os.popen(durationCommand).read())

    if seconds == 0 or math.isinf(seconds) or math.isnan(seconds):
        print("invalid duration")
        return

    outputName = "vid"
    outputExtension = "mp4"
    outputFileName = outputName + "." + outputExtension
    parentDirectory = filePathCheck.parent.absolute()
    outputFile = pathlib.Path(f"{parentDirectory}/{outputFileName}")
    if outputFile.exists():
        print("output file already exists")
        return

    audioBitrate = 128 # audio kb/s
    bitrate = sizeLimit * 8 # to megabits
    bitrate *= 1000 # to kilo bits
    audioSize = audioBitrate * seconds

    if bitrate > audioSize:
        bitrate -= audioSize # account for audio

    bitrate /= seconds
    bitrate = int(bitrate)

    isWindows = platform.system() == "Windows"

    while True:
        pass1 = f"ffmpeg -y -i {filePath} -c:v libx264 -b:v {bitrate}k -pass 1 -an -f null /dev/null"
        if isWindows:
            pass1 = f"ffmpeg -y -i {filePath} -c:v libx264 -b:v {bitrate}k -pass 1 -an -f null NUL"

        os.system(pass1)

        pass2 = f"ffmpeg -i {filePath} -c:v libx264 -b:v {bitrate}k -pass 2 -c:a aac -b:a {audioBitrate}k \"{outputFile.absolute()}\""
        os.system(pass2)
        outputFile = pathlib.Path(f"{parentDirectory}/{outputFileName}")

        if isWindows:
            os.remove(pathlib.Path(f"{parentDirectory}/ffmpeg2pass-0.log").absolute())
            os.remove(pathlib.Path(f"{parentDirectory}/ffmpeg2pass-0.log.mbtree").absolute())

        if outputFile.stat().st_size <= sizeLimitBytes: # binary not metric
            return

        bitrate *= sizeLimitBytes / outputFile.stat().st_size
        # bitrate *= 0.5 # an extra decay factor
        bitrate = int(bitrate)

        os.remove(outputFile.absolute())


if __name__ == "__main__":
    main()
