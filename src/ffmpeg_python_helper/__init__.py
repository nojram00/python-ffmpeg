from .ffmpeg_api import FFMPEG

__all__ = [
    'FFMPEG'
]

def main():
    ffmpeg = FFMPEG()
    print(ffmpeg.executable)
