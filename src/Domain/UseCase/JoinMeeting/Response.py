from typing import List


class Response:

    def __init__(self) -> None:
        self.success: bool = False
        self.error_message: str = ''
        self.alive_player_count: int = 0
        self.joined_players: List[str] = []
        self.meeting_started: bool = False