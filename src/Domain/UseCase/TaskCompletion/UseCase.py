from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.TaskCompletion.Response import Response
from Domain.Validators.Game.GameExistsValidator import GameExistsValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self) -> Response:
        response = Response()

        validator = GameExistsValidator()

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        response.total_task_count = game.total_tasks()
        response.completed_task_count = game.get_completed_task_count()

        self.__game_model_gateway.check_in(game)
        response.success = True
        return response

