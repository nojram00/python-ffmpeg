from typing import Callable

class Pipe:

    @staticmethod
    def pipe_bytes(initial_value : bytes, *fn : Callable[[bytes], bytes]):
        current : bytes = initial_value
        for callable in fn:
            current = callable(current)

        return current