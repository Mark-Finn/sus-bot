from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.DeadValidator import DeadValidator
from Domain.Validators.Game.ReportValidator import ReportValidator


class ReportBodyValidator(ChainValidator):

    def __init__(self, player_id: int, body_id: int) -> None:
        super().__init__([
            ReportValidator(player_id),
            DeadValidator(body_id),
            self.__InnerValidator(body_id)
        ])

    class __InnerValidator(BaseValidator):

        def __init__(self, body_id: int) -> None:
            super().__init__()
            self.body_id: int = body_id

        def validate(self, game: Game) -> bool:
            if game.player_set.fetch(self.body_id).confirmed_dead:
                self.error_message = 'Player died in a previous round'
            return not self.error_message
