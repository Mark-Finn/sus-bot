from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.PlayerValidator import PlayerValidator


class ImpostorValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            PlayerValidator(player_id),
            self.__InnerValidator(player_id)
        ])

    class __InnerValidator(BaseValidator):

        def __init__(self, player_id: int) -> None:
            super().__init__()
            self.player_id: int = player_id

        def validate(self, game: Game) -> bool:
            if not game.player_set.fetch(self.player_id).is_impostor:
                self.error_message = 'This action can only be taken by impostors'
            return not self.error_message
