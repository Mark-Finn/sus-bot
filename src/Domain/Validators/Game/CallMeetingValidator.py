from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.InProgressValidator import InProgressValidator
from Domain.Validators.Game.AliveValidator import AliveValidator


class CallMeetingValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            InProgressValidator(),
            AliveValidator(player_id),
        ])

