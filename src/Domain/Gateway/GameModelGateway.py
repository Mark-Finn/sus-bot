import asyncio

from Domain.Models.Game import Game


class GameModelGateway:

    def __init__(self) -> None:
        self.lock: asyncio.Lock = asyncio.Lock()
        self.__game_model: Game = None

    async def new_game(self, game_model: Game):
        async with self.lock:
            self.__game_model = game_model

    def read_only(self) -> Game:
        return self.__game_model

    async def check_out(self) -> Game:
        await self.lock.acquire()
        return self.__game_model

    def check_in(self, game_model: Game):
        self.__game_model = game_model
        self.lock.release()