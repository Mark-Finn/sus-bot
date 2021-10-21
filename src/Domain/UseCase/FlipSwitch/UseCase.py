import copy

from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.FlipSwitch.Request import Request
from Domain.UseCase.FlipSwitch.Response import Response
from Domain.Validators.Game.ResolveElectricalValidator import ResolveElectricalValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, request: Request) -> Response:
        response = Response()

        game = await self.__game_model_gateway.check_out()

        validator = ResolveElectricalValidator(request.player_id)

        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        game.sabotage.flip_switch(request.switch_number)

        response.switch_states = copy.copy(game.sabotage.switch_states)
        response.is_resolved = game.sabotage.is_resolved

        self.__game_model_gateway.check_in(game)
        response.success = True
        return response