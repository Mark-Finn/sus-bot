class Request:

    def __init__(self, player_id: int, rotation: int) -> None:
        self.player_id: int = player_id
        self.rotation: int = rotation
