from Domain.Validators.Game.PlayerValidator import PlayerValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.InLobbyValidator import InLobbyValidator


class LeaveGameValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            InLobbyValidator(),
            PlayerValidator(player_id)
        ])
