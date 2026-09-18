import subprocess
from pathlib import Path


class FFMPEG:
    """
    A Python wrapper for FFMPEG that provides a simple, intuitive API for
    common video processing tasks.

    This class automatically detects FFMPEG installation in the system PATH
    and provides methods for video conversion, GIF creation, and video trimming.
    It supports both file-based operations and in-memory data processing.

    Example:
        >>> from ffmpeg_python_helper import FFMPEG
        >>> ffmpeg = FFMPEG()
        >>> ffmpeg.reformat("input.mp4", "output.avi")
        >>> ffmpeg.gif("video.mp4", "animation.gif", fps=15, scale=480)
        >>> ffmpeg.trim("video.mp4", "short_clip.mp4", start=10.5, duration=5.0)
        >>> 
        >>> # In-memory processing
        >>> with open("video.mp4", "rb") as f:
        ...     video_data = f.read()
        >>> gif_data = ffmpeg.gifs(video_data, fps=15, scale=480)

    Attributes:
        executable (str): The path to the FFMPEG executable found in the system PATH.
    """

    def __init__(self) -> None:
        """
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
        """
        import shutil
        self.executable = shutil.which('ffmpeg')

        if self.executable is None:
            raise FileNotFoundError("""
FFmpeg is not installed or could not be found in PATH.
Please install FFmpeg and make sure it is available
in your system PATH.
""")

    @classmethod
    def api(cls) -> "FFMPEG":
        """
        Factory method that returns a new FFMPEG instance.

        Returns:
            FFMPEG: A new instance of the FFMPEG class.

        Example:
            >>> ffmpeg = FFMPEG.api()
            >>> ffmpeg.execute("-version")
        """
        return cls()

    def execute(self, *args: str, input_data: bytes | None = None) -> tuple[bytes, bytes]:
        """
        Execute raw FFMPEG commands with the given arguments.

        This method allows you to run any FFMPEG command directly,
        providing maximum flexibility for operations not covered
        by the built-in methods.

        Args:
            *args: FFMPEG command-line arguments as strings.
            input_data: Optional bytes to send to FFMPEG's stdin. Useful for
                       piping data directly to FFMPEG without intermediate files.

        Returns:
            tuple[bytes, bytes]: A tuple containing (stdout, stderr) from FFMPEG
                                 as bytes objects.

        Raises:
            FileNotFoundError: If FFMPEG executable is not found.
            RuntimeError: If FFMPEG command returns a non-zero exit code.

        Example:
            >>> stdout, stderr = ffmpeg.execute("-version")
            >>> print(stdout.decode())

            >>> # Extract audio from video
            >>> ffmpeg.execute("-i", "video.mp4", "-q:a", "0", "-map", "a", "audio.mp3")

            >>> # Add watermark to video
            >>> ffmpeg.execute("-i", "video.mp4", "-i", "watermark.png",
            ...                "-filter_complex", "overlay=10:10", "output.mp4")

            >>> # Process data from memory
            >>> video_data = b"...video bytes..."
            >>> stdout, stderr = ffmpeg.execute("-i", "pipe:0", "-f", "null", "-",
            ...                                 input_data=video_data)
        """
        if self.executable:
            result = subprocess.run(
                [self.executable, *args], 
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False
                )

            if result.returncode != 0:
                raise RuntimeError(
                    result.stderr.decode(errors="replace")
                )
            
            return result.stdout, result.stderr

        raise FileNotFoundError("""
        No ffmpeg executable found.

        Please Install ffmpeg first.
        """)

    def reformat(self, input_file: str, output_file: str) -> bytes:
        """
        Convert a video file from one format to another.

        This method performs a simple format conversion without
        modifying video quality or other parameters.

        Args:
            input_file: Path to the input video file.
            output_file: Path for the output video file.

        Returns:
            bytes: FFMPEG output (stdout or stderr) as bytes.

        Raises:
            FileNotFoundError: If input file doesn't exist.

        Example:
            >>> output = ffmpeg.reformat("input.mov", "output.mp4")
            >>> print(output.decode())
            >>> 
            >>> output = ffmpeg.reformat("video.avi", "video.mkv")
            >>> print(output.decode())
        """
        if not Path(input_file).exists():
            raise FileNotFoundError(f"""
                    Input file {input_file} did not found .
            
                    Please check filename and directory if correct.
                    """)

        stdout, stderr = self.execute("-i", input_file, output_file)

        if stdout:
            return stdout
        else:
            return stderr

    def gifs(self,
            input_byte: bytes,
            fps: int = 10,
            scale: int = 320) -> bytes:
        """
        Convert video data from bytes to an optimized GIF.

        Creates a high-quality GIF from in-memory video data using FFMPEG's
        palette optimization. This method is useful when you have video data
        in memory and want to avoid writing temporary files.

        Args:
            input_byte: Video data as bytes to convert to GIF.
            fps: Frames per second for the GIF. Defaults to 10.
            scale: Width of the GIF in pixels. Height is auto-scaled
                   to maintain aspect ratio. Defaults to 320.

        Returns:
            bytes: The generated GIF data as bytes.

        Raises:
            RuntimeError: If GIF conversion fails.

        Example:
            >>> # Read video data from a file
            >>> with open("video.mp4", "rb") as f:
            ...     video_data = f.read()
            >>> 
            >>> # Convert to GIF in memory
            >>> gif_data = ffmpeg.gifs(video_data, fps=15, scale=480)
            >>> 
            >>> # Save the GIF
            >>> with open("output.gif", "wb") as f:
            ...     f.write(gif_data)

            >>> # Process video from network or database
            >>> # video_bytes = download_video_from_url(url)
            >>> # gif_bytes = ffmpeg.gifs(video_bytes, scale=320)
        """
        filter_graph: str = (
            f"fps={fps},"
            f"scale={scale}:-1:flags=lanczos,"
            "split[s0][s1];"
            "[s0]palettegen[p];"
            "[s1][p]paletteuse"
        )

        stdout, stderr = self.execute(
            "-y",
            "-i", "pipe:0",
            "-vf", filter_graph,
            "-f", "gif",
            "pipe:1",
            input_data=input_byte
        )

        return stdout

    def gif(self,
            input_file: str,
            output_file: str,
            fps: int = 10,
            scale: int = 320
            ) -> bytes:
        """
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
            bytes: FFMPEG output (stdout or stderr) as bytes.

        Raises:
            FileNotFoundError: If input file doesn't exist.
            RuntimeError: If GIF file was not created successfully.

        Example:
            >>> # Create a standard GIF
            >>> output = ffmpeg.gif("video.mp4", "output.gif")
            >>> print(output.decode())

            >>> # Create a higher quality GIF with custom settings
            >>> output = ffmpeg.gif("video.mp4", "output.gif",
            ...                     fps=15, scale=640)
            >>> print(output.decode())

            >>> # Create a small thumbnail GIF
            >>> output = ffmpeg.gif("video.mp4", "thumbnail.gif",
            ...                     fps=5, scale=160)
            >>> print(output.decode())
        """
        input_path = Path(input_file)
        output_path = Path(output_file)

        if not input_path.exists():
            raise FileNotFoundError(
                f"Input file {input_file} was not found."
            )

        filter_graph: str = (
            f"fps={fps},"
            f"scale={scale}:-1:flags=lanczos,"
            "split[s0][s1];"
            "[s0]palettegen[p];"
            "[s1][p]paletteuse"
        )

        stdout, stderr = self.execute(
            "-y",
            "-i", str(input_path),
            "-vf", filter_graph,
            str(output_path),
        )

        if not output_path.exists():
            raise RuntimeError(
                f"GIF was not created: {output_file}"
            )

        if stderr:
            return stderr

        return stdout

    def trim(
        self,
        input_file: str,
        output_file: str,
        start: float = 0,
        duration: float | None = None,
    ) -> bytes:
        """
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
            bytes: FFMPEG output (stdout or stderr) as bytes.

        Raises:
            FileNotFoundError: If input file doesn't exist.
            ValueError: If start is negative or duration is non-positive.
            RuntimeError: If trimmed video was not created successfully.

        Example:
            >>> # Trim from 5 seconds to 10 seconds (5-second clip)
            >>> output = ffmpeg.trim("video.mp4", "clip.mp4",
            ...                      start=5, duration=5)
            >>> print(output.decode())

            >>> # Trim from 10 seconds to the end of video
            >>> output = ffmpeg.trim("video.mp4", "ending.mp4",
            ...                      start=10)
            >>> print(output.decode())

            >>> # Trim first 30 seconds of video
            >>> output = ffmpeg.trim("video.mp4", "intro.mp4",
            ...                      start=0, duration=30)
            >>> print(output.decode())

            >>> # Trim with floating point precision
            >>> output = ffmpeg.trim("video.mp4", "precise.mp4",
            ...                      start=2.5, duration=3.75)
            >>> print(output.decode())
        """
        input_path = Path(input_file)
        output_path = Path(output_file)

        if not input_path.exists():
            raise FileNotFoundError(
                f"Input file {input_file} was not found."
            )

        if start < 0:
            raise ValueError("start must be greater than or equal to 0")

        if duration is not None and duration <= 0:
            raise ValueError("duration must be greater than 0")

        args = [
            "-y",
            "-ss", str(start),
            "-i", str(input_path),
        ]

        if duration is not None:
            args.extend(["-t", str(duration)])

        args.append(str(output_path))

        stdout, stderr = self.execute(*args)

        if not output_path.exists():
            raise RuntimeError(
                f"Trimmed video was not created: {output_file}"
            )

        return stdout if stdout else stderr