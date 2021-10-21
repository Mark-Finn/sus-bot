from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.KillOptions.Response import Response
from Domain.Validators.Game.KillValidator import KillValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, id: int) -> Response:
        response = Response()

        validator = KillValidator(id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        crewmates = game.player_set.fetch_crewmates()
        for crewmate in crewmates:
            if crewmate.is_alive():
                response.kill_options[crewmate.id] = str(crewmate)

        response.impostors_names = list(map(lambda player: player.name, game.player_set.fetch_impostors()))

        self.__game_model_gateway.check_in(game)

        response.success = True
        return response
