from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Models.Vote import Vote
from Domain.UseCase.TextResponse import TextResponse
from Domain.UseCase.Vote.Request import Request
from Domain.Validators.Game.VoteValidator import VoteValidator


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self, request: Request) -> TextResponse:
        response = TextResponse()

        validator = VoteValidator(request.player_id, request.recipient_id)

        game = await self.__game_model_gateway.check_out()
        if not validator.validate(game):
            response.success = False
            response.message = validator.error_message
            self.__game_model_gateway.check_in(game)
            return response

        vote = Vote(game.player_set.fetch(request.player_id), game.player_set.fetch(request.recipient_id))
        game.cast_vote(vote)

        self.__game_model_gateway.check_in(game)
        response.success = True
        return response
