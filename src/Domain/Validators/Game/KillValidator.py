from datetime import datetime, timedelta

import math

from Domain.Models.Game import Game
from Domain.Models.Impostor import Impostor
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.InProgressValidator import InProgressValidator
from Domain.Validators.Game.ImpostorValidator import ImpostorValidator
from Domain.Validators.Game.AliveValidator import AliveValidator


class KillValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            InProgressValidator(),
            ImpostorValidator(player_id),
            AliveValidator(player_id),
            self.__InnerValidator(player_id)
        ])

    class __InnerValidator(BaseValidator):

        def __init__(self, player_id: int) -> None:
            super().__init__()
            self.player_id: int = player_id

        def validate(self, game: Game) -> bool:
            impostor: Impostor = game.player_set.fetch(self.player_id)

            last_cooldown_event = max([impostor.get_last_kill_time(), game.round_start_time])
            cooldown_complete_time = last_cooldown_event + timedelta(seconds=game.settings.kill_cooldown)

            now = datetime.now()

            if cooldown_complete_time > now:
                total_seconds = math.ceil((cooldown_complete_time - now).total_seconds())
                self.error_message = f'Kill off cooldown in {total_seconds} second{"s" if total_seconds > 1 else ""}...'

            return not self.error_message
