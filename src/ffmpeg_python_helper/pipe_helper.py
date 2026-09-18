from typing import Callable


class Pipe:
    """
    A utility class for piping bytes through multiple processing functions.

    This class provides a convenient way to chain multiple byte-processing
    operations together, creating a pipeline that transforms data step by step.

    Example:
        >>> from ffmpeg_python_helper import FFMPEG, Pipe
        >>> ffmpeg = FFMPEG()
        >>> 
        >>> # Define processing functions
        >>> def trim_first_30s(data: bytes) -> bytes:
        ...     return ffmpeg.trims(data, start=0, duration=30)
        >>> 
        >>> def convert_to_gif(data: bytes) -> bytes:
        ...     return ffmpeg.gifs(data, fps=15, scale=480)
        >>> 
        >>> def extract_audio(data: bytes) -> bytes:
        ...     return ffmpeg.extract_audios(data, output_format="m4a")
        >>> 
        >>> # Read video data
        >>> with open("video.mp4", "rb") as f:
        ...     video_data = f.read()
        >>> 
        >>> # Create a processing pipeline
        >>> # Trim → Convert to GIF → Extract audio
        >>> result = Pipe.pipe_bytes(
        ...     video_data,
        ...     trim_first_30s,
        ...     convert_to_gif,
        ...     extract_audio
        ... )
        >>> 
        >>> # Save the final result (audio from trimmed GIF-converted video)
        >>> with open("processed_audio.m4a", "wb") as f:
        ...     f.write(result)
    """

    @staticmethod
    def pipe_bytes(initial_value: bytes, *fn: Callable[[bytes], bytes]) -> bytes:
        """
        Pipe bytes through multiple processing functions.

        This method takes an initial bytes value and passes it through
        a series of functions, using the output of each function as the
        input to the next function in the chain.

        Args:
            initial_value: The initial bytes to start the pipeline with.
            *fn: One or more callable functions that take bytes as input
                 and return bytes as output. Functions are applied in
                 the order they are provided.

        Returns:
            bytes: The final result after passing through all functions.

        Raises:
            TypeError: If any function is not callable or doesn't accept bytes.
            RuntimeError: If any function in the pipeline fails.

        Example:
            >>> # Simple pipeline: read, process, save
            >>> def add_header(data: bytes) -> bytes:
            ...     return b"HEADER" + data
            >>> 
            >>> def add_footer(data: bytes) -> bytes:
            ...     return data + b"FOOTER"
            >>> 
            >>> def uppercase_data(data: bytes) -> bytes:
            ...     return data.upper()
            >>> 
            >>> # Create pipeline
            >>> result = Pipe.pipe_bytes(
            ...     b"hello world",
            ...     add_header,
            ...     uppercase_data,
            ...     add_footer
            ... )
            >>> 
            >>> print(result)
            b'HEADERHELLO WORLD FOOTER'

            >>> # FFMPEG processing pipeline
            >>> from ffmpeg_python_helper import FFMPEG
            >>> ffmpeg = FFMPEG()
            >>> 
            >>> def trim_video(data: bytes) -> bytes:
            ...     return ffmpeg.trims(data, start=10, duration=5)
            >>> 
            >>> def convert_to_webm(data: bytes) -> bytes:
            ...     return ffmpeg.trims(data, format_type="webm")  # Re-encode as webm
            >>> 
            >>> # Process video through pipeline
            >>> with open("input.mp4", "rb") as f:
            ...     video_data = f.read()
            >>> 
            >>> processed_data = Pipe.pipe_bytes(
            ...     video_data,
            ...     trim_video,
            ...     convert_to_webm
            ... )
            >>> 
            >>> with open("output.webm", "wb") as f:
            ...     f.write(processed_data)
        """
        current: bytes = initial_value
        for callable in fn:
            current = callable(current)

        return current