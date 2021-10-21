from typing import List
from Dtos.Task import Task


class PlayerResponse:

    def __init__(self, id: str, is_impostor: bool, tasks: List[Task]) -> None:
        self.id = id
        self.is_impostor = is_impostor
        self.tasks = tasks