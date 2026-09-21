# FFMPEG Python Helper

A Python wrapper for FFMPEG that provides a simple, intuitive API for common video processing tasks.

## Features

- 🔧 **Easy FFMPEG Integration** - Automatically detects FFMPEG installation
- 🎥 **Video Processing** - Reformat videos between formats
- 🎞️ **GIF Creation** - Convert videos to optimized GIFs with customizable settings
- 🎵 **Audio Extraction** - Extract audio tracks from videos without re-encoding
- 🧠 **In-Memory Processing** - Process video/audio data directly from bytes without temporary files
- ✂️ **Video Trimming** - Trim videos with precise start time and duration control
- 🔍 **Video Metadata Analysis** - Extract video information and metadata using FFProbe
- ⚡ **Asynchronous Operations** - Non-blocking async API for responsive applications
- 🐍 **Pythonic API** - Clean, object-oriented interface with proper error handling
- 📁 **File Validation** - Automatic input file existence checking

## Installation

### Prerequisites
- Python 3.14 or higher
- FFMPEG installed and available in your system PATH

### Install FFMPEG Python Helper

```bash
pip install ffmpeg-python-helper
```

Or install from source:

```bash
git clone https://github.com/yourusername/ffmpeg-python-helper.git
cd ffmpeg-python-helper
pip install -e .
```

## Quick Start

```python
from ffmpeg_python_helper import FFMPEG

# Initialize the FFMPEG wrapper
ffmpeg = FFMPEG()

# Check if FFMPEG is available
print(f"FFMPEG executable found at: {ffmpeg.executable}")

# Convert a video file
output = ffmpeg.reformat("input.mp4", "output.avi")
print(output.decode())

# Create a GIF from video
ffmpeg.gif("video.mp4", "animation.gif", fps=15, scale=480)

# Trim a video
ffmpeg.trim("video.mp4", "short_clip.mp4", start=10.5, duration=5.0)

# Extract audio from video
ffmpeg.extract_audio("video.mp4", "audio.m4a")

# Create GIF from in-memory video data
with open("video.mp4", "rb") as f:
    video_data = f.read()
gif_data = ffmpeg.gifs(video_data, fps=15, scale=480)
with open("memory.gif", "wb") as f:
    f.write(gif_data)

# Trim video in memory
trimmed_data = ffmpeg.trims(video_data, start=0, duration=30)
with open("trimmed.mp4", "wb") as f:
    f.write(trimmed_data)

# Extract audio in memory
audio_data = ffmpeg.extract_audios(video_data, output_format="m4a")
with open("audio.m4a", "wb") as f:
    f.write(audio_data)

# Analyze video metadata with FFProbe
from ffmpeg_python_helper import FFProbe
import json

ffprobe = FFProbe()
print(f"FFProbe executable found at: {ffprobe.executable}")

# Check if video is short enough for social media
if ffprobe.is_max_length("video.mp4", max_length=5.0):
    print("Video is perfect for Instagram Reels!")
else:
    print("Video needs trimming for short-form content")

# Get detailed video metadata
stdout, stderr = ffprobe.execute("-v", "quiet", "-print_format", "json", 
                                 "-show_format", "-show_streams", "video.mp4")
metadata = json.loads(stdout.decode())
print(f"Video duration: {metadata['format']['duration']} seconds")
print(f"Video dimensions: {metadata['streams'][0]['width']}x{metadata['streams'][0]['height']}")

# Use AsyncFFMPEG for non-blocking operations
import asyncio
from ffmpeg_python_helper import AsyncFFMPEG

async def process_video_async():
    async_ffmpeg = AsyncFFMPEG()
    print(f"AsyncFFMPEG executable found at: {async_ffmpeg.executable}")
    
    # Convert video asynchronously
    output = await async_ffmpeg.reformat("input.mp4", "output_async.avi")
    print(f"Async conversion output: {output.decode()[:50]}...")
    
    # Create GIF asynchronously
    await async_ffmpeg.gif("video.mp4", "animation_async.gif", fps=15, scale=480)
    print("Async GIF creation completed!")

# Run the async function
asyncio.run(process_video_async())
```

## API Reference

### `FFMPEG` Class

The main class that wraps FFMPEG functionality.

#### Constructor
```python
FFMPEG()
```
Creates a new FFMPEG instance. Automatically searches for FFMPEG in the system PATH.
- **Raises**: `FileNotFoundError` if FFMPEG is not found in PATH

