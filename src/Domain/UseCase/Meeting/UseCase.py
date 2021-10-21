from datetime import datetime, timedelta

from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Models.ElectricalSabotage import ElectricalSabotage
from Domain.Models.ComSabotage import ComSabotage
from Domain.UseCase.Meeting.FinalResponse import FinalResponse
from Domain.UseCase.Meeting.UpdateResponse import UpdateResponse


class UseCase:

    def __init__(self, game_model_gateway: GameModelGateway):
        self.__game_model_gateway = game_model_gateway

    async def execute(self):
        game = await self.__game_model_gateway.check_out()

        update_response = UpdateResponse()
        update_response.player_options = dict(map(lambda player: (player.id, str(player)), game.player_set.fetch_alive()))

        voting_start_time = datetime.now() + timedelta(seconds=game.settings.discussion_time)
        meeting_end_time = voting_start_time + timedelta(seconds=game.settings.voting_time)

        update = True
        while update:
            now = datetime.now()

            if not update_response.is_voting and now > voting_start_time:
                update_response.is_voting = True
                game.start_voting()

            date_diff = meeting_end_time - now if update_response.is_voting else voting_start_time - now
            update_response.time_remaining = int(date_diff.total_seconds())

            update_response.voters = list(map(lambda player: str(player), game.current_meeting.fetch_voters()))

            update = update_response.time_remaining >= 0 and game.current_meeting.vote_count() != len(game.player_set.fetch_alive())

            self.__game_model_gateway.check_in(game)

            yield update_response

            game = await self.__game_model_gateway.check_out()

        final_response = FinalResponse()

        ejected_player = game.end_meeting()
        final_response.anonymous_voting = game.settings.anonymous_voting
        final_response.ejected_player = str(ejected_player) if ejected_player else None
        final_response.no_ejection_reason = game.current_meeting.no_ejection_reason
        final_response.was_impostor = ejected_player.is_impostor if ejected_player and game.settings.confirm_ejects else None
        final_response.remaining_impostors = game.player_set.alive_impostor_count() if game.settings.confirm_ejects else None
        final_response.is_game_over = game.check_for_game_over()

        has_active_sabotage = not game.sabotage.is_resolved if game.sabotage else False

        if has_active_sabotage and isinstance(game.sabotage, ElectricalSabotage):
            final_response.is_electrical_sabotage = True
            final_response.switch_states = game.sabotage.switch_states
        elif has_active_sabotage and isinstance(game.sabotage, ComSabotage):
            final_response.is_com_sabotage = True
            final_response.rotation_options = game.sabotage.ROTATION_OPTIONS

        for vote in game.current_meeting.fetch_votes():
            recipient = str(vote.recipient) if vote.recipient else 'Skip'
            if recipient not in final_response.recipient_votes_map:
                final_response.recipient_votes_map[recipient] = []
            final_response.recipient_votes_map[recipient].append(str(vote.voter))

        for recipient, votes in final_response.recipient_votes_map.items():
            final_response.recipient_vote_count_list.append((recipient, len(votes)))

        final_response.recipient_vote_count_list.sort(key=lambda tup: tup[1], reverse=True)

        self.__game_model_gateway.check_in(game)
        yield final_response
