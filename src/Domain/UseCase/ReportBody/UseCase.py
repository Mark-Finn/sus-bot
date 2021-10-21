from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.ReportBody.Request import Request
from Domain.UseCase.ReportBody.Response import Response
from Domain.Validators.Game.ReportBodyValidator import ReportBodyValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, request: Request) -> Response:
        response = Response()

        validator = ReportBodyValidator(request.player_id, request.body_id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        player = game.player_set.fetch(request.player_id)
        body = game.player_set.fetch(request.body_id)
        game.call_meeting(player, body)

        response.body_name = str(body)
        response.caller_name = str(player)
        response.caller_color = player.color
        response.alive_player_count = game.player_set.alive_count()

        self.__game_model_gateway.check_in(game)
        response.success = True
        return response
