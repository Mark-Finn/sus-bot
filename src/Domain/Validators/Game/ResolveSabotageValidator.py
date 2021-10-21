from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.InProgressValidator import InProgressValidator
from Domain.Validators.Game.AliveValidator import AliveValidator


class ResolveSabotageValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            InProgressValidator(),
            AliveValidator(player_id),
            self.__InnerValidator()
        ])

    class __InnerValidator(BaseValidator):

        def validate(self, game: Game) -> bool:
            if not game.sabotage:
                self.error_message = 'There is not an active sabotage'
            elif game.sabotage.is_resolved:
                self.error_message = 'The sabotage is resolved'
            return not self.error_message