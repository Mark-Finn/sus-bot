from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.PressReactorButton import Request
from Domain.UseCase.TextResponse import TextResponse
from Domain.Validators.Game.ResolveReactorValidator import ResolveReactorValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, request: Request) -> TextResponse:
        response = TextResponse()

        validator = ResolveReactorValidator(request.player_id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        if request.is_left_button:
            game.sabotage.press_left(request.player_id)
            side = 'left'
        else:
            game.sabotage.press_right(request.player_id)
            side = 'right'

        response.message = f'You are holding the {side} button for {game.sabotage.depress_time} seconds...'

        self.__game_model_gateway.check_in(game)

        response.success = True
        return response
