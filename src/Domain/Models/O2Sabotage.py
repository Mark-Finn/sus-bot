import random
from datetime import datetime, timedelta
from typing import Tuple

from Domain.Models.Sabotage import Sabotage


class O2Sabotage(Sabotage):

    def __init__(self, hypoxia_time: int) -> None:
        super().__init__()
        self.hypoxia_time: datetime = datetime.now() + timedelta(seconds=hypoxia_time)
        self.code1: int = random.randint(100_000, 550_000)
        self.code2: int = random.randint(550_001, 999_999)
        self.code1_resolved: bool = False
        self.code2_resolved: bool = False

    def enter_code(self, code: int) -> bool:
        accepted = False
        if code == self.code1:
            accepted = True
            self.code1_resolved = True
            self.__check_resolve()
        if code == self.code2:
            accepted = True
            self.code2_resolved = True
            self.__check_resolve()
        return accepted

    def time_before_hypoxia(self) -> float:
        return max([(self.hypoxia_time - datetime.now()).total_seconds(), 0.0])

    def get_completed_required_tuple(self) -> Tuple:
        return int(self.code1_resolved) + int(self.code2_resolved), 2

    def __check_resolve(self):
        if self.code1_resolved and self.code2_resolved:
            self.resolve()