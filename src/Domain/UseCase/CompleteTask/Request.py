class Request:

    def __init__(self, player_id: int, task_name: str) -> None:
        self.player_id: int = player_id
        self.task_name: str = task_name
