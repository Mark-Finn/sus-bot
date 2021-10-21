class Request:

    def __init__(self, player_id: int, body_id: int) -> None:
        self.player_id: int = player_id
        self.body_id: int = body_id
