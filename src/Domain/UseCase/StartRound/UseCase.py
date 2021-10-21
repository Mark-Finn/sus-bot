from Domain.Gateway.GameModelGateway import GameModelGateway

class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self):
        game = await self.__game_model_gateway.check_out()
        game.begin_round()
        self.__game_model_gateway.check_in(game)