#### Properties
- `executable` (str): The path to the FFMPEG executable found in the system

#### Class Methods
```python
@classmethod
def api(cls) -> "FFMPEG"
```
Factory method that returns a new FFMPEG instance.
- **Returns**: `FFMPEG` instance

#### Instance Methods

##### `execute(*args: str, input_data: bytes | None = None) -> tuple[bytes, bytes]`
Execute raw FFMPEG commands with the given arguments.

**Parameters:**
- `*args` (str): FFMPEG command-line arguments
- `input_data` (bytes | None, optional): Optional bytes to send to FFMPEG's stdin

**Returns:**
- `tuple[bytes, bytes]`: A tuple containing (stdout, stderr) as bytes

**Raises:**
- `FileNotFoundError`: If FFMPEG executable is not found
- `RuntimeError`: If FFMPEG command returns a non-zero exit code

**Example:**
```python
stdout, stderr = ffmpeg.execute("-version")
print(stdout.decode())

# Process data from memory
video_data = b"...video bytes..."
stdout, stderr = ffmpeg.execute("-i", "pipe:0", "-f", "null", "-", input_data=video_data)
```

##### `reformat(input_file: str, output_file: str) -> bytes`
Convert a video file from one format to another.

**Parameters:**
- `input_file` (str): Path to the input video file
- `output_file` (str): Path for the output video file

**Returns:**
- `bytes`: FFMPEG output (stdout or stderr) as bytes

**Raises:**
- `FileNotFoundError`: If input file doesn't exist

**Example:**
```python
output = ffmpeg.reformat("input.mov", "output.mp4")
print(output.decode())
```

##### `gif(input_file: str, output_file: str, fps: int = 10, scale: int = 320) -> bytes`
Convert a video file to an optimized GIF.

**Parameters:**
- `input_file` (str): Path to the input video file
- `output_file` (str): Path for the output GIF file
- `fps` (int, optional): Frames per second for the GIF (default: 10)
- `scale` (int, optional): Width of the GIF in pixels, height is auto-scaled (default: 320)

**Returns:**
- `bytes`: FFMPEG output (stdout or stderr) as bytes

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `RuntimeError`: If GIF file was not created successfully

**Example:**
```python
output = ffmpeg.gif("video.mp4", "output.gif", fps=15, scale=640)
print(output.decode())
```

##### `gifs(input_byte: bytes, fps: int = 10, scale: int = 320) -> bytes`
Convert video data from bytes to an optimized GIF (in-memory processing).

**Parameters:**
- `input_byte` (bytes): Video data as bytes to convert to GIF
- `fps` (int, optional): Frames per second for the GIF (default: 10)
- `scale` (int, optional): Width of the GIF in pixels, height is auto-scaled (default: 320)

**Returns:**
- `bytes`: The generated GIF data as bytes

**Raises:**
- `RuntimeError`: If GIF conversion fails

**Example:**
```python
# Read video data from a file
with open("video.mp4", "rb") as f:
    video_data = f.read()

# Convert to GIF in memory
gif_data = ffmpeg.gifs(video_data, fps=15, scale=480)

# Save the GIF
with open("output.gif", "wb") as f:
    f.write(gif_data)
```

##### `trim(input_file: str, output_file: str, start: float = 0, duration: float | None = None) -> bytes`
Trim a video file.

**Parameters:**
- `input_file` (str): Path to the input video file
- `output_file` (str): Path for the output trimmed video
- `start` (float, optional): Start time in seconds (default: 0)
- `duration` (float | None, optional): Duration in seconds, or None for remaining video (default: None)

**Returns:**
- `bytes`: FFMPEG output (stdout or stderr) as bytes

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `ValueError`: If start is negative or duration is non-positive
- `RuntimeError`: If trimmed video was not created successfully

**Example:**
```python
# Trim from 5 seconds to 10 seconds (5-second clip)
output = ffmpeg.trim("video.mp4", "clip.mp4", start=5, duration=5)
print(output.decode())

# Trim from 10 seconds to the end of video
output = ffmpeg.trim("video.mp4", "ending.mp4", start=10)
print(output.decode())
```

### `FFProbe` Class

A Python wrapper for FFProbe (the FFMPEG multimedia stream analyzer) that provides video metadata analysis capabilities.

#### Constructor
```python
FFProbe()
```
Creates a new FFProbe instance. Automatically searches for FFProbe in the system PATH.
- **Raises**: `FileNotFoundError` if FFProbe is not found in PATH

