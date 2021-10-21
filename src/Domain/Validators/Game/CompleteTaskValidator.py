from Domain.Models.ComSabotage import ComSabotage
from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.CrewmateValidator import CrewmateValidator
from Domain.Validators.Game.TaskValidator import TaskValidator


class CompleteTaskValidator(ChainValidator):

    def __init__(self, player_id: int, task_name: str) -> None:
        super().__init__([
            TaskValidator(player_id),
            CrewmateValidator(player_id),
            self.__InnerValidator(player_id, task_name)
        ])

    class __InnerValidator(BaseValidator):

        def __init__(self, player_id: int, task_name: str) -> None:
            super().__init__()
            self.player_id: int = player_id
            self.task_name: str = task_name

        def validate(self, game: Game) -> bool:
            checklist = game.player_set.fetch(self.player_id).task_checklist

            if not checklist.has_task(self.task_name):
                self.error_message = 'You do not have that task'
            elif checklist.is_completed(self.task_name):
                self.error_message = 'You have already completed that task'

            if not self.error_message and isinstance(game.sabotage, ComSabotage) and not game.sabotage.is_resolved:
                uncompleted_names = checklist.get_uncompleted_tasks()
                tasks = filter(lambda task: task.name in uncompleted_names, game.all_tasks)
                next_task = tasks.__next__().name
                self.error_message = f'Due to communication issues, you must complete "{next_task}" next.' \
                    if next_task != self.task_name \
                    else ''

            return not self.error_message
