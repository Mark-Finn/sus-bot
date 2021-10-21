from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.TextResponse import TextResponse
from Domain.Validators.Game.SabotageValidator import SabotageValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, player_id: int) -> TextResponse:
        response = TextResponse()

        validator = SabotageValidator(player_id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.message = validator.error_message
        else:
            response.success = True

        self.__game_model_gateway.check_in(game)
        return response
