from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.EndGame.Response import Response
from Domain.Validators.Game.GameExistsValidator import GameExistsValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self) -> Response:
        response = Response()

        validator = GameExistsValidator()

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        game.end()

        if game.impostors_win is None:
            response.message = 'Game Ended'
        else:
            if game.impostors_win:
                winners = game.player_set.fetch_impostors()
                response.message = 'Impostors win!\r\n'
            else:
                winners = game.player_set.fetch_crewmates()
                response.message = 'Crewmates win!\r\n'

            response.is_impostor_win = game.impostors_win
            response.message += ', '.join(map(lambda player: str(player), winners))
            response.winner_color_pairs = list(map(lambda player: (player.name, player.color), winners))

        self.__game_model_gateway.check_in(game)
        response.success = True
        return response
