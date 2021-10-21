from typing import List

from Dtos.Task import Task
from Enums.TaskType import TaskType
from Gateway.BaseJson.Encoder import Encoder as BaseEncoder


class Encoder(BaseEncoder):

    def _encode_object(self, obj):
        if isinstance(obj, TaskType):
            return obj.value
        else:
            return super()._encode_object(obj)

    def _get_keys(self, lst: List[Task]) -> List[str]:
        return lst(map(lambda task: task.name, lst))