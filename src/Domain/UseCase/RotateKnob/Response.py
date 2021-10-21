from typing import List


class Response:

    def __init__(self) -> None:
        self.success: bool = False
        self.message: str = ''
        self.is_resolved: bool = False
