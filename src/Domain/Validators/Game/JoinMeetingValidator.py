from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.MeetingCalledValidator import MeetingCalledValidator
from Domain.Validators.Game.AliveValidator import AliveValidator


class JoinMeetingValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            MeetingCalledValidator(),
            AliveValidator(player_id),
            self.__InnerValidator(player_id)
        ])

    class __InnerValidator(BaseValidator):

        def __init__(self, player_id: int) -> None:
            super().__init__()
            self.player_id: int = player_id

        def validate(self, game: Game) -> bool:
            if game.current_meeting.has_player_joined(self.player_id):
                self.error_message = 'You are already in the meeting'
            return not self.error_message
