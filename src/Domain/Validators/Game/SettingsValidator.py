from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator
from Dtos.Settings import Settings


class SettingsValidator(BaseValidator):

    def validate(self, game: Game) -> bool:
        return self._validate_settings(game.settings)

    def _validate_settings(self, settings: Settings) -> bool:
        messages = []
        if settings.impostors <= 0:
            messages.append('"impostors" must be greater than 0')
        if settings.confirm_ejects not in [0, 1]:
            messages.append('"confirm_ejects" must be 0 or 1')
        if settings.emergency_meetings < 0:
            messages.append('"emergency_meetings" must be greater than or equal to 0')
        if settings.emergency_cooldown < 0:
            messages.append('"emergency_cooldown" must be greater than or equal to 0')
        if settings.discussion_time < 0:
            messages.append('"discussion_time" must be greater than or equal to 0')
        if settings.voting_time < 15:
            messages.append('"voting_time" must be greater than or equal to 15')
        if settings.kill_cooldown < 0:
            messages.append('"kill_cooldown" must be greater than or equal to 0')
        if settings.common_tasks < 0:
            messages.append('"common_tasks" must be greater than or equal to 0')
        if settings.long_tasks < 0:
            messages.append('"long_tasks" must be greater than or equal to 0')
        if settings.short_tasks < 0:
            messages.append('"short_tasks" must be greater than or equal to 0')
        if settings.anonymous_voting not in [0, 1]:
            messages.append('"anonymous_voting" must be 0 or 1')
        if settings.task_bar_updates not in [0, 1, 2]:
            messages.append('"task_bar_updates" must be 0 (Never), 1 (Meetings), 2 (Always)')

        self.error_message = ','.join(messages)
        return not self.error_message
