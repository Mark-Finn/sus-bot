from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.EnterCode.Request import Request
from Domain.UseCase.TextResponse import TextResponse
from Domain.Validators.Game.ResolveO2Validator import ResolveO2Validator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, request: Request) -> TextResponse:
        response = TextResponse()
        game = await self.__game_model_gateway.check_out()

        validator = ResolveO2Validator(request.player_id)

        if not validator.validate(game):
            response.success = False
            response.message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        response.message = 'Code Accepted' if game.sabotage.enter_code(request.code) else 'Incorrect Code'

        self.__game_model_gateway.check_in(game)

        response.success = True
        return response