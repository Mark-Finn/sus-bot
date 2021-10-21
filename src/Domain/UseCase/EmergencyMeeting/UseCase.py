from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.EmergencyMeeting.Response import Response
from Domain.Validators.Game.EmergencyMeetingValidator import EmergencyMeetingValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, player_id: int) -> Response:
        response = Response()

        validator = EmergencyMeetingValidator(player_id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        player = game.player_set.fetch(player_id)
        game.call_meeting(player)
        game.current_meeting.add_player(player_id)
        player.emergency_meetings_called += 1

        response.caller_name = str(player)
        response.caller_color = player.color
        response.alive_player_count = game.player_set.alive_count()

        self.__game_model_gateway.check_in(game)
        response.success = True
        return response