#### Properties
- `executable` (str): The path to the FFProbe executable found in the system

#### Class Methods
```python
@classmethod
def api(cls) -> "FFProbe"
```
Factory method that returns a new FFProbe instance.
- **Returns**: `FFProbe` instance

**Example:**
```python
ffprobe = FFProbe.api()
print(f"FFProbe executable found at: {ffprobe.executable}")
```

#### Instance Methods

##### `execute(*args: str, input_data: bytes | None = None) -> tuple[bytes, bytes]`
Execute raw FFProbe commands with the given arguments.

**Parameters:**
- `*args` (str): FFProbe command-line arguments as strings
- `input_data` (bytes | None, optional): Optional bytes to send to FFProbe's stdin

**Returns:**
- `tuple[bytes, bytes]`: A tuple containing (stdout, stderr) as bytes

**Raises:**
- `FileNotFoundError`: If FFProbe executable is not found
- `RuntimeError`: If FFProbe command returns a non-zero exit code

**Example:**
```python
# Get FFProbe version
stdout, stderr = ffprobe.execute("-version")
print(stdout.decode())

# Get video metadata in JSON format
stdout, stderr = ffprobe.execute("-v", "quiet", "-print_format", "json", 
                                 "-show_format", "-show_streams", "video.mp4")
metadata = json.loads(stdout.decode())
print(f"Video duration: {metadata['format']['duration']} seconds")

# Get video dimensions
stdout, stderr = ffprobe.execute("-v", "error", "-select_streams", "v:0",
                                 "-show_entries", "stream=width,height", 
                                 "-of", "csv=p=0", "video.mp4")
print(f"Video dimensions: {stdout.decode().strip()}")
```

##### `is_max_length(input_file: str, max_length: float = 5.0) -> bool`
Check if a video file's duration is less than or equal to a specified maximum length.

**Parameters:**
- `input_file` (str): Path to the input video file
- `max_length` (float, optional): Maximum allowed duration in seconds (default: 5.0)

**Returns:**
- `bool`: `True` if video duration ≤ max_length, `False` otherwise

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `RuntimeError`: If FFProbe command fails

**Example:**
```python
# Check if video is shorter than 10 seconds
if ffprobe.is_max_length("video.mp4", max_length=10.0):
    print("Video is short enough for social media upload")
else:
    print("Video is too long, needs trimming")

# Check multiple videos for length compliance
videos = ["clip1.mp4", "clip2.mp4", "clip3.mp4"]
for video in videos:
    if ffprobe.is_max_length(video, max_length=5.0):
        print(f"{video}: OK (≤ 5 seconds)")
    else:
        print(f"{video}: Too long (> 5 seconds)")
```

### `AsyncFFMPEG` Class

An asynchronous Python wrapper for FFMPEG that provides a simple, intuitive API for common video processing tasks with non-blocking operations.

This class provides all the same functionality as the `FFMPEG` class but with asynchronous methods, allowing you to perform video processing operations without blocking your application. This is especially useful for web applications, GUI applications, or any scenario where you need to maintain responsiveness while performing video processing tasks.

#### Constructor
```python
AsyncFFMPEG()
```
Creates a new AsyncFFMPEG instance. Automatically searches for FFMPEG in the system PATH.
- **Raises**: `FileNotFoundError` if FFMPEG is not found in PATH

#### Properties
- `executable` (str): The path to the FFMPEG executable found in the system

#### Class Methods
```python
@classmethod
def api(cls) -> "AsyncFFMPEG"
```
Factory method that returns a new AsyncFFMPEG instance.
- **Returns**: `AsyncFFMPEG` instance

#### Instance Methods

All methods are asynchronous and must be awaited. The API mirrors the synchronous `FFMPEG` class but with `async`/`await` syntax.

##### `async execute(*args: str, input_data: bytes | None = None) -> tuple[bytes, bytes]`
Execute raw FFMPEG commands asynchronously with the given arguments.

**Parameters:**
- `*args` (str): FFMPEG command-line arguments
- `input_data` (bytes | None, optional): Optional bytes to send to FFMPEG's stdin

**Returns:**
- `tuple[bytes, bytes]`: A tuple containing (stdout, stderr) as bytes

**Raises:**
- `FileNotFoundError`: If FFMPEG executable is not found
- `RuntimeError`: If FFMPEG command returns a non-zero exit code

