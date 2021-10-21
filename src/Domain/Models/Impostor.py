import random
from datetime import datetime
from typing import List

from Domain.Models.Player import Player


class Impostor(Player):

    def __init__(self, id: int, name: str, color: str) -> None:
        super().__init__(id, name, color)
        self.is_impostor: bool = True
        self.kill_times: List[datetime] = []
        self.killed_players = []

    def kill(self, crewmate: Player) -> str:
        self.kill_times.append(datetime.now())
        kill_message = self.__kill_message()
        crewmate.die(kill_message)
        self.killed_players.append(str(crewmate))
        return kill_message

    def get_last_kill_time(self) -> datetime:
        return self.kill_times[-1] if self.kill_times else datetime.min

    def __kill_message(self):
        return random.choice([
            '{0} executed {1} with a pistol',
            '{0} stabbed {1} in the back',
            '{0} spiked {1} in the face',
            '{0} neck snapped {1}',
        ])
