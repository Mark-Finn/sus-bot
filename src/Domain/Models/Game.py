from datetime import datetime
from typing import List, Optional

from Domain.Models.Player import Player
from Domain.Models.PlayerSet import PlayerSet
from Domain.Models.Meeting import Meeting
from Domain.Models.O2Sabotage import O2Sabotage
from Domain.Models.ReactorSabotage import ReactorSabotage
from Domain.Models.Sabotage import Sabotage
from Domain.Models.Vote import Vote
from Dtos.Settings import Settings
from Dtos.Task import Task
from Enums.GameState import GameState
from Enums.TaskType import TaskType


class Game:

    def __init__(self, settings: Settings, all_tasks: List[Task]) -> None:
        self.player_set: PlayerSet = PlayerSet()
        self.settings: Settings = settings
        self.all_tasks: List[Task] = all_tasks
        self.game_state: GameState = GameState.IN_LOBBY
        self.lobby_start_time: datetime = datetime.now()
        self.game_start_time: datetime = datetime.min
        self.round_start_time: datetime = datetime.min
        self.game_end_time: datetime = datetime.min
        self.current_meeting: Optional[Meeting] = None
        self.meeting_history: List[Meeting] = []
        self.impostors_win: Optional[bool] = None
        self.sabotage: Sabotage = None
        self.__completed_task_count_cache: int = 0

    def add_player(self, id: int, name: str, color: str):
        self.player_set.update(Player(id, name, color))

    def start(self):
        self.player_set.assign_roles(self.settings.impostors)
        self.player_set.assign_tasks(self.all_tasks, self.settings.common_tasks, self.settings.long_tasks, self.settings.short_tasks)
        self.game_start_time = datetime.now()
        self.begin_round()

    def end(self):
        if self.game_state != GameState.GAME_END:
            self.game_state = GameState.GAME_END
            self.game_end_time = datetime.now()

    def get_task_names(self) -> List[str]:
        return list(map(lambda task: task.name, self.all_tasks))

    def get_task_of_type(self, type: TaskType) -> List[Task]:
        return list(filter(lambda task: task.task_type == type, self.all_tasks))

    def get_completed_task_count(self):
        if self.settings.task_bar_updates == 0:
            return 0
        elif self.settings.task_bar_updates == 1:
            return self.__completed_task_count_cache
        else:
            return self.__count_completed_tasks()

    def total_tasks(self) -> int:
        tasks_per_player = self.settings.common_tasks + self.settings.long_tasks + self.settings.short_tasks
        return tasks_per_player * self.player_set.crewmate_count()

    def begin_round(self):
        for player in self.player_set.fetch_dead():
            player.confirmed_dead = True
        self.round_start_time = datetime.now()
        self.game_state = GameState.IN_PROGRESS

    def check_for_game_over(self) -> bool:
        if self.__count_completed_tasks() == self.total_tasks():
            self.end()
            self.impostors_win = False
            return True

        impostors_alive = self.player_set.alive_impostor_count()
        if self.player_set.alive_crewmate_count() <= impostors_alive or not impostors_alive:
            self.end()
            self.impostors_win = bool(impostors_alive)
            return True

        return False

    def get_recent_meeting(self) -> Optional[Meeting]:
        return self.meeting_history[-1] if self.meeting_history else None

    def call_meeting(self, meeting_caller: Player, body_found: Optional[Player]=None):
        self.game_state = GameState.MEETING_CALLED
        self.current_meeting = Meeting(meeting_caller, body_found)
        if isinstance(self.sabotage, (ReactorSabotage, O2Sabotage)):
            self.sabotage.resolve()

    def player_join_meeting(self, player_id: int):
        self.current_meeting.add_player(player_id)
        if self.current_meeting.player_count() == len(self.player_set.fetch_alive()):
            self.start_meeting()

    def start_meeting(self):
        self.game_state = GameState.DISCUSSING if self.settings.discussion_time > 0 else GameState.VOTING
        self.current_meeting.meeting_start_time = datetime.now()

    def start_voting(self):
        self.game_state = GameState.VOTING

    def cast_vote(self, vote: Vote) -> bool:
        self.current_meeting.add_vote(vote)
        is_last_vote = self.current_meeting.vote_count() == len(self.player_set.fetch_alive())
        return is_last_vote

    def end_meeting(self) -> Optional[Player]:
        self.__completed_task_count_cache = self.__count_completed_tasks()

        ejected_player = None

        current_meeting = self.current_meeting
        self.current_meeting.meeting_end_time = datetime.now()

        ejected_player_id = current_meeting.get_ejected_player_id()
        if ejected_player_id:
            ejected_player = self.player_set.fetch(ejected_player_id)
            ejected_player.die('Ejected')

        if len(self.player_set.fetch_crewmates()) == len(self.player_set.fetch_impostors()):
            self.game_state = GameState.GAME_END
        else:
            self.game_state = GameState.RESULTS

        self.meeting_history.append(self.current_meeting)
        return ejected_player

    def __count_completed_tasks(self):
        total = 0
        for player in self.player_set.fetch_crewmates():
            total += player.task_checklist.get_completed_count()
        return total
