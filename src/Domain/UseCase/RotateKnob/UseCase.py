from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.RotateKnob.Request import Request
from Domain.UseCase.RotateKnob.Response import Response
from Domain.Validators.Game.ResolveComValidator import ResolveComValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, request: Request) -> Response:
        response = Response()

        game = await self.__game_model_gateway.check_out()

        validator = ResolveComValidator(request.player_id)

        if not validator.validate(game):
            response.success = False
            response.message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        pre_rotation = game.sabotage.get_rotation(request.player_id)
        turn_quality = game.sabotage.rotate_knob(request.player_id, request.rotation)
        post_rotation = game.sabotage.get_rotation(request.player_id)
        response.is_resolved = game.sabotage.is_resolved

        turn = abs(post_rotation - pre_rotation)
        if request.rotation > 0:
            emoji_direction = '↩'
            direction = '+'
        else:
            emoji_direction = '↪'
            direction = '-'
        prefix = f'({pre_rotation}° {emoji_direction} {direction}{turn}° = {post_rotation}°)'
        
        if response.is_resolved:
            response.message = f'I can hear you clearly, {post_rotation}° is perfect!'
        elif turn_quality == game.sabotage.CLOSER:
            response.message = f'{prefix}\r\n I can hear you better, try going more in the same direction'
        elif turn_quality == game.sabotage.FURTHER:
            response.message = f'{prefix}\r\n That is worse, try going the opposite direction'
        elif turn_quality == game.sabotage.SKIPPED:
            response.message = f'{prefix}\r\n You had it for a second!'

        self.__game_model_gateway.check_in(game)
        response.success = True
        return response