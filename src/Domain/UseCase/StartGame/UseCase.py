from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.StartGame.Response import Response
from Domain.UseCase.StartGame.PlayerResponse import PlayerResponse
from Domain.Validators.Game.StartGameValidator import StartGameValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self) -> Response:
        response = Response()

        validator = StartGameValidator()

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        game.start()
        for player in game.player_set.fetch_all():
            player_task_names = player.task_checklist.get_all()
            player_tasks = list(filter(lambda task: task.name in player_task_names, game.all_tasks))
            response.players.append(PlayerResponse(player.id, player.is_impostor, player_tasks))
            if player.is_impostor:
                response.impostor_color_pairs.append((player.name, player.color))
                response.impostor_names.append(str(player))
            else:
                response.crewmate_color_pairs.append((player.name, player.color))



        self.__game_model_gateway.check_in(game)
        response.success = True
        return response

