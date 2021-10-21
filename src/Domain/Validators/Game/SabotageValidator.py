from datetime import datetime, timedelta

import math

from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.InProgressValidator import InProgressValidator
from Domain.Validators.Game.ImpostorValidator import ImpostorValidator


class SabotageValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            InProgressValidator(),
            ImpostorValidator(player_id),
            self.__InnerValidator()
        ])

    class __InnerValidator(BaseValidator):

        def validate(self, game: Game) -> bool:
            sabotage = game.sabotage
            if not sabotage:
                return True

            cooldown_complete_time = sabotage.end_time + timedelta(seconds=game.settings.sabotage_cooldown)
            now = datetime.now()

            if not sabotage.is_resolved:
                self.error_message = 'There is already a sabotage in progress'
            elif cooldown_complete_time > now:
                total_seconds = math.ceil((cooldown_complete_time - now).total_seconds())
                self.error_message = f'Sabotage off cooldown in {total_seconds} second{"s" if total_seconds > 1 else ""}...'

            return not self.error_message
