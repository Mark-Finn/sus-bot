from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.InProgressValidator import InProgressValidator
from Domain.Validators.Game.CrewmateValidator import CrewmateValidator


class TaskValidator(ChainValidator):

    def __init__(self, player_id: int) -> None:
        super().__init__([
            InProgressValidator(),
            self.__InnerValidator(player_id)
        ])

    class __InnerValidator(BaseValidator):

        def __init__(self, player_id: int) -> None:
            super().__init__()
            self.player_id: int = player_id

        def validate(self, game: Game) -> bool:
            checklist = game.player_set.fetch(self.player_id).task_checklist

            if not checklist.get_uncompleted_tasks():
                self.error_message = 'You completed all your tasks!'

            return not self.error_message
