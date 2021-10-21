from typing import List

from Dtos.Task import Task
from Enums.TaskType import TaskType


class TaskSet:
    
    def __init__(self, tasks: dict=None) -> None:
        self.tasks = tasks or {}
        
    def update(self, task: Task):
        self.tasks[task.name] = task

    def fetch(self, name: str) -> Task:
        return self.tasks[name]

    def fetch_all(self, task_type_filter:TaskType=None) -> List[Task]:
        values = list(self.tasks.values())
        if not task_type_filter:
            return values
        return list(filter(lambda task: task.task_type == task_type_filter, values))

    def fetch_all_names(self) -> List[str]:
        return list(self.tasks.keys())