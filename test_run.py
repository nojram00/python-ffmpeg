from pathlib import Path
from ffmpeg_python_helper import FFMPEG

SAMPLE_VIDEO = Path.cwd() / "sample-vid/vid.mp4"
OUTPUT_VIDEO = Path.cwd() / "sample-vid/clip.mp4"
OUTPUT_GIF = Path.cwd() / "sample-vid/clip.gif"

def main():
    # stdout, stderr = FFMPEG.api().trim(str(SAMPLE_VIDEO), str(OUTPUT_VIDEO), start=59, duration=4.5)
    stdout, stderr = FFMPEG.api().gif(str(OUTPUT_VIDEO), str(OUTPUT_GIF))

    if stdout: print(stdout)
    else: print(stderr)

if __name__ == '__main__':
    main()