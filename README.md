# FFMPEG Python Helper

A Python wrapper for FFMPEG that provides a simple, intuitive API for common video processing tasks.

## Features

- 🔧 **Easy FFMPEG Integration** - Automatically detects FFMPEG installation
- 🎥 **Video Processing** - Reformat videos between formats
- 🎞️ **GIF Creation** - Convert videos to optimized GIFs with customizable settings
- 🧠 **In-Memory Processing** - Process video data directly from bytes without temporary files
- ✂️ **Video Trimming** - Trim videos with precise start time and duration control
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
output = ffmpeg.gif("video.mp4", "animation.gif", fps=15, scale=480)
print(output.decode())

# Trim a video
output = ffmpeg.trim("video.mp4", "short_clip.mp4", start=10.5, duration=5.0)
print(output.decode())

# Create GIF from in-memory video data
with open("video.mp4", "rb") as f:
    video_data = f.read()
gif_data = ffmpeg.gifs(video_data, fps=15, scale=480)
with open("memory.gif", "wb") as f:
    f.write(gif_data)
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

- **Issues**: [GitHub Issues](https://github.com/yourusername/ffmpeg-python-helper/issues)
- **Documentation**: [ReadTheDocs](https://ffmpeg-python-helper.readthedocs.io)
- **Email**: marjongodito@gmanmi.com

## Acknowledgments

- FFMPEG team for the amazing multimedia framework
- Python community for excellent tooling and libraries