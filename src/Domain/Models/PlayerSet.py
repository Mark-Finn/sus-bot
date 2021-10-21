from random import shuffle, sample
from typing import List, Optional

from Domain.Models.Player import Player
from Dtos.Task import Task
from Domain.Models.Crewmate import Crewmate

from Domain.Models.Impostor import Impostor
from Enums.TaskType import TaskType


class PlayerSet:

    def __init__(self) -> None:
        self.players: dict = {}

    def update(self, player: Player):
        self.players[player.id] = player

    def remove(self, id: int):
        self.players.pop(id)

    def fetch(self, id: int) -> Optional[Player]:
        return self.players[id] if id in self.players else None

    def count(self) -> int:
        return len(self.players)

    def crewmate_count(self) -> int:
        return len(self.fetch_crewmates())

    def impostor_count(self) -> int:
        return len(self.fetch_impostors())

    def alive_count(self) -> int:
        return len(self.fetch_alive())

    def alive_crewmate_count(self) -> int:
        return len(self.fetch_alive_crewmates())

    def alive_impostor_count(self) -> int:
        return len(self.fetch_alive_impostors())

    def fetch_all(self) -> List[Player]:
        return list(self.players.values())

    def fetch_alive(self) -> List[Player]:
        return list(filter(lambda player: player.is_alive(), self.fetch_all()))

    def fetch_possibly_alive(self) -> List[Player]:
        return list(filter(lambda player: not player.confirmed_dead, self.fetch_all()))

    def fetch_dead(self) -> List[Player]:
        return list(filter(lambda player: not player.is_alive(), self.fetch_all()))

    def fetch_impostors(self) -> List[Player]:
        return list(filter(lambda player: player.is_impostor, self.fetch_all()))

    def fetch_alive_impostors(self) -> List[Player]:
        return list(filter(lambda player: player.is_impostor and player.is_alive(), self.fetch_all()))

    def fetch_crewmates(self) -> List[Player]:
        return list(filter(lambda player: not player.is_impostor, self.fetch_all()))

    def fetch_alive_crewmates(self) -> List[Player]:
        return list(filter(lambda player: not player.is_impostor and player.is_alive(), self.fetch_all()))

    def fetch_all_ids(self) -> List[int]:
        return list(self.players.keys())

    def assign_roles(self, impostors_count: int):
        players = self.fetch_all()
        shuffle(players)
        cnt = 0
        for player in players:
            self.players[player.id] = Impostor(player.id, player.name, player.color) \
                if cnt < impostors_count \
                else Crewmate(player.id, player.name, player.color)
            cnt += 1

    def assign_tasks(self, all_tasks: List[Task], common_count: int, long_count: int, short_count: int):
        grouped_tasks = self.__group_tasks(all_tasks)

        common_tasks = sample(grouped_tasks[TaskType.COMMON], common_count)

        for player in self.fetch_all():
            player.assign_tasks(common_tasks)
            player.assign_tasks(sample(grouped_tasks[TaskType.LONG], long_count))
            player.assign_tasks(sample(grouped_tasks[TaskType.SHORT], short_count))

    def __group_tasks(self, all_tasks: List[Task]) -> dict:
        grouped_tasks = {TaskType.COMMON: [], TaskType.LONG: [], TaskType.SHORT: []}
        for task in all_tasks:
            grouped_tasks[task.task_type].append(task)
        return grouped_tasks