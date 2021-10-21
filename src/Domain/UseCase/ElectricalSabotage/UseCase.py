import copy

from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Models.ElectricalSabotage import ElectricalSabotage
from Domain.UseCase.ElectricalSabotage.Response import Response
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

        game.sabotage = ElectricalSabotage()

        response.switch_states = copy.copy(game.sabotage.switch_states)

        self.__game_model_gateway.check_in(game)
        response.success = True
        return response