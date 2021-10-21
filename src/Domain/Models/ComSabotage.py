import random
from typing import Optional

from Domain.Models.Sabotage import Sabotage


class ComSabotage(Sabotage):

    def __init__(self):
        super().__init__()
        self.ROTATION_OPTIONS = [ 5, 13, 59 ]
        self.CLOSER = 1
        self.SKIPPED = 0
        self.FURTHER = -1
        self.__MAX = 170
        self.__target: int = random.randint(10, self.__MAX - 1) * random.choice([1, -1])
        self.__player_knobs: dict = {}

    def get_rotation(self, player_id: int):
        return self.__player_knobs.get(player_id, 0) + self.__MAX

    def rotate_knob(self, player_id: int, rotation: int) -> Optional[int]:
        self.__player_knobs[player_id] = self.__player_knobs.get(player_id, 0)

        should_go_right = self.__target > self.__player_knobs[player_id]
        self.__player_knobs[player_id] += rotation

        if self.__player_knobs[player_id] > self.__MAX:
            self.__player_knobs[player_id] = self.__MAX
        if self.__player_knobs[player_id] < -self.__MAX:
            self.__player_knobs[player_id] = -self.__MAX

        if self.__player_knobs[player_id] == self.__target:
            self.resolve()
            return None

        turned_right = rotation > 0
        should_still_go_right = self.__target > self.__player_knobs[player_id]

        if should_go_right != should_still_go_right:
            return self.SKIPPED

        return self.CLOSER if should_go_right == turned_right else self.FURTHER
