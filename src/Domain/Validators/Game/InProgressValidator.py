from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.GameExistsValidator import GameExistsValidator
from Enums.GameState import GameState


class InProgressValidator(ChainValidator):

    def __init__(self) -> None:
        super().__init__([
            GameExistsValidator(),
            self.__InnerValidator()
        ])

    class __InnerValidator(BaseValidator):

        def validate(self, game: Game) -> bool:
            if game.game_state != GameState.IN_PROGRESS:
                self.error_message = 'This action can only be taken while the game is in progress'
            return not self.error_message
