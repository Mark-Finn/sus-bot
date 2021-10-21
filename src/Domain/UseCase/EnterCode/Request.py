class Request:

    def __init__(self, player_id: int, code: int) -> None:
        self.player_id: int = player_id
        self.code: int = code
