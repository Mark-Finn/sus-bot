from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.PlayerValidator import PlayerValidator


class AliveValidator(ChainValidator):
    def __init__(self, player_id: int, is_targeted_by_action: bool=False) -> None:
        super().__init__([
            PlayerValidator(player_id),
            self.__InnerValidator(player_id, is_targeted_by_action)
        ])

    class __InnerValidator(BaseValidator):
        def __init__(self, player_id: int, is_targeted_by_action: bool=False) -> None:
            super().__init__()
            self.player_id: int = player_id
            self.is_targeted_by_action: bool = is_targeted_by_action

        def validate(self, game: Game) -> bool:
            if not game.player_set.fetch(self.player_id).is_alive():
                if self.is_targeted_by_action:
                    self.error_message = 'This action can only effect alive players'
                else:
                    self.error_message = 'This action can only be taken while alive'
            return not self.error_message
