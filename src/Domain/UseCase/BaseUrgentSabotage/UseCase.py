import math
from abc import ABC, abstractmethod

from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Models.Sabotage import Sabotage
from Domain.UseCase.BaseUrgentSabotage.ErrorResponse import ErrorResponse
from Domain.UseCase.BaseUrgentSabotage.FinalResponse import FinalResponse
from Domain.UseCase.BaseUrgentSabotage.UpdateResponse import UpdateResponse
from Domain.Validators.Game.SabotageValidator import SabotageValidator
from Dtos.Settings import Settings
from Enums.GameState import GameState


class UseCase(ABC):

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, player_id: int):
        game = await self.__game_model_gateway.check_out()

        validator = SabotageValidator(player_id)

        if not validator.validate(game):
            response = ErrorResponse()
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            yield response
        else:
            game.sabotage = self._create_sabotage(game.settings)
            update_response = UpdateResponse()
            while True:
                update_response.time_remaining = math.ceil(self._get_time_before_game_over(game.sabotage))
                game_in_progress = game.game_state == GameState.IN_PROGRESS

                if not update_response.time_remaining or game.sabotage.is_resolved or not game_in_progress:
                    break

                self.__game_model_gateway.check_in(game)

                yield self._update_hook(update_response, game.sabotage)

                game = await self.__game_model_gateway.check_out()

            final_response = FinalResponse()

            if not game.sabotage.is_resolved and not update_response.time_remaining:
                game.impostors_win = True
                game.end()
                final_response.is_game_over = True
            elif not game.sabotage.is_resolved:
                game.sabotage.resolve()

            self.__game_model_gateway.check_in(game)
            yield final_response

    @abstractmethod
    def _create_sabotage(self, settings: Settings) -> Sabotage:
        pass

    @abstractmethod
    def _get_time_before_game_over(self, sabotage: Sabotage) -> float:
        pass

    def _update_hook(self, update_response: UpdateResponse, sabotage: Sabotage) -> UpdateResponse:
        return update_response