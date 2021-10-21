from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.UseCase.JoinMeeting.Response import Response
from Domain.Validators.Game.JoinMeetingValidator import JoinMeetingValidator
from Enums.GameState import GameState


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, player_id: int) -> Response:
        response = Response()

        validator = JoinMeetingValidator(player_id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.error_message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        game.player_join_meeting(player_id)

        response.alive_player_count = game.player_set.alive_count()
        response.joined_players = list(map(lambda id: str(game.player_set.fetch(id)), game.current_meeting.players_joined))
        response.meeting_started = game.game_state != GameState.MEETING_CALLED

        self.__game_model_gateway.check_in(game)

        response.success = True
        return response
