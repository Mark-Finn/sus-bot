from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Models.O2Sabotage import O2Sabotage
from Domain.Models.Sabotage import Sabotage
from Domain.UseCase.BaseUrgentSabotage.UpdateResponse import UpdateResponse
from Domain.UseCase.O2Sabotage.UpdateResponse import UpdateResponse as O2UpdateResponse
from Domain.UseCase.BaseUrgentSabotage.UseCase import UseCase as BaseUrgentSabotageUseCase
from Dtos.Settings import Settings


class UseCase(BaseUrgentSabotageUseCase):

    def __init__(self, game_model_gateway: GameModelGateway) -> None:
        super().__init__(game_model_gateway)

    def _create_sabotage(self, settings: Settings) -> Sabotage:
        return O2Sabotage(settings.hypoxia_time)

    def _get_time_before_game_over(self, sabotage: Sabotage) -> float:
        return sabotage.time_before_hypoxia() if isinstance(sabotage, O2Sabotage) else 0.0

    def _update_hook(self, update_response: UpdateResponse, sabotage: Sabotage) -> UpdateResponse:
        o2_response = O2UpdateResponse()
        o2_response.time_remaining = update_response.time_remaining
        if isinstance(sabotage, O2Sabotage):
            o2_response.code1 = self.__chunk_string(str(sabotage.code1), 3)
            o2_response.code2 = self.__chunk_string(str(sabotage.code2), 3)
            o2_response.completed_codes, o2_response.required_codes = sabotage.get_completed_required_tuple()
        return o2_response

    def __chunk_string(self, string: str, n: int, glue: str=' ') -> str:
        chunks = [ string[i:i+n] for i in range(0, len(string), n) ]
        return glue.join(chunks)