from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.GameExistsValidator import GameExistsValidator
from Enums.GameState import GameState


class MeetingCalledValidator(ChainValidator):

    def __init__(self) -> None:
        super().__init__([
            GameExistsValidator(),
            self.__InnerValidator()
        ])

    class __InnerValidator(BaseValidator):

        def validate(self, game: Game) -> bool:
            if game.game_state != GameState.MEETING_CALLED:
                self.error_message = 'This action can only be taken when a meeting is called'
            return not self.error_message
