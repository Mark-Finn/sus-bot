from datetime import datetime, timedelta

import math

from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.CallMeetingValidator import CallMeetingValidator


class EmergencyMeetingValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            CallMeetingValidator(player_id),
            self.__InnerValidator(player_id)
        ])

    class __InnerValidator(BaseValidator):

        def __init__(self, player_id: int) -> None:
            super().__init__()
            self.player_id: int = player_id

        def validate(self, game: Game) -> bool:
            cooldown_complete_time = game.round_start_time + timedelta(seconds=game.settings.emergency_cooldown)
            now = datetime.now()

            if game.sabotage and not game.sabotage.is_resolved:
                self.error_message = 'You cannot call an emergency meeting during an sabotage'
            elif game.player_set.fetch(self.player_id).emergency_meetings_called >= game.settings.emergency_meetings:
                self.error_message = 'You do not have any emergency meetings left'
            elif cooldown_complete_time > now:
                total_seconds = math.ceil((cooldown_complete_time - now).total_seconds())
                self.error_message = f'Cannot call an emergency meeting for another {total_seconds} second{"s" if total_seconds > 1 else ""}...'

            return not self.error_message
