import subprocess
from pathlib import Path


class FFMPEG:
    """
    A Python wrapper for FFMPEG that provides a simple, intuitive API for
    common video processing tasks.

    This class automatically detects FFMPEG installation in the system PATH
    and provides methods for video conversion, GIF creation, video trimming,
    and audio extraction. It supports both file-based operations and 
    in-memory data processing.

    Example:
        >>> from ffmpeg_python_helper import FFMPEG
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
            input_bytes: bytes,
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
            input_data=input_bytes
        )

        return stdout

    def gif(self,
            input_file: str,
            output_file: str,
            fps: int = 10,
            scale: int = 320
            ) -> None:
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

        Raises:
            FileNotFoundError: If input file doesn't exist.
            RuntimeError: If GIF file was not created successfully.

        Example:
            >>> # Create a standard GIF
            >>> ffmpeg.gif("video.mp4", "output.gif")

            >>> # Create a higher quality GIF with custom settings
            >>> ffmpeg.gif("video.mp4", "output.gif",
            ...            fps=15, scale=640)

            >>> # Create a small thumbnail GIF
            >>> ffmpeg.gif("video.mp4", "thumbnail.gif",
            ...            fps=5, scale=160)
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

        self.execute(
            "-y",
            "-i", str(input_path),
            "-vf", filter_graph,
            str(output_path),
        )

        if not output_path.exists():
            raise RuntimeError(
                f"GIF was not created: {output_file}"
            )

    def trim(
        self,
        input_file: str,
        output_file: str,
        start: float = 0,
        duration: float | None = None,
    ) -> None:
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

        Raises:
            FileNotFoundError: If input file doesn't exist.
            ValueError: If start is negative or duration is non-positive.
            RuntimeError: If trimmed video was not created successfully.

        Example:
            >>> # Trim from 5 seconds to 10 seconds (5-second clip)
            >>> ffmpeg.trim("video.mp4", "clip.mp4",
            ...             start=5, duration=5)

            >>> # Trim from 10 seconds to the end of video
            >>> ffmpeg.trim("video.mp4", "ending.mp4",
            ...             start=10)

            >>> # Trim first 30 seconds of video
            >>> ffmpeg.trim("video.mp4", "intro.mp4",
            ...             start=0, duration=30)

            >>> # Trim with floating point precision
            >>> ffmpeg.trim("video.mp4", "precise.mp4",
            ...             start=2.5, duration=3.75)
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

    def trims(self, input_bytes: bytes,
            start: float = 0,
            duration: float | None = None,
            format_type: str = "mp4",
            v_encoder : str = "libx264",
            a_encoder : str = "aac"
            ) -> bytes:
        """
        Trim video data from bytes (in-memory processing).

        Extracts a segment from in-memory video data starting at a specified time
        and optionally ending after a specified duration. This method is useful
        when you have video data in memory and want to avoid writing temporary files.

        Note: For MP4 format, this method uses libx264 video codec and AAC audio codec
        with fragmented MP4 output for better streaming compatibility.

        Args:
            input_bytes: Video data as bytes to trim.
            start: Start time in seconds. Defaults to 0.
            duration: Duration in seconds, or None for remaining video.
                      Defaults to None.
            format_type: Output format (e.g., 'mp4', 'avi', 'mov'). Defaults to 'mp4'.

        Returns:
            bytes: The trimmed video data as bytes.

        Raises:
            RuntimeError: If video trimming fails.

        Example:
            >>> # Read video data from a file
            >>> with open("video.mp4", "rb") as f:
            ...     video_data = f.read()
            >>> 
            >>> # Trim first 30 seconds in memory
            >>> trimmed_data = ffmpeg.trims(video_data, start=0, duration=30)
            >>> 
            >>> # Save the trimmed video
            >>> with open("intro.mp4", "wb") as f:
            ...     f.write(trimmed_data)
            >>> 
            >>> # Trim with different format
            >>> webm_data = ffmpeg.trims(video_data, start=10, duration=5, format_type="webm")
            >>> with open("clip.webm", "wb") as f:
            ...     f.write(webm_data)
            >>> 
            >>> # Trim with specific codec settings
            >>> # For non-MP4 formats, FFMPEG will use default codecs
            >>> avi_data = ffmpeg.trims(video_data, start=5, duration=10, format_type="avi")
        """
        args = [
            "-y",
            "-i", "pipe:0",
            "-ss", str(start)
        ]

        if duration is not None:
            args.extend(["-t", str(duration)])

        if format_type == 'mp4':
            args.extend([
                "-c:v", v_encoder,
                "-pix_fmt", "yuv420p",
                "-c:a", a_encoder,
                "-movflags", "frag_keyframe+empty_moov"
            ])

        args.extend([
            "-f", format_type,
            "pipe:1"
        ])

        stdout, stderr = self.execute(*args, input_data=input_bytes)

        return stdout

    def extract_audio(self, input_file: str, output_file: str) -> None:
        """
        Extract audio from a video file.

        Extracts the audio track from a video file without re-encoding,
        preserving the original audio quality. The output file extension
        should match the audio codec (e.g., .m4a for AAC, .mp3 for MP3,
        .ogg for Vorbis).

        Args:
            input_file: Path to the input video file.
            output_file: Path for the output audio file.

        Raises:
            FileNotFoundError: If input file doesn't exist.
            RuntimeError: If audio extraction fails.

        Example:
            >>> # Extract audio from MP4 video
            >>> ffmpeg.extract_audio("video.mp4", "audio.m4a")
            >>> 
            >>> # Extract audio and convert to MP3
            >>> ffmpeg.execute("-i", "video.mp4", "-q:a", "0", "-map", "a", "audio.mp3")
            >>> 
            >>> # Extract audio from multiple formats
            >>> ffmpeg.extract_audio("movie.mkv", "audio.m4a")
            >>> ffmpeg.extract_audio("clip.avi", "audio.mp3")
        """
        input_path = Path(input_file)
        output_path = Path(output_file)

        if not input_path.exists():
            raise FileNotFoundError(
                f"Input file {input_file} was not found."
            )

        self.execute(
            "-i", str(input_path),  # Specifies the input video file.
            "-vn",  # Disables the video stream (drops the visual data).
            "-c:a", "copy",  # Copies the audio track as-is without re-encoding.
            str(output_path)  # Output file. Extension should match audio codec.
        )

    def extract_audios(self, input_bytes: bytes, output_format: str = "m4a") -> bytes:
        """
        Extract audio from video data (in-memory processing).

        Extracts the audio track from in-memory video data without re-encoding,
        preserving the original audio quality. This method is useful when you
        have video data in memory and want to avoid writing temporary files.

        Args:
            input_bytes: Video data as bytes to extract audio from.
            output_format: Audio output format (e.g., 'm4a', 'mp3', 'ogg', 'wav').
                          Defaults to 'm4a'.

        Returns:
            bytes: The extracted audio data as bytes.

        Raises:
            RuntimeError: If audio extraction fails.

        Example:
            >>> # Read video data from a file
            >>> with open("video.mp4", "rb") as f:
            ...     video_data = f.read()
            >>> 
            >>> # Extract audio in memory
            >>> audio_data = ffmpeg.extract_audios(video_data, output_format="m4a")
            >>> 
            >>> # Save the extracted audio
            >>> with open("audio.m4a", "wb") as f:
            ...     f.write(audio_data)
            >>> 
            >>> # Extract audio in different formats
            >>> mp3_data = ffmpeg.extract_audios(video_data, output_format="mp3")
            >>> ogg_data = ffmpeg.extract_audios(video_data, output_format="ogg")
        """
        args = [
            "-i", "pipe:0",
            "-vn",
            "-c:a", "copy",
            "-f", output_format,
            "pipe:1"
        ]

        return self.execute(*args, input_data=input_bytes)[0]

    def compress_file(self, 
                input_file : str, 
                output_file : str, 
                crf: int = 28,
                v_encoder : str = "libx264",
                a_encoder : str = "aac" ,
                px_format : str = "yuv420p"):

            args = [
                "-i", input_file,
                "-c:v", v_encoder,
                "-crf", str(crf),
                "-pix_fmt", px_format,
                "-c:a", a_encoder,
                "-movflags", "faststart",
                output_file,
            ]

            self.execute(*args)

    def compress_byte(self, 
            input_data : bytes,
            crf: int = 28,
            v_encoder : str = "libx264",
            a_encoder : str = "aac" ,
            px_format : str = "yuv420p"
            ):
        args = [
            "-i", "pipe:0",
            "-c:v", v_encoder,
            "-crf", str(crf),
            "-pix_fmt", px_format,
            "-c:a", a_encoder,
            "-movflags", "frag_keyframe+empty_moov",
            "-f", "mp4",
            "pipe:1"
        ]

        return self.execute(*args, input_data=input_data)[0]

    def verify(self, input_file : str) -> tuple[bool, str]:
        args = [
            "-v", "error",
            "-i", input_file,
            "-f",  "null",
            "-"
        ]

        try: 
            self.execute(*args)
            return True, ""
        except RuntimeError as e:
            return False, str(e)