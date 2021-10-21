from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.TaskOptions.Response import Response
from Domain.Validators.Game.TaskValidator import TaskValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, player_id: int) -> Response:
        response = Response()

        validator = TaskValidator(player_id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        checklist = game.player_set.fetch(player_id).task_checklist

        uncompleted_names = checklist.get_uncompleted_tasks()
        tasks = filter(lambda task: task.name in uncompleted_names, game.all_tasks)
        response.task_options = list(map(lambda task: task.checklist_display_name(), tasks))

        self.__game_model_gateway.check_in(game)

        response.success = True
        return response
