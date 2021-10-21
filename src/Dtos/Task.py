from random import shuffle

from Enums.TaskType import TaskType


class Task:
    def __init__(self, name='', location='', description='', task_type='', order=0):
        self.name = name
        self.description = description
        self.order = order
        self.location = self.__get_order_string() if order else location

        try:
            converted_type = TaskType[task_type.upper()]
        except KeyError:
            converted_type = TaskType.NONE

        self.task_type = converted_type

    def __eq__(self, other):
        return False # assume tasks are unique

    def __ne__(self, other):
        return True

    def __lt__(self, other):
        return (self.__order[self.task_type], self.name) < (self.__order[other.task_type], other.name)

    def __le__(self, other):
        return self.__lt__(other)

    def __gt__(self, other):
        return not self.__lt__(other)

    def __ge__(self, other):
        return self.__gt__(other)

    def checklist_display_name(self) -> str:
        self.__get_order_string()
        if not self.order:
            return self.name
        return self.name + ' [' + self.__get_order_string() + ']'

    def __get_order_string(self) -> str:
        nums = [str(n + 1) for n in range(self.order)]
        shuffle(nums)
        return ' -> '.join(nums)

    __order = {
        TaskType.COMMON: 0,
        TaskType.LONG: 1,
        TaskType.SHORT: 2,
        TaskType.NONE: 3,
    }