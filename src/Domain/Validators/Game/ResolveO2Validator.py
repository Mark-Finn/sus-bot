from Domain.Models.Game import Game
from Domain.Models.O2Sabotage import O2Sabotage
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.ResolveSabotageValidator import ResolveSabotageValidator


class ResolveO2Validator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            ResolveSabotageValidator(player_id),
            self.__InnerValidator()
        ])

    class __InnerValidator(BaseValidator):

        def validate(self, game: Game) -> bool:
            if not isinstance(game.sabotage, O2Sabotage):
                self.error_message = 'The current sabotage is not an O2 sabotage'

            return not self.error_message
