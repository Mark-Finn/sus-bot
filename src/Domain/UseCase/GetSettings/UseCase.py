import copy

from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Gateway.Settings.Gateway import Gateway as SettingsGateway
from Dtos.Settings import Settings


class UseCase:

    def __init__(self,
                 game_model_gateway: GameModelGateway,
                 settings_gateway: SettingsGateway):
        self.__game_model_gateway = game_model_gateway
        self.__settings_gateway = settings_gateway

    def execute(self) -> Settings:
        game = self.__game_model_gateway.read_only()

        if game:
            settings = game.settings
        else:
            settings = self.__settings_gateway.fetch()

        return copy.deepcopy(settings)