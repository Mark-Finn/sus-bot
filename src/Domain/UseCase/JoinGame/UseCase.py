from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.JoinGame.Request import Request
from Domain.UseCase.JoinGame.Response import Response
from Domain.Validators.Game.JoinGameAsColorValidator import JoinGameAsColorValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, request: Request) -> Response:
        response = Response()

        validator = JoinGameAsColorValidator(request.id, request.color)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        game.add_player(request.id, request.name, request.color)

        response.player_list = list(map(lambda player: str(player), game.player_set.fetch_all()))
        self.__game_model_gateway.check_in(game)

        response.success = True
        return response
