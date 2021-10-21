import copy

from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Models.ComSabotage import ComSabotage
from Domain.UseCase.ComSabotage.Response import Response
from Domain.Validators.Game.SabotageValidator import SabotageValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, player_id: int) -> Response:
        response = Response()

        game = await self.__game_model_gateway.check_out()

        validator = SabotageValidator(player_id)

        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        game.sabotage = ComSabotage()

        response.rotation_options = game.sabotage.ROTATION_OPTIONS

        self.__game_model_gateway.check_in(game)
        response.success = True
        return response