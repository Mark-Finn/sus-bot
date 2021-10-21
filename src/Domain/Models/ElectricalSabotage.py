import random
from typing import List

from Domain.Models.Sabotage import Sabotage


class ElectricalSabotage(Sabotage):

    def __init__(self):
        super().__init__()
        self.switch_states: List[bool] = [random.choice([True, False, False]) for _ in range(10)]
        self.switch_states[0] = False

    def flip_switch(self, switch_number: int):
        if 0 <= switch_number < len(self.switch_states):
            self.switch_states[switch_number] = not self.switch_states[switch_number]
            self.__check_resolve()

    def __check_resolve(self):
        if all(self.switch_states):
            self.resolve()