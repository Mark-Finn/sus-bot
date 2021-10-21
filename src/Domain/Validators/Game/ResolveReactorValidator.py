from Domain.Models.Game import Game
from Domain.Models.ReactorSabotage import ReactorSabotage
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.ResolveSabotageValidator import ResolveSabotageValidator


class ResolveReactorValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            ResolveSabotageValidator(player_id),
            self.__InnerValidator()
        ])

    class __InnerValidator(BaseValidator):

        def validate(self, game: Game) -> bool:
            if not isinstance(game.sabotage, ReactorSabotage):
                self.error_message = 'The current sabotage is not a reactor sabotage'

            return not self.error_message
