from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Models.ReactorSabotage import ReactorSabotage
from Domain.Models.Sabotage import Sabotage
from Domain.UseCase.BaseUrgentSabotage.UseCase import UseCase as BaseUrgentSabotageUseCase
from Dtos.Settings import Settings


class UseCase(BaseUrgentSabotageUseCase):

    def __init__(self, game_model_gateway: GameModelGateway):
        super().__init__(game_model_gateway)

    def _create_sabotage(self, settings: Settings) -> Sabotage:
        return ReactorSabotage(settings.meltdown_time)

    def _get_time_before_game_over(self, sabotage: Sabotage) -> float:
        return sabotage.time_before_meltdown() if isinstance(sabotage, ReactorSabotage) else 0.0