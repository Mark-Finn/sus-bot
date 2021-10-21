from datetime import datetime
from typing import List

from Domain.Models.TaskChecklist import TaskChecklist
from Dtos.Task import Task


class Player:

    def __init__(self, id: int, name: str, color: str) -> None:
        self.id: int = id
        self.name: str = name
        self.color: str = color
        self.is_impostor = None
        self.task_checklist: TaskChecklist = TaskChecklist()
        self.emergency_meetings_called: int = 0
        self.time_of_death: datetime = datetime.min
        self.confirmed_dead: bool = False
        self.cause_of_death: str = ''

    def __hash__(self):
        return self.id

    def __str__(self):
        return f'{self.name} ({self.color})'

    def assign_tasks(self, tasks: List[Task]):
        for task in tasks:
            self.task_checklist.add_task(task.name)

    def die(self, caused_by: str):
        self.cause_of_death = caused_by
        self.time_of_death = datetime.now()

    def is_alive(self) -> bool:
        return self.time_of_death == datetime.min

