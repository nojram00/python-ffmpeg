import subprocess
from pathlib import Path


class FFProbe:
    """
    A Python wrapper for FFProbe (FFMPEG's multimedia stream analyzer) that provides
    video metadata analysis capabilities.

    This class automatically detects FFProbe installation in the system PATH
    and provides methods for extracting video metadata, analyzing video properties,
    and checking video characteristics.

    Example:
        >>> from ffmpeg_python_helper import FFProbe
        >>> ffprobe = FFProbe()
        >>> # Check if video is short enough for social media
        >>> if ffprobe.is_max_length("video.mp4", max_length=5.0):
        ...     print("Video is perfect for Instagram Reels!")
        >>> # Get video metadata
        >>> import json
        >>> stdout, stderr = ffprobe.execute("-v", "quiet", "-print_format", "json", 
        ...                                  "-show_format", "-show_streams", "video.mp4")
        >>> metadata = json.loads(stdout.decode())
        >>> print(f"Video duration: {metadata['format']['duration']} seconds")
        >>> print(f"Video dimensions: {metadata['streams'][0]['width']}x{metadata['streams'][0]['height']}")

    Attributes:
        executable (str): The path to the FFProbe executable found in the system PATH.
    """

    def __init__(self) -> None:
        """
        Initialize a new FFProbe instance.

        Automatically searches for FFProbe in the system PATH.

        Raises:
            FileNotFoundError: If FFProbe is not found in the system PATH.

        Example:
            >>> try:
            ...     ffprobe = FFProbe()
            ...     print(f"FFProbe found at: {ffprobe.executable}")
            ... except FileNotFoundError as e:
            ...     print(f"FFProbe not found: {e}")
        """
        import shutil
        self.executable = shutil.which('ffprobe')

        if self.executable is None:
            raise FileNotFoundError("""
FFProbe is not installed or could not be found in PATH.
Please install FFmpeg and make sure it is available
in your system PATH.
""")

    @classmethod
    def api(cls) -> "FFProbe":
        """
        Factory method that returns a new FFProbe instance.

        Returns:
            FFProbe: A new instance of the FFProbe class.

        Example:
            >>> ffprobe = FFProbe.api()
            >>> ffprobe.execute("-version")
        """
        return cls()

    def execute(self, *args: str, input_data: bytes | None = None) -> tuple[bytes, bytes]:
        """
        Execute raw FFProbe commands with the given arguments.

        This method allows you to run any FFProbe command directly,
        providing maximum flexibility for metadata analysis operations
        not covered by the built-in methods.

        Args:
            *args: FFProbe command-line arguments as strings.
            input_data: Optional bytes to send to FFProbe's stdin. Useful for
                       analyzing data directly without intermediate files.

        Returns:
            tuple[bytes, bytes]: A tuple containing (stdout, stderr) from FFProbe
                                 as bytes objects.

        Raises:
            FileNotFoundError: If FFProbe executable is not found.
            RuntimeError: If FFProbe command returns a non-zero exit code.

        Example:
            >>> stdout, stderr = ffprobe.execute("-version")
            >>> print(stdout.decode())

            >>> # Get video metadata in JSON format
            >>> stdout, stderr = ffprobe.execute("-v", "quiet", "-print_format", "json",
            ...                                  "-show_format", "-show_streams", "video.mp4")
            >>> import json
            >>> metadata = json.loads(stdout.decode())
            >>> print(f"Video duration: {metadata['format']['duration']} seconds")

            >>> # Get video dimensions
            >>> stdout, stderr = ffprobe.execute("-v", "error", "-select_streams", "v:0",
            ...                                  "-show_entries", "stream=width,height",
            ...                                  "-of", "csv=p=0", "video.mp4")
            >>> print(f"Video dimensions: {stdout.decode().strip()}")
        """
        if self.executable:
            result = subprocess.run(
                [self.executable, *args], 
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                text=True
                )

            if result.returncode != 0:
                raise RuntimeError(
                    result.stderr.decode(errors="replace")
                )
            
            return result.stdout, result.stderr

        raise FileNotFoundError("""
        No ffprobe executable found.

        Please Install FFmpeg (which includes ffprobe) first.
        """)

    def is_max_length(self, input_file : str, max_length : float = 5.0) -> bool:
        """
        Check if a video file's duration is less than or equal to a specified maximum length.

        Args:
            input_file: Path to the input video file
            max_length: Maximum allowed duration in seconds (default: 5.0)

        Returns:
            bool: True if video duration ≤ max_length, False otherwise

        Raises:
            FileNotFoundError: If input file doesn't exist
            RuntimeError: If FFProbe command fails

        Example:
            >>> if ffprobe.is_max_length("video.mp4", max_length=10.0):
            ...     print("Video is short enough for social media upload")
            ... else:
            ...     print("Video is too long, needs trimming")
        """
        args = [
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_file,
        ]

        stdout, stderr = self.execute(*args)

        duration = float(stdout.strip())

        return duration <= max_length


    