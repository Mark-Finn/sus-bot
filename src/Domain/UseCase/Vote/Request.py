from typing import Optional


class Request:

    def __init__(self, player_id: int, recipient_id: Optional[int]=None) -> None:
        self.player_id: int = player_id
        self.recipient_id: Optional[int] = recipient_id

    @staticmethod
    def create_skip_vote(player_id: int):
        return Request(player_id)

    @staticmethod
    def create_vote_for_player(player_id: int, recipient_id: int):
        return Request(player_id, recipient_id)
