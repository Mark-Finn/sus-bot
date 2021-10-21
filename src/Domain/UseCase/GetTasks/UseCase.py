import copy
from typing import List

from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Gateway.Tasks.Gateway import Gateway as TaskGateway
from Dtos.Task import Task


class UseCase:

    def __init__(self,
                 game_model_gateway: GameModelGateway,
                 task_gateway: TaskGateway):
        self.__game_model_gateway = game_model_gateway
        self.__task_gateway = task_gateway

    def execute(self) -> List[Task]:
        game = self.__game_model_gateway.read_only()

        if game:
            tasks = game.all_tasks
        else:
            tasks = self.__task_gateway.fetch()

        tasks.sort()

        return copy.deepcopy(tasks)

    def __task_compare(self):
        pass