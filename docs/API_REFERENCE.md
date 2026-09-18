# FFMPEG Python Helper API Reference

## Module: `ffmpeg_python_helper`

Version: 0.1.0
Author: marjon <marjongodito@gmanmi.com>

### Module Documentation
```python

FFMPEG Python Helper - A Python wrapper for FFMPEG video processing.

This package provides a simple, intuitive API for common video processing tasks
including format conversion, GIF creation, and video trimming.

Example:
    >>> from ffmpeg_python_helper import FFMPEG
    >>> ffmpeg = FFMPEG()
    >>> ffmpeg.reformat("input.mp4", "output.avi")
    >>> ffmpeg.gif("video.mp4", "animation.gif", fps=15, scale=480)
    >>> ffmpeg.trim("video.mp4", "short_clip.mp4", start=10.5, duration=5.0)

For detailed API documentation, see:
    - FFMPEG class documentation
    - README.md for usage examples and tutorials

```

## Class: `FFMPEG`

### Class Documentation
```python

A Python wrapper for FFMPEG that provides a simple, intuitive API for
common video processing tasks.

This class automatically detects FFMPEG installation in the system PATH
and provides methods for video conversion, GIF creation, and video trimming.

Example:
    >>> from ffmpeg_python_helper import FFMPEG
    >>> ffmpeg = FFMPEG()
    >>> ffmpeg.reformat("input.mp4", "output.avi")
    >>> ffmpeg.gif("video.mp4", "animation.gif", fps=15, scale=480)
    >>> ffmpeg.trim("video.mp4", "short_clip.mp4", start=10.5, duration=5.0)

Attributes:
    executable (str): The path to the FFMPEG executable found in the system PATH.

```

### Constructor
```python

Initialize a new FFMPEG instance.

Automatically searches for FFMPEG in the system PATH.

Raises:
    FileNotFoundError: If FFMPEG is not found in the system PATH.

Example:
    >>> try:
    ...     ffmpeg = FFMPEG()
    ...     print(f"FFMPEG found at: {ffmpeg.executable}")
    ... except FileNotFoundError as e:
    ...     print(f"FFMPEG not found: {e}")

```

### Class Methods
#### `FFMPEG.api()`
```python

Factory method that returns a new FFMPEG instance.

Returns:
    FFMPEG: A new instance of the FFMPEG class.

Example:
    >>> ffmpeg = FFMPEG.api()
    >>> ffmpeg.execute("-version")

```

### Instance Methods
#### `execute(*args: str)`
```python

Execute raw FFMPEG commands with the given arguments.

This method allows you to run any FFMPEG command directly,
providing maximum flexibility for operations not covered
by the built-in methods.

Args:
    *args: FFMPEG command-line arguments as strings.

Returns:
    tuple[str, str]: A tuple containing (stdout, stderr) from FFMPEG.

Raises:
    FileNotFoundError: If FFMPEG executable is not found.

Example:
    >>> stdout, stderr = ffmpeg.execute("-version")
    >>> print(stdout)

    >>> # Extract audio from video
    >>> ffmpeg.execute("-i", "video.mp4", "-q:a", "0", "-map", "a", "audio.mp3")

    >>> # Add watermark to video
    >>> ffmpeg.execute("-i", "video.mp4", "-i", "watermark.png",
    ...                "-filter_complex", "overlay=10:10", "output.mp4")

```

#### `reformat(input_file: str, output_file: str)`
```python

Convert a video file from one format to another.

This method performs a simple format conversion without
modifying video quality or other parameters.

Args:
    input_file: Path to the input video file.
    output_file: Path for the output video file.

Raises:
    FileNotFoundError: If input file doesn't exist.
    Prints FFMPEG output (stdout or stderr) to console.

Example:
    >>> ffmpeg.reformat("input.mov", "output.mp4")
    >>> ffmpeg.reformat("video.avi", "video.mkv")

```

#### `gif(input_file: str, output_file: str, fps: int = 10, scale: int = 320)`
```python

Convert a video file to an optimized GIF.

Creates a high-quality GIF using FFMPEG's palette optimization
for better color reproduction and smaller file sizes.

Args:
    input_file: Path to the input video file.
    output_file: Path for the output GIF file.
    fps: Frames per second for the GIF. Defaults to 10.
    scale: Width of the GIF in pixels. Height is auto-scaled
           to maintain aspect ratio. Defaults to 320.

Returns:
    tuple[str, str]: A tuple containing (stdout, stderr) from FFMPEG.

Raises:
    FileNotFoundError: If input file doesn't exist.
    RuntimeError: If GIF file was not created successfully.

Example:
    >>> # Create a standard GIF
    >>> stdout, stderr = ffmpeg.gif("video.mp4", "output.gif")

    >>> # Create a higher quality GIF with custom settings
    >>> stdout, stderr = ffmpeg.gif("video.mp4", "output.gif",
    ...                             fps=15, scale=640)

    >>> # Create a small thumbnail GIF
    >>> stdout, stderr = ffmpeg.gif("video.mp4", "thumbnail.gif",
    ...                             fps=5, scale=160)

```

#### `trim(input_file: str, output_file: str, start: float = 0, duration: float | None = None)`
```python

Trim a video file.

Extracts a segment from a video file starting at a specified time
and optionally ending after a specified duration.

Args:
    input_file: Path to the input video file.
    output_file: Path for the output trimmed video.
    start: Start time in seconds. Defaults to 0.
    duration: Duration in seconds, or None for remaining video.
              Defaults to None.

Returns:
    tuple[str, str]: A tuple containing (stdout, stderr) from FFMPEG.

Raises:
    FileNotFoundError: If input file doesn't exist.
    ValueError: If start is negative or duration is non-positive.
    RuntimeError: If trimmed video was not created successfully.

Example:
    >>> # Trim from 5 seconds to 10 seconds (5-second clip)
    >>> stdout, stderr = ffmpeg.trim("video.mp4", "clip.mp4",
    ...                               start=5, duration=5)

    >>> # Trim from 10 seconds to the end of video
    >>> stdout, stderr = ffmpeg.trim("video.mp4", "ending.mp4",
    ...                               start=10)

    >>> # Trim first 30 seconds of video
    >>> stdout, stderr = ffmpeg.trim("video.mp4", "intro.mp4",
    ...                               start=0, duration=30)

    >>> # Trim with floating point precision
    >>> stdout, stderr = ffmpeg.trim("video.mp4", "precise.mp4",
    ...                               start=2.5, duration=3.75)

```

## Usage Examples

### Basic Usage
```python
from ffmpeg_python_helper import FFMPEG

# Initialize
ffmpeg = FFMPEG()

# Convert video format
ffmpeg.reformat('input.mp4', 'output.avi')

# Create GIF
ffmpeg.gif('video.mp4', 'animation.gif', fps=15, scale=480)

# Trim video
ffmpeg.trim('video.mp4', 'short_clip.mp4', start=10.5, duration=5.0)
```

### Advanced Usage
```python
# Custom FFMPEG commands
ffmpeg.execute('-i', 'video.mp4', '-q:a', '0', '-map', 'a', 'audio.mp3')

# Batch processing
import os
videos = ['video1.mp4', 'video2.mp4', 'video3.mp4']
for video in videos:
    if os.path.exists(video):
        base_name = os.path.splitext(video)[0]
        ffmpeg.gif(video, f'{base_name}.gif', fps=12, scale=400)
```
