"""
FFMPEG Python Helper - A Python wrapper for FFMPEG video processing.

This package provides a simple, intuitive API for common video processing tasks
including format conversion, GIF creation, video trimming, audio extraction,
in-memory processing, and data pipeline utilities.

Example:
    >>> from ffmpeg_python_helper import FFMPEG, Pipe
    >>> ffmpeg = FFMPEG()
    >>> ffmpeg.reformat("input.mp4", "output.avi")
    >>> ffmpeg.gif("video.mp4", "animation.gif", fps=15, scale=480)
    >>> ffmpeg.trim("video.mp4", "short_clip.mp4", start=10.5, duration=5.0)
    >>> ffmpeg.extract_audio("video.mp4", "audio.m4a")
    >>> 
    >>> # In-memory processing
    >>> with open("video.mp4", "rb") as f:
    ...     video_data = f.read()
    >>> gif_data = ffmpeg.gifs(video_data, fps=15, scale=480)
    >>> trimmed_data = ffmpeg.trims(video_data, start=0, duration=30)
    >>> audio_data = ffmpeg.extract_audios(video_data, output_format="m4a")
    >>> 
    >>> # Pipeline processing
    >>> def process_video(data: bytes) -> bytes:
    ...     return ffmpeg.trims(data, start=0, duration=30)
    >>> 
    >>> def convert_to_gif(data: bytes) -> bytes:
    ...     return ffmpeg.gifs(data, fps=15, scale=480)
    >>> 
    >>> processed_data = Pipe.pipe_bytes(video_data, process_video, convert_to_gif)

For detailed API documentation, see:
    - FFMPEG class documentation
    - Pipe class documentation
    - README.md for usage examples and tutorials
"""

from .ffmpeg_api import FFMPEG
from .pipe_helper import Pipe
from .ffprobe_api import FFProbe
from .async_ffmpeg_api import AsyncFFMPEG

__all__ = [
    'FFMPEG',
    'Pipe',
    'FFProbe',
    'AsyncFFMPEG'
]

__version__ = "0.1.0"
__author__ = "marjon <marjongodito@gmanmi.com>"


def main() -> None:
    """
    Command-line entry point for the FFMPEG Python Helper.

    This function is called when the package is executed as a script.
    It demonstrates basic functionality by:
        1. Creating an FFMPEG instance
        2. Printing the path to the FFMPEG executable

    Example:
        $ python -m ffmpeg_python_helper
        FFMPEG executable found at: /usr/bin/ffmpeg

    Raises:
        FileNotFoundError: If FFMPEG is not found in PATH.
    """
    ffmpeg = FFMPEG()
    print(f"FFMPEG executable found at: {ffmpeg.executable}")
