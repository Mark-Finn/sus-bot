from typing import Optional

from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.NowVotingValidator import NowVotingValidator
from Domain.Validators.Game.AliveValidator import AliveValidator


class VoteValidator(ChainValidator):

    def __init__(self, player_id: int, recipient_id: Optional[int]) -> None:
        validators = [
            NowVotingValidator(),
            AliveValidator(player_id),
            self.__InnerValidator(player_id)
        ]
        if recipient_id:
            validators.append(AliveValidator(recipient_id, is_targeted_by_action=True))
        super().__init__(validators)

    class __InnerValidator(BaseValidator):

        def __init__(self, player_id: int) -> None:
            super().__init__()
            self.player_id: int = player_id

        def validate(self, game: Game) -> bool:
            if game.current_meeting.has_vote(self.player_id):
                self.error_message = 'You already voted in this meeting'
            return not self.error_message
