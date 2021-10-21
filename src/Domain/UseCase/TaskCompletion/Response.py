from typing import List
from Domain.UseCase.StartGame.PlayerResponse import PlayerResponse


class Response:

    def __init__(self) -> None:
        self.success: bool = False
        self.error_message: str = ''
        self.total_task_count: int = 0
        self.completed_task_count: int = 0