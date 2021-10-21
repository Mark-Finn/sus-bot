class Request:

    def __init__(self, player_id: int, switch_number: int) -> None:
        self.player_id: int = player_id
        self.switch_number: int = switch_number
