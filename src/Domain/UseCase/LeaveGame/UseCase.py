from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.LeaveGame.Response import Response
from Domain.Validators.Game.LeaveGameValidator import LeaveGameValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, id: int) -> Response:
        response = Response()

        validator = LeaveGameValidator(id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        game.player_set.remove(id)

        response.player_list = list(map(lambda player: str(player), game.player_set.fetch_all()))
        self.__game_model_gateway.check_in(game)

        response.success = True
        return response
