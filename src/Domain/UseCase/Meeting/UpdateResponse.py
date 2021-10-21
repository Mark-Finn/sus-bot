from typing import List


class UpdateResponse:

    def __init__(self) -> None:
        self.player_options: dict = {}
        self.time_remaining: int = 0
        self.is_voting: bool = False
        self.voters: List[str] = []