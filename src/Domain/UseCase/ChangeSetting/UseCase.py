from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Gateway.Settings.Gateway import Gateway as SettingsGateway
from Domain.UseCase.ChangeSetting.Request import Request
from Domain.UseCase.TextResponse import TextResponse
from Domain.Validators.Game.ChangeSettingValidator import ChangeSettingValidator


class UseCase:

    def __init__(self,
                 game_model_gateway: GameModelGateway,
                 settings_gateway: SettingsGateway):
        self.__game_model_gateway = game_model_gateway
        self.__settings_gateway = settings_gateway

    async def execute(self, request: Request) -> TextResponse:
        response = TextResponse()
        response.success = True
        response.message = 'Setting updated'

        validator = ChangeSettingValidator(request.setting, request.value)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        setattr(game.settings, request.setting, request.value)
        self.__settings_gateway.save(game.settings)
        self.__game_model_gateway.check_in(game)

        return response
