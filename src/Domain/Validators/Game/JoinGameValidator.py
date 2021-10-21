from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.InLobbyValidator import InLobbyValidator


class JoinGameValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            InLobbyValidator(),
            self.__InnerValidator(player_id)
        ])

    class __InnerValidator(BaseValidator):

        def __init__(self, player_id: int) -> None:
            super().__init__()
            self.player_id: int = player_id

        def validate(self, game: Game) -> bool:
            if game.player_set.fetch(self.player_id):
                self.error_message = 'You are already in the game'
            elif len(game.player_set.fetch_all()) == 18:
                self.error_message = 'The game is full'

            return not self.error_message
