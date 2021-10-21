from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.KillValidator import KillValidator
from Domain.Validators.Game.CrewmateValidator import CrewmateValidator
from Domain.Validators.Game.AliveValidator import AliveValidator


class KillPlayerValidator(ChainValidator):

    def __init__(self, player_id: int, victim_id: int) -> None:
        super().__init__([
            KillValidator(player_id),
            CrewmateValidator(victim_id, is_targeted_by_action=True),
            AliveValidator(victim_id, is_targeted_by_action=True),
        ])
