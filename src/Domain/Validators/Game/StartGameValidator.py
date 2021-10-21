from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.InLobbyValidator import InLobbyValidator
from Domain.Validators.Game.SettingsValidator import SettingsValidator
from Enums.TaskType import TaskType


class StartGameValidator(ChainValidator):

    def __init__(self) -> None:
        super().__init__([
            InLobbyValidator(),
            SettingsValidator(),
            self.__InnerValidator()
        ])

    class __InnerValidator(BaseValidator):

        def validate(self, game: Game) -> bool:
            if len(game.get_task_of_type(TaskType.COMMON)) < game.settings.common_tasks:
                self.error_message = 'Not enough common tasks'
            elif len(game.get_task_of_type(TaskType.LONG)) < game.settings.long_tasks:
                self.error_message = 'Not enough long tasks'
            elif len(game.get_task_of_type(TaskType.SHORT)) < game.settings.short_tasks:
                self.error_message = 'Not enough short tasks'
            elif game.player_set.count() <= game.settings.impostors * 2:
                self.error_message = f'Not enough players for {game.settings.impostors} impostor(s)'

            return not self.error_message
