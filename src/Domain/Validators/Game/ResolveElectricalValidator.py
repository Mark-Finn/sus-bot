from Domain.Models.Game import Game
from Domain.Models.ElectricalSabotage import ElectricalSabotage
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.ResolveSabotageValidator import ResolveSabotageValidator


class ResolveElectricalValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            ResolveSabotageValidator(player_id),
            self.__InnerValidator()
        ])

    class __InnerValidator(BaseValidator):

        def validate(self, game: Game) -> bool:
            if not isinstance(game.sabotage, ElectricalSabotage):
                self.error_message = 'The current sabotage is not an electrical sabotage'

            return not self.error_message
