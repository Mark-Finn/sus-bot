from Domain.Models.Game import Game
from Domain.Validators.Game.ChainValidator import ChainValidator
from Domain.Validators.Game.InLobbyValidator import InLobbyValidator
from Domain.Validators.Game.SettingsValidator import SettingsValidator
from Dtos.Settings import Settings


class ChangeSettingValidator(ChainValidator):

    def __init__(self, setting: str, value: int) -> None:
        super().__init__([
            InLobbyValidator(),
            self.__InternalValidator(setting, value)
        ])

    class __InternalValidator(SettingsValidator):

        def __init__(self, setting: str, value: int) -> None:
            super().__init__()
            self.setting = setting
            self.value = value

        def validate(self, game: Game):
            settings = Settings()

            if self.setting not in self.__setting_options(settings):
                self.error_message = 'That setting does not exist'
                return False

            setattr(settings, self.setting, self.value)
            return self._validate_settings(settings)


        def __setting_options(self, settings: Settings):
            return [attr for attr in settings.__dict__.keys() if attr[:1] != '_']


