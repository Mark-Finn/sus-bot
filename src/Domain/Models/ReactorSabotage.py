from datetime import datetime, timedelta

from Domain.Models.Sabotage import Sabotage


class ReactorSabotage(Sabotage):

    def __init__(self, meltdown_time: int):
        super().__init__()
        self.meltdown_time: datetime = datetime.now() + timedelta(seconds=meltdown_time)
        self.depress_time: int = 5
        self.left_button_press_time: datetime = datetime.min
        self.right_button_press_time: datetime = datetime.min
        self.left_player_id: int = 0
        self.right_player_id: int = 0

    def press_left(self, player_id: int):
        self.left_player_id = player_id
        self.left_button_press_time = datetime.now()
        self.__check_resolve()

    def press_right(self, player_id: int):
        self.right_player_id = player_id
        self.right_button_press_time = datetime.now()
        self.__check_resolve()

    def time_before_meltdown(self) -> float:
        return max([(self.meltdown_time - datetime.now()).total_seconds(), 0.0])

    def __check_resolve(self):
        time_between_presses = self.left_button_press_time - self.right_button_press_time
        if abs(time_between_presses.total_seconds()) < self.depress_time and self.left_player_id != self.right_player_id:
            self.resolve()
