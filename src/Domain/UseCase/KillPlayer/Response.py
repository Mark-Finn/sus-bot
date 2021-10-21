class Response:

    def __init__(self) -> None:
        self.success: bool = False
        self.error_message: str = ''
        self.killer_message: str = ''
        self.victim_message: str = ''
        self.is_game_over: bool = False