from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Models.Crewmate import Crewmate
from Domain.Models.Impostor import Impostor
from Domain.UseCase.KillPlayer.Response import Response
from Domain.UseCase.KillPlayer.Request import Request
from Domain.Validators.Game.KillPlayerValidator import KillPlayerValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, request: Request) -> Response:
        response = Response()

        validator = KillPlayerValidator(request.killer_id, request.victim_id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        killer: Impostor = game.player_set.fetch(request.killer_id)
        victim: Crewmate = game.player_set.fetch(request.victim_id)
        cause_of_death = killer.kill(victim)

        response.killer_message = cause_of_death.format('You', str(victim))
        response.victim_message = cause_of_death.format(str(killer), 'You')
        response.is_game_over = game.check_for_game_over()

        self.__game_model_gateway.check_in(game)

        response.success = True
        return response
