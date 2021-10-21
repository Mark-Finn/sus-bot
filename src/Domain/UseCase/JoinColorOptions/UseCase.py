from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.JoinColorOptions.Response import Response
from Domain.Validators.Game.JoinGameValidator import JoinGameValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, id: int) -> Response:
        response = Response()

        validator = JoinGameValidator(id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        taken_colors = map(lambda player: player.color, game.player_set.fetch_all())

        response.color_options = list(set(self.__color_options()) - set(taken_colors))
        self.__game_model_gateway.check_in(game)

        response.success = True
        return response

    def __color_options(self):
        return [
            'Red',
            'Blue',
            'Green',
            'Pink',
            'Orange',
            'Yellow',
            'Black',
            'White',
            'Purple',
            'Brown',
            'Cyan',
            'Lime',
            'Maroon',
            'Rose',
            'Banana',
            'Gray',
            'Tan',
            'Coral',
        ]