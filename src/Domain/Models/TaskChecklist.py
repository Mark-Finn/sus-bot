from typing import List


class TaskChecklist:

    def __init__(self) -> None:
        self.task_checklist: dict = {}

    def add_task(self, task_name: str):
        self.task_checklist[task_name] = False

    def complete_task(self, task_name: str):
        self.task_checklist[task_name] = True

    def get_all(self) -> List[str]:
        return list(self.task_checklist.keys())

    def has_task(self, task_name: str) -> bool:
        return task_name in self.task_checklist

    def is_completed(self, task_name: str) -> bool:
        return self.has_task(task_name) and self.task_checklist[task_name]

    def get_uncompleted_tasks(self) -> List[str]:
        return self.__get_tasks(get_completed=False)

    def get_completed_tasks(self) -> List[str]:
        return self.__get_tasks(get_completed=True)

    def get_completed_count(self) -> int:
        return len(self.get_completed_tasks())

    def __get_tasks(self, get_completed: bool):
        return [name for (name, completed) in self.task_checklist.items() if completed == get_completed]