class Response:

    def __init__(self):
        self.success: bool = False
        self.error_message: str = ''
        self.alive_player_count: int = 0
        self.caller_name: str = ''
        self.caller_color: str = ''