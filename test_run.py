from pathlib import Path
from ffmpeg_python_helper import FFMPEG, Pipe

SAMPLE_VIDEO = Path.cwd() / "sample-vid/vid.mp4"
OUTPUT_VIDEO = Path.cwd() / "sample-vid/clip.mp4"
OUTPUT_GIF = Path.cwd() / "sample-vid/clip.gif"

def main():

    if SAMPLE_VIDEO.exists():
        with SAMPLE_VIDEO.open('rb') as video:
            output = Pipe.pipe_bytes(
                video.read(),
                lambda b: FFMPEG.api().trims(input_bytes=b, start=59, duration=4.5),
                lambda b: FFMPEG.api().gifs(input_bytes=b) 
            )
            # b = video.read()
            # trimmed = FFMPEG.api().trims(input_bytes=b, start=59, duration=4.5)
            # output = FFMPEG.api().gifs(input_bytes=trimmed)

        with (Path.cwd() / "sample-vid/clip-02.gif").open('wb') as file:
            file.write(output)


    # FFMPEG.api().trim(str(SAMPLE_VIDEO), str(OUTPUT_VIDEO), start=59, duration=4.5)
    # FFMPEG.api().gif(str(OUTPUT_VIDEO), str(OUTPUT_GIF))

if __name__ == '__main__':
    main()