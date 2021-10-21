from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator


class GameExistsValidator(BaseValidator):

    def validate(self, game: Game):
        if not game:
            self.error_message = 'No game was found'
        return not self.error_message