import subprocess
from pathlib import Path

class FFMPEG:
    def __init__(self) -> None:
        import shutil
        self.executable = shutil.which('ffmpeg')

        if self.executable is None:
            raise FileNotFoundError("""
FFmpeg is not installed or could not be found in PATH.
Please install FFmpeg and make sure it is available
in your system PATH.
""")

    @classmethod
    def api(cls):
        return cls()

    def execute(self, *args : str):
        if self.executable:
            result = subprocess.run([self.executable, *args], capture_output=True, text=True)
            return result.stdout.strip(), result.stderr.strip()

        raise FileNotFoundError("""
        No ffmpeg executable found.

        Please Install ffmpeg first.
        """)

    def reformat(self, input_file : str, output_file : str):
        if not Path(input_file).exists():
            raise FileNotFoundError(f"""
                    Input file {input_file} did not found .
            
                    Please check filename and directory if correct.
                    """)

        stdout, stderr = self.execute("-i", input_file, output_file)

        if stdout:
            print(stdout)
        else:
            print(stderr)

    def gif(self, 
            input_file : str, 
            output_file : str,
            fps = 10,
            scale = 320
            ):
        input_path = Path(input_file)
        output_path = Path(output_file)

        if not input_path.exists():
            raise FileNotFoundError(
                f"Input file {input_file} was not found."
            )

        filter_graph : str = (
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

        return stdout, stderr

    def trim(
        self,
        input_file: str,
        output_file: str,
        start: float = 0,
        duration: float | None = None,
    ):
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

        return stdout, stderr