**Example:**
```python
# Must be called within an async context
stdout, stderr = await async_ffmpeg.execute("-version")
print(stdout.decode())

# Process data from memory asynchronously
video_data = b"...video bytes..."
stdout, stderr = await async_ffmpeg.execute("-i", "pipe:0", "-f", "null", "-", input_data=video_data)
```

##### `async reformat(input_file: str, output_file: str) -> bytes`
Asynchronously convert a video file from one format to another.

**Parameters:**
- `input_file` (str): Path to the input video file
- `output_file` (str): Path for the output video file

**Returns:**
- `bytes`: FFMPEG output (stdout or stderr) as bytes

**Raises:**
- `FileNotFoundError`: If input file doesn't exist

**Example:**
```python
output = await async_ffmpeg.reformat("input.mov", "output.mp4")
print(output.decode())
```

##### `async gif(input_file: str, output_file: str, fps: int = 10, scale: int = 320) -> bytes`
Asynchronously convert a video file to an optimized GIF.

**Parameters:**
- `input_file` (str): Path to the input video file
- `output_file` (str): Path for the output GIF file
- `fps` (int, optional): Frames per second for the GIF (default: 10)
- `scale` (int, optional): Width of the GIF in pixels, height is auto-scaled (default: 320)

**Returns:**
- `bytes`: FFMPEG output (stdout or stderr) as bytes

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `RuntimeError`: If GIF file was not created successfully

**Example:**
```python
output = await async_ffmpeg.gif("video.mp4", "output.gif", fps=15, scale=640)
print(output.decode())
```

##### `async gifs(input_byte: bytes, fps: int = 10, scale: int = 320) -> bytes`
Asynchronously convert video data from bytes to an optimized GIF (in-memory processing).

**Parameters:**
- `input_byte` (bytes): Video data as bytes to convert to GIF
- `fps` (int, optional): Frames per second for the GIF (default: 10)
- `scale` (int, optional): Width of the GIF in pixels, height is auto-scaled (default: 320)

**Returns:**
- `bytes`: The generated GIF data as bytes

**Raises:**
- `RuntimeError`: If GIF conversion fails

**Example:**
```python
# Read video data from a file
with open("video.mp4", "rb") as f:
    video_data = f.read()

# Convert to GIF in memory asynchronously
gif_data = await async_ffmpeg.gifs(video_data, fps=15, scale=480)

# Save the GIF
with open("output.gif", "wb") as f:
    f.write(gif_data)
```

##### `async trim(input_file: str, output_file: str, start: float = 0, duration: float | None = None) -> bytes`
Asynchronously trim a video file.

**Parameters:**
- `input_file` (str): Path to the input video file
- `output_file` (str): Path for the output trimmed video
- `start` (float, optional): Start time in seconds (default: 0)
- `duration` (float | None, optional): Duration in seconds, or None for remaining video (default: None)

**Returns:**
- `bytes`: FFMPEG output (stdout or stderr) as bytes

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `ValueError`: If start is negative or duration is non-positive
- `RuntimeError`: If trimmed video was not created successfully

**Example:**
```python
# Trim from 5 seconds to 10 seconds (5-second clip) asynchronously
output = await async_ffmpeg.trim("video.mp4", "clip.mp4", start=5, duration=5)
print(output.decode())

# Trim from 10 seconds to the end of video asynchronously
output = await async_ffmpeg.trim("video.mp4", "ending.mp4", start=10)
print(output.decode())
```

## Advanced Usage

### Custom FFMPEG Commands
For operations not covered by the built-in methods, use the `execute` method:

```python
# Extract audio from video
ffmpeg.execute("-i", "video.mp4", "-q:a", "0", "-map", "a", "audio.mp3")

# Add watermark to video
ffmpeg.execute("-i", "video.mp4", "-i", "watermark.png", 
               "-filter_complex", "overlay=10:10", "output.mp4")

# Change video bitrate
ffmpeg.execute("-i", "input.mp4", "-b:v", "1M", "output.mp4")
```

### Advanced FFProbe Usage
FFProbe provides powerful video metadata analysis capabilities:

```python
from ffmpeg_python_helper import FFProbe
import json

ffprobe = FFProbe()

# Get multiple video metadata properties at once
stdout, stderr = ffprobe.execute(
    "-v", "error",
    "-select_streams", "v:0",
    "-show_entries", "stream=width,height,duration,bit_rate,codec_name",
    "-of", "json",
    "video.mp4"
)
video_info = json.loads(stdout.decode())
print(f"Video codec: {video_info['streams'][0]['codec_name']}")
print(f"Video bitrate: {video_info['streams'][0]['bit_rate']} bps")

# Check frame rate
stdout, stderr = ffprobe.execute(
    "-v", "error",
    "-select_streams", "v:0",
    "-show_entries", "stream=r_frame_rate",
    "-of", "default=noprint_wrappers=1:nokey=1",
    "video.mp4"
)
print(f"Frame rate: {stdout.decode().strip()}")

# Get audio stream information
stdout, stderr = ffprobe.execute(
    "-v", "error",
    "-select_streams", "a:0",
    "-show_entries", "stream=codec_name,channels,sample_rate",
    "-of", "json",
    "video.mp4"
)
audio_info = json.loads(stdout.decode())
if audio_info['streams']:
    print(f"Audio codec: {audio_info['streams'][0]['codec_name']}")
    print(f"Audio channels: {audio_info['streams'][0]['channels']}")
    print(f"Sample rate: {audio_info['streams'][0]['sample_rate']} Hz")
```

### Asynchronous Batch Processing with AsyncFFMPEG
AsyncFFMPEG is ideal for batch processing and web applications where you need to maintain responsiveness:

```python
import asyncio
from ffmpeg_python_helper import AsyncFFMPEG

async def process_videos_concurrently():
    async_ffmpeg = AsyncFFMPEG()
    videos = ["video1.mp4", "video2.mp4", "video3.mp4"]
    
    # Process multiple videos concurrently
    tasks = []
    for video in videos:
        task = async_ffmpeg.gif(video, f"{video}_async.gif", fps=12, scale=400)
        tasks.append(task)
    
    # Wait for all async tasks to complete
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle results
    for video, result in zip(videos, results):
        if isinstance(result, Exception):
            print(f"Failed to process {video}: {result}")
        else:
            print(f"Successfully processed {video}: {len(result)} bytes output")

# Run concurrent processing
asyncio.run(process_videos_concurrently())
```

### Error Handling
```python
from ffmpeg_python_helper import FFMPEG
import sys

try:
    ffmpeg = FFMPEG()
    ffmpeg.gif("video.mp4", "output.gif")
except FileNotFoundError as e:
    print(f"FFMPEG not found: {e}", file=sys.stderr)
    sys.exit(1)
except RuntimeError as e:
    print(f"Processing failed: {e}", file=sys.stderr)
    sys.exit(1)
```

## Common Use Cases

### Batch Processing
```python
import os
from ffmpeg_python_helper import FFMPEG

ffmpeg = FFMPEG()
videos = ["video1.mp4", "video2.mp4", "video3.mp4"]

for video in videos:
    if os.path.exists(video):
        base_name = os.path.splitext(video)[0]
        ffmpeg.gif(video, f"{base_name}.gif", fps=12, scale=400)
```

### Video Compilation
```python
from ffmpeg_python_helper import FFMPEG

ffmpeg = FFMPEG()

# Trim interesting parts
ffmpeg.trim("concert.mp4", "intro.mp4", start=0, duration=30)
ffmpeg.trim("concert.mp4", "chorus.mp4", start=120, duration=45)
ffmpeg.trim("concert.mp4", "finale.mp4", start=300, duration=60)

# Later, use FFMPEG to concatenate trimmed parts
ffmpeg.execute("-f", "concat", "-safe", "0", "-i", "parts.txt", "highlight_reel.mp4")
```

## Troubleshooting

### FFMPEG Not Found
If you get `FileNotFoundError` when creating an FFMPEG instance:

1. **Install FFMPEG**:
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (Fedora/RHEL)

2. **Add to PATH**:
   - Ensure FFMPEG is in your system PATH
   - Test with `ffmpeg -version` in your terminal

### File Not Found Errors
- Ensure input file paths are correct and files exist
- Use absolute paths if working with files in different directories
- Check file permissions

### GIF Creation Issues
- Lower FPS or scale if GIF file is too large
- Ensure input video has sufficient quality
- Check available disk space

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Building Documentation
```bash
# Install documentation dependencies
pip install pdoc3

# Generate API documentation
pdoc --html ffmpeg_python_helper --output-dir docs
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Add tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/nojram00/python-ffmpeg/issues)
- **Email**: marjongodito.0505@gmail.com

## Acknowledgments

- FFMPEG team for the amazing multimedia framework
- Python community for excellent tooling and libraries