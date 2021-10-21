from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator


class PlayerValidator(BaseValidator):

    def __init__(self, player_id: int, is_targeted_by_action: bool=False) -> None:
        super().__init__()
        self.player_id = player_id
        self.is_targeted_by_action: bool = is_targeted_by_action

    def validate(self, game: Game) -> bool:
        if not game.player_set.fetch(self.player_id):
            if self.is_targeted_by_action:
                self.error_message = 'This action can only effect players in the game'
            else:
                self.error_message = 'You must be in the game to take this action'
        return not self.error_message
