from typing import List

from Domain.Models.Player import Player


class Crewmate(Player):

    def __init__(self, id: int, name: str, color: str) -> None:
        super().__init__(id, name, color)
        self.is_impostor: bool = False

    def complete_task(self, task_name: str):
        self.task_checklist.complete_task(task_name)

    def get_uncompleted_tasks(self) -> List[str]:
        return self.task_checklist.get_uncompleted_tasks()

    def get_completed_task_count(self) -> int:
        return self.task_checklist.get_completed_count()