class Request:

    def __init__(self, player_id: int, is_left_button: bool) -> None:
        self.player_id: int = player_id
        self.is_left_button: bool = is_left_button
