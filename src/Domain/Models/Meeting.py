from datetime import datetime
from typing import List,  Optional

from Domain.Models.Player import Player
from Domain.Models.Vote import Vote


class Meeting:

    def __init__(self, meeting_caller: Player, body_found: Optional[Player]=None) -> None:
        self.meeting_caller: Player = meeting_caller
        self.body_found: Player = body_found
        self.is_emergency_meeting = not body_found
        self.players_joined: List[int] = []
        self.votes: dict = {}
        self.meeting_called_time: datetime = datetime.now()
        self.meeting_start_time: datetime = datetime.min
        self.meeting_end_time: datetime = datetime.min
        self.no_ejection_reason: str = ''
        self.__vote_counts: dict = {}

    def add_player(self, id: int):
        self.players_joined.append(id)

    def has_player_joined(self, id: int) -> bool:
        return id in self.players_joined

    def player_count(self) -> int:
        return len(self.players_joined)

    def add_vote(self, vote: Vote):
        self.votes[vote.voter] = vote

        recipient = vote.recipient.id if vote.recipient else 'skip'
        if recipient not in self.__vote_counts:
            self.__vote_counts[recipient] = 0
        self.__vote_counts[recipient] += 1

    def fetch_votes(self) -> List[Vote]:
        return list(self.votes.values())

    def fetch_voters(self) -> List[Player]:
        return list(self.votes.keys())

    def has_vote(self, player_id: int):
        return player_id in self.votes

    def vote_count(self) -> int:
        return len(self.fetch_votes())

    def get_ejected_player_id(self) -> Optional[int]:
        max_player, max_vote_count = self.__extract_max_player_and_vote_count()
        next_max_player, next_max_vote_count = self.__extract_max_player_and_vote_count()

        if max_player is None:
            self.no_ejection_reason = 'No votes'
        elif max_player == 'skip':
            self.no_ejection_reason = 'Skipped'
        elif max_vote_count == next_max_vote_count:
            self.no_ejection_reason = 'Tie'

        return max_player if not self.no_ejection_reason else None

    def __extract_max_player_and_vote_count(self) -> tuple:
        if not self.__vote_counts:
            return None, None

        max_player = max(self.__vote_counts, key=self.__vote_counts.get)
        vote_count = self.__vote_counts[max_player]
        self.__vote_counts.pop(max_player)
        return max_player, vote_count