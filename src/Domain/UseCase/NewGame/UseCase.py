from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Gateway.Settings.Gateway import Gateway as SettingsGateway
from Domain.Gateway.Tasks.Gateway import Gateway as TaskGateway
from Domain.Models.Game import Game


class UseCase:

    def __init__(self,
                 game_model_gateway: GameModelGateway,
                 settings_gateway: SettingsGateway,
                 task_gateway: TaskGateway):
        self.__game_model_gateway = game_model_gateway
        self.__settings_gateway = settings_gateway
        self.__task_gateway = task_gateway

    async def execute(self):
        settings = self.__settings_gateway.fetch()
        tasks = self.__task_gateway.fetch()
        tasks.sort()
        game = Game(settings, tasks)
        await self.__game_model_gateway.new_game(game)