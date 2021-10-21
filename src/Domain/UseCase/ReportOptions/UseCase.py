from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.ReportOptions.Response import Response
from Domain.Validators.Game.ReportValidator import ReportValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, player_id: int) -> Response:
        response = Response()

        validator = ReportValidator(player_id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        options = filter(lambda player: player.id != player_id, game.player_set.fetch_possibly_alive())
        response.report_options = {player.id: str(player) for player in options}

        self.__game_model_gateway.check_in(game)

        response.success = True
        return response
