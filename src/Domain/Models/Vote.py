from datetime import datetime
from typing import Optional

from Domain.Models.Player import Player


class Vote:

    def __init__(self, voter: Player, recipient: Optional[Player]=None) -> None:
        self.voter: Player = voter
        self.recipient: Optional[Player] = recipient
        self.vote_time: datetime = datetime.now()

    def __str__(self):
        choice = f'for {str(self.recipient)}' if self.recipient else 'to skip'
        return f'{str(self.voter)} votes {choice} at {str(self.vote_time)}'