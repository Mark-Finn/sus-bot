from typing import List

from Dtos.Task import Task


class Response:

    def __init__(self) -> None:
        self.success: bool = False
        self.error_message: str = ''
        self.task_list: List[Task] = []
        self.completed_task_names: List[str] = []
        self.is_game_over: bool = False

