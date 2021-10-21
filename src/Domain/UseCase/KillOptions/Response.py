from typing import List


class Response:

    def __init__(self) -> None:
        self.success: bool = False
        self.error_message: str = ''
        self.kill_options: dict = {}
        self.impostors_names: List[str] = []