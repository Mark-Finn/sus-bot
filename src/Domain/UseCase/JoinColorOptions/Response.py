from typing import List


class Response:

    def __init__(self) -> None:
        self.success: bool = False
        self.error_message: str = ''
        self.color_options: List[str] = []