from typing import List, Tuple


class Response:

    def __init__(self) -> None:
        self.success: bool = False
        self.message: str = ''
        self.is_impostor_win: bool = None
        self.winner_color_pairs: List[Tuple] = []
