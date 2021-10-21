from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.JoinGameValidator import JoinGameValidator


class JoinGameAsColorValidator(ChainValidator):

    def __init__(self, player_id: int, color: str) -> None:
        super().__init__([
            JoinGameValidator(player_id),
            self.__InnerValidator(color)
        ])

    class __InnerValidator(BaseValidator):

        def __init__(self, color: str) -> None:
            super().__init__()
            self.color: str = color

        def validate(self, game: Game) -> bool:
            if next(filter(lambda player: player.color == self.color, game.player_set.fetch_all()), None):
                self.error_message = 'Someone already has that color'

            return not self.error_message
