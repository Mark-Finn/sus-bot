import re

from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.CompleteTask.Request import Request
from Domain.UseCase.CompleteTask.Response import Response
from Domain.Validators.Game.CompleteTaskValidator import CompleteTaskValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, request: Request) -> Response:
        response = Response()

        request.task_name = re.sub(r'\s\[(\d| -> )*\]$', '', request.task_name) # removes order at end of task name
        validator = CompleteTaskValidator(request.player_id, request.task_name)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        checklist = game.player_set.fetch(request.player_id).task_checklist
        checklist.complete_task(request.task_name)

        task_names = checklist.get_all()
        response.task_list = list(filter(lambda task: task.name in task_names, game.all_tasks))
        response.completed_task_names = checklist.get_completed_tasks()
        response.is_game_over = game.check_for_game_over()

        self.__game_model_gateway.check_in(game)
        response.success = True
        return response
