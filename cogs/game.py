from typing import List, Optional

import copy

import time

import os

from config import *

import discord
import math

from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button, ButtonStyle, Select, SelectOption

from Container import Container
from utils import Utils

from Dtos.Task import Task

from Domain.UseCase.NewGame.UseCase import UseCase as NewGameUseCase
from Domain.UseCase.JoinColorOptions.UseCase import UseCase as JoinColorOptionsUseCase
from Domain.UseCase.JoinGame.Request import Request as JoinGameRequest
from Domain.UseCase.JoinGame.UseCase import UseCase as JoinGameUseCase
from Domain.UseCase.LeaveGame.UseCase import UseCase as LeaveGameUseCase
from Domain.UseCase.GetTasks.UseCase import UseCase as GetTasksUseCase
from Domain.UseCase.GetSettings.UseCase import UseCase as GetSettingsUseCase
from Domain.UseCase.ChangeSetting.UseCase import UseCase as ChangeSettingUseCase
from Domain.UseCase.ChangeSetting.Request import Request as ChangeSettingRequest
from Domain.UseCase.StartGame.UseCase import UseCase as StartGameUseCase
from Domain.UseCase.TaskCompletion.UseCase import UseCase as TaskCompletionUseCase
from Domain.UseCase.KillOptions.UseCase import UseCase as KillOptionsUseCase
from Domain.UseCase.KillPlayer.UseCase import UseCase as KillPlayerUseCase
from Domain.UseCase.KillPlayer.Request import Request as KillPlayerRequest
from Domain.UseCase.EndGame.UseCase import UseCase as EndGameUseCase
from Domain.UseCase.EmergencyMeeting.UseCase import UseCase as EmergencyMeetingUseCase
from Domain.UseCase.JoinMeeting.UseCase import UseCase as JoinMeetingUseCase
from Domain.UseCase.Meeting.UseCase import UseCase as MeetingUseCase
from Domain.UseCase.Meeting.UpdateResponse import UpdateResponse as MeetingUpdateResponse
from Domain.UseCase.Vote.UseCase import UseCase as VoteUseCase
from Domain.UseCase.Vote.Request import Request as VoteRequest
from Domain.UseCase.StartRound.UseCase import UseCase as StartRoundUseCase
from Domain.UseCase.ReportOptions.UseCase import UseCase as ReportOptionsUseCase
from Domain.UseCase.ReportBody.UseCase import UseCase as ReportBodyUseCase
from Domain.UseCase.ReportBody.Request import Request as ReportBodyRequest
from Domain.UseCase.TaskOptions.UseCase import UseCase as TaskOptionsUseCase
from Domain.UseCase.CompleteTask.UseCase import UseCase as CompleteTaskUseCase, Request as CompleteTaskRequest
from Domain.UseCase.ReactorSabotage.UseCase import UseCase as ReactorSabotageUseCase
from Domain.UseCase.BaseUrgentSabotage.ErrorResponse import ErrorResponse as UrgentSabotageErrorResponse
from Domain.UseCase.BaseUrgentSabotage.UpdateResponse import UpdateResponse as UrgentSabotageUpdateResponse
from Domain.UseCase.BaseUrgentSabotage.FinalResponse import FinalResponse as UrgentSabotageFinalResponse
from Domain.UseCase.PressReactorButton.UseCase import UseCase as PressReactorButtonUseCase
from Domain.UseCase.PressReactorButton.Request import Request as PressReactorButtonRequest
from Domain.UseCase.CanSabotage.UseCase import UseCase as CanSabotageUseCase
from Domain.UseCase.ElectricalSabotage.UseCase import UseCase as ElectricalSabotageUseCase
from Domain.UseCase.FlipSwitch.UseCase import UseCase as FlipSwitchUseCase
from Domain.UseCase.FlipSwitch.Request import Request as FlipSwitchRequest
from Domain.UseCase.O2Sabotage.UseCase import UseCase as O2SabotageUseCase
from Domain.UseCase.O2Sabotage.UpdateResponse import UpdateResponse as O2UpdateResponse
from Domain.UseCase.EnterCode.UseCase import UseCase as EnterCodeUseCase
from Domain.UseCase.EnterCode.Request import Request as EnterCodeRequest
from Domain.UseCase.ComSabotage.UseCase import UseCase as ComSabotageUseCase
from Domain.UseCase.RotateKnob.UseCase import UseCase as RotateKnobUseCase
from Domain.UseCase.RotateKnob.Request import Request as RotateKnobRequest
from Service.ImageService import ImageService


class Game(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.RATE_LIMIT = 50
        self.DEFERRED_UPDATE_MESSAGE = 6

        self.PLAYER_COLORS = {
            'red': (215,30,34),
            'blue': (29,60,233),
            'green': (27, 145, 62),
            'pink': (255, 99, 212),
            'orange': (255, 141, 28),
            'yellow': (255, 255, 103),
            'black': (74, 86, 94),
            'white': (233, 247, 255),
            'purple': (120, 61, 210),
            'brown': (128, 88, 45),
            'cyan': (68, 255, 247),
            'lime': (91, 254, 75),
            'maroon': (108, 43, 61),
            'rose': (255, 214, 236),
            'banana': (255, 255, 190),
            'gray': (131, 151, 167),
            'tan': (159, 153, 137),
            'coral': (236, 117, 120),
        }
        self.THEME_COLOR_PRIMARY = discord.Color.from_rgb(239, 71, 111)
        self.THEME_COLOR_SECONDARY = discord.Color.from_rgb(23, 143, 235)
        self.THEME_COLOR_TERTIARY = discord.Color.from_rgb(0, 128, 0)

        self.SABOTAGE_REACTOR = 'Nuclear Reactor'
        self.SABOTAGE_ELECTRICAL = 'Electrical'
        self.SABOTAGE_O2 = 'O2'
        self.SABOTAGE_COM = 'Communications'

        self.bot: Bot = bot
        self.__pre_lobby_message_id = 0
        self.__lobby_tasks_message_id = 0
        self.__lobby_settings_message_id = 0
        self.__dm_task_list_message_set = {}
        self.__hud_message_id = 0
        self.__meeting_message_id = 0
        self.__meeting_message_embed = None
        self.__electrical_sabotage_message_id = 0
        self.__com_sabotage_message_id = 0

        container = Container()
        self.__new_game_use_case: NewGameUseCase = container.new_game_use_case()
        self.__join_color_options_use_case: JoinColorOptionsUseCase = container.join_color_options_use_case()
        self.__join_game_use_case: JoinGameUseCase = container.join_game_use_case()
        self.__leave_game_use_case: LeaveGameUseCase = container.leave_game_use_case()
        self.__get_tasks_use_case: GetTasksUseCase = container.get_tasks_use_case()
        self.__get_settings_use_case: GetSettingsUseCase = container.get_settings_use_case()
        self.__change_setting_use_case: ChangeSettingUseCase = container.change_setting_use_case()
        self.__start_game_use_case: StartGameUseCase = container.start_game_use_case()
        self.__task_completion_use_case: TaskCompletionUseCase = container.task_completion_use_case()
        self.__kill_options_use_case: KillOptionsUseCase = container.kill_options_use_case()
        self.__kill_player_use_case: KillPlayerUseCase = container.kill_player_use_case()
        self.__end_game_use_case: EndGameUseCase = container.end_game_use_case()
        self.__emergency_meeting_use_case: EmergencyMeetingUseCase = container.emergency_meeting_use_case()
        self.__join_meeting_use_case: JoinMeetingUseCase = container.join_meeting_use_case()
        self.__meeting_use_case: MeetingUseCase = container.meeting_use_case()
        self.__vote_use_case: VoteUseCase = container.vote_use_case()
        self.__start_round_use_case: StartRoundUseCase = container.start_round_use_case()
        self.__report_options_use_case: ReportOptionsUseCase = container.report_options_use_case()
        self.__report_body_use_case: ReportBodyUseCase = container.report_body_use_case()
        self.__task_options_use_case: TaskOptionsUseCase = container.task_options_use_case()
        self.__complete_task_use_case: CompleteTaskUseCase = container.complete_task_use_case()
        self.__reactor_sabotage_use_case: ReactorSabotageUseCase = container.reactor_sabotage_use_case()
        self.__press_reactor_button_use_case: PressReactorButtonUseCase = container.press_reactor_button_use_case()
        self.__can_sabotage_button_use_case: CanSabotageUseCase = container.can_sabotage_button_use_case()
        self.__electrical_sabotage_use_case: ElectricalSabotageUseCase = container.electrical_sabotage_use_case()
        self.__flip_switch_use_case: FlipSwitchUseCase = container.flip_switch_use_case()
        self.__o2_sabotage_use_case: O2SabotageUseCase = container.o2_sabotage_use_case()
        self.__enter_code_use_case: EnterCodeUseCase = container.enter_code_use_case()
        self.__com_sabotage_use_case: ComSabotageUseCase = container.com_sabotage_use_case()
        self.__rotate_knob_use_case: RotateKnobUseCase = container.rotate_knob_use_case()
        self.__image_service: ImageService = ImageService(os.getcwd(), self.PLAYER_COLORS)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.__new_game()

    @commands.command()
    @commands.has_role(ADMIN_ROLE)
    async def new_game(self, ctx):
        await self.__new_game()

    @commands.command()
    @commands.has_role(ADMIN_ROLE)
    async def start_game(self, ctx):
        response = await self.__start_game_use_case.execute()

        if not response.success:
            await ctx.send(response.error_message)
            return

        self.__dm_task_list_message_set = {}
        guild = self.bot.get_guild(SERVER_ID)
        crewmate_role = guild.get_role(CREWMATE_ROLE_ID)

        player_ids = list(map(lambda player: player.id, response.players))

        for member in crewmate_role.members:
            if member.id not in player_ids:
                await member.remove_roles(crewmate_role)
                time.sleep(1 / self.RATE_LIMIT)

        crewmate_image, impostor_image = self.__image_service.create_team_screens(
            response.crewmate_color_pairs, response.impostor_color_pairs)

        for player in response.players:
            member = guild.get_member(player.id)
            await member.add_roles(crewmate_role)
            await self.__dm_player(player.id, image=impostor_image if player.is_impostor else crewmate_image)
            await self.__dm_task_list(player.id, player.tasks)
            time.sleep(3 / self.RATE_LIMIT)

        channel = Utils.get_channel(self.bot, GAME_CHANNEL)
        await Utils.delete_history(channel)

        await self.__game_hud()

    @commands.command()
    @commands.has_role(ADMIN_ROLE)
    async def setting(self, ctx, setting, value):
        request = ChangeSettingRequest(setting, int(value))
        response = await self.__change_setting_use_case.execute(request)

        if response.success:
            await ctx.send(f'Updated {setting}')
            await self.__lobby_settings_message()
        else:
            await ctx.send(response.message)

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        if interaction.custom_id == 'join_game':
            await self.__on_join_game(interaction)
        elif interaction.custom_id == 'leave_game':
            await self.__on_leave_game(interaction)
        elif interaction.custom_id == 'task_list':
            await self.__on_task_list(interaction)
        elif interaction.custom_id == 'emergency_meeting':
            await self.__on_emergency_meeting(interaction)
        elif interaction.custom_id == 'report_list':
            await self.__on_report_options(interaction)
        elif interaction.custom_id == 'kill_list':
            await self.__on_kill_button(interaction)
        elif interaction.custom_id == 'join_meeting':
            await self.__on_join_meeting(interaction)
        elif interaction.custom_id == 'skip':
            await self.__on_vote(interaction, is_skip=True)
        elif interaction.custom_id == 'sabotage_options':
            await self.__on_sabotage_option(interaction)
        elif interaction.custom_id == 'reactor_left':
            await self.__press_reactor_button(interaction, is_left_button=True)
        elif interaction.custom_id == 'reactor_right':
            await self.__press_reactor_button(interaction, is_left_button=False)
        elif 'switch' in interaction.custom_id:
            await self.__on_switch(interaction)
        elif 'rotate' in interaction.custom_id:
            await self.__on_rotate(interaction)

    @commands.Cog.listener()
    async def on_select_option(self, interaction):
        if interaction.custom_id == 'join_game_with_color':
            await self.__on_join_game_with_color(interaction)
        elif interaction.custom_id == 'kill_player':
            await self.__on_kill_player(interaction)
        elif interaction.custom_id == 'vote':
            await self.__on_vote(interaction)
        elif interaction.custom_id == 'report_body':
            await self.__on_report_body(interaction)
        elif interaction.custom_id == 'complete_task':
            await self.__on_complete_task(interaction)
        elif interaction.custom_id == 'sabotage':
            await self.__on_sabotage(interaction)

    @commands.Cog.listener()
    async def on_message(self, message):
        content: str = message.content.replace(' ', '').replace('-', '')
        user_id = message.author.id
        is_o2_user = user_id in (O2_USER1_ID, O2_USER2_ID)

        if not isinstance(message.channel, discord.DMChannel) or not content.isnumeric() or is_o2_user:
            return

        request = EnterCodeRequest(user_id, code=int(content))
        response = await self.__enter_code_use_case.execute(request)

        await message.reply(response.message)

    async def __on_sabotage(self, interaction):
        if interaction.values[0] == self.SABOTAGE_REACTOR:
            await self.__reactor_sabotage(interaction)
        elif interaction.values[0] == self.SABOTAGE_ELECTRICAL:
            await self.__electrical_sabotage(interaction)
        elif interaction.values[0] == self.SABOTAGE_O2:
            await self.__o2_sabotage(interaction)
        elif interaction.values[0] == self.SABOTAGE_COM:
            await self.__com_sabotage(interaction)

    async def __new_game(self):
        channel = Utils.get_channel(self.bot, LOBBY_CHANNEL)
        await Utils.delete_history(channel)

        await self.__new_game_use_case.execute()
        await self.__lobby_tasks_message()
        await self.__lobby_settings_message()
        await self.__pre_lobby_message()

    async def __lobby_tasks_message(self):
        tasks = self.__get_tasks_use_case.execute()
        embed = self.__tasks_embed(tasks)

        channel = Utils.get_channel(self.bot, LOBBY_CHANNEL)

        try:
            message = await channel.fetch_message(self.__lobby_tasks_message_id)
            await message.edit(embed=embed)
        except discord.NotFound:
            message = await channel.send(embed=embed)
            self.__lobby_tasks_message_id = message.id

    async def __lobby_settings_message(self):
        embed = discord.Embed(
            title='Settings',
            colour=self.THEME_COLOR_SECONDARY
        )
        embed.set_thumbnail(url=SETTINGS_URL)

        settings = self.__get_settings_use_case.execute()

        map = {
            'confirm_ejects': ['Off', 'On'],
            'anonymous_voting': ['Off', 'On'],
            'task_bar_updates': ['Never', 'Meetings', 'Always']
        }

        for setting, value in settings.__dict__.items():
            presented_value = map[setting][value] if setting in map else value
            embed.add_field(name=setting.replace('_', ' ').title(), value=presented_value, inline=True)

        channel = Utils.get_channel(self.bot, LOBBY_CHANNEL)

        try:
            message = await channel.fetch_message(self.__lobby_settings_message_id)
            await message.edit(embed=embed)
        except discord.NotFound:
            message = await channel.send(embed=embed)
            self.__lobby_settings_message_id = message.id

    async def __pre_lobby_message(self, players: List[str]=None):
        embed = discord.Embed(
            title=LOBBY_CHANNEL,
            description='Waiting for host to start...',
            colour=self.THEME_COLOR_PRIMARY
        )
        embed.set_thumbnail(url=LOBBY_URL)
        embed.add_field(name=f'Players ({len(players or [])}):', value='\r\n'.join(players or ['*none*']), inline=False)

        components = [[
            Button(style=ButtonStyle.green, label="Join", custom_id="join_game"),
            Button(style=ButtonStyle.red, label="Leave", custom_id="leave_game"),
        ]]

        channel = Utils.get_channel(self.bot, LOBBY_CHANNEL)

        try:
            message = await channel.fetch_message(self.__pre_lobby_message_id)
            await message.edit(embed=embed, components=components)
        except discord.NotFound:
            message = await channel.send(embed=embed, components=components)
            self.__pre_lobby_message_id = message.id

    async def __on_join_game(self, interaction):
        response = await self.__join_color_options_use_case.execute(interaction.user.id)

        if not response.success:
            await Utils.interact(interaction, response.error_message)
            return

        select_options = list(map(lambda color: SelectOption(label=color, value=color), response.color_options))
        message = 'Please pick a color'
        await Utils.interact(interaction, message, components=[
            Select(placeholder="Player Color", options=select_options, custom_id="join_game_with_color")
        ])

    async def __on_join_game_with_color(self, interaction):
        user = interaction.user
        request = JoinGameRequest(user.id, user.nick or user.name, color=interaction.values[0])
        response = await self.__join_game_use_case.execute(request)

        if response.success:
            await self.__pre_lobby_message(response.player_list)
            await Utils.interact(interaction, 'Joined!')
        else:
            await Utils.interact(interaction, response.error_message)

    async def __on_leave_game(self, interaction):
        response = await self.__leave_game_use_case.execute(interaction.user.id)

        if not response.success:
            await Utils.interact(interaction, response.error_message)
            return

        await Utils.interact(interaction, 'Left ヽ(*。>Д<)o゜')
        await self.__pre_lobby_message(response.player_list)

    async def __on_kill_button(self, interaction):
        response = await self.__kill_options_use_case.execute(interaction.user.id)

        if not response.success:
            await Utils.interact(interaction, response.error_message)
            return

        select_options = []
        for victim_id, victim_name in response.kill_options.items():
            select_options.append(SelectOption(label=victim_name, value=victim_id))

        message = f'Kill crewmate in arms reach\r\nImpostors: {", ".join(response.impostors_names)}'
        await Utils.interact(interaction, message, components=[
            Select(placeholder='Victim', options=select_options, custom_id="kill_player")
        ])

    async def __on_kill_player(self, interaction):
        killer_id = interaction.user.id
        victim_id = int(interaction.values[0])
        request = KillPlayerRequest(killer_id, victim_id)
        response = await self.__kill_player_use_case.execute(request)

        if not response.success:
            await Utils.interact(interaction, response.error_message)
            return

        await Utils.interact(interaction, response.killer_message)
        await self.__dm_player(victim_id, response.victim_message)
        if response.is_game_over:
            await self.__end_game()

    async def __on_emergency_meeting(self, interaction):
        response = await self.__emergency_meeting_use_case.execute(interaction.user.id)

        if not response.success:
            await Utils.interact(interaction, response.error_message)
            return
        await Utils.interact(interaction, 'You hit the button!')

        color_tuple = self.PLAYER_COLORS.get(response.caller_color.lower(), None)
        self.__meeting_message_embed = discord.Embed(
            title='Meeting',
            description=f'{response.caller_name} called an Emergency Meeting',
            colour=discord.Color.from_rgb(*color_tuple) if color_tuple else self.THEME_COLOR_PRIMARY
        )
        self.__meeting_message_embed.set_thumbnail(url=EMERGENCY_BUTTON_URL)

        return await self.__join_meeting_message(response.alive_player_count, [response.caller_name])

    async def __on_vote(self, interaction, is_skip=False):
        if is_skip:
            request = VoteRequest.create_skip_vote(interaction.user.id)
        else:
            request = VoteRequest.create_vote_for_player(interaction.user.id, int(interaction.values[0]))

        response = await self.__vote_use_case.execute(request)

        if not response.success:
            await Utils.interact(interaction, response.message)

        await Utils.interact(interaction, 'Thank you for performing your civic duty crewmate!')

    async def __on_report_options(self, interaction):
        response = await self.__report_options_use_case.execute(interaction.user.id)

        if not response.success:
            await Utils.interact(interaction, response.error_message)
            return

        options = list(map(lambda kv: SelectOption(label=kv[1], value=kv[0]), response.report_options.items()))
        components = [
            Select(placeholder='Dead Body', options=options, custom_id='report_body')
        ]

        await Utils.interact(interaction, 'Report a dead body', components=components)

    async def __on_report_body(self, interaction):
        request = ReportBodyRequest(interaction.user.id, int(interaction.values[0]))
        response = await self.__report_body_use_case.execute(request)

        if not response.success:
            await Utils.interact(interaction, response.error_message)
            return
        await Utils.interact(interaction, 'Body reported!')

        color_tuple = self.PLAYER_COLORS.get(response.caller_color.lower(), None)
        self.__meeting_message_embed = discord.Embed(
            title='Meeting',
            description=f'{response.caller_name} found the dead body of {response.body_name}',
            colour=discord.Color.from_rgb(*color_tuple) if color_tuple else self.THEME_COLOR_PRIMARY
        )
        self.__meeting_message_embed.set_thumbnail(url=REPORT_URL)

        return await self.__join_meeting_message(response.alive_player_count)

    async def __on_task_list(self, interaction):
        response = await self.__task_options_use_case.execute(interaction.user.id)

        if not response.success:
            await Utils.interact(interaction, response.error_message)
            return

        options = list(map(lambda task: SelectOption(label=task, value=task), response.task_options))
        components = [
            Select(placeholder='Task List', options=options, custom_id='complete_task')
        ]

        await Utils.interact(interaction, 'Complete a Task', components=components)

    async def __on_complete_task(self, interaction):
        request = CompleteTaskRequest(interaction.user.id, interaction.values[0])
        response = await self.__complete_task_use_case.execute(request)

        if not response.success:
            await Utils.interact(interaction, response.error_message)
            return
        await Utils.interact(interaction, f'"{request.task_name}" completed!')

        await self.__game_hud(update_only=True)
        await self.__dm_task_list(interaction.user.id, response.task_list, response.completed_task_names)

        if response.is_game_over:
            return await self.__end_game()

    async def __join_meeting_message(self, alive_player_count: int, joined_players: Optional[List[str]]=None):
        name = f'Players ({len(joined_players or [])}/{alive_player_count}):'
        value = '\r\n'.join(joined_players or ['*none*'])

        embed = copy.deepcopy(self.__meeting_message_embed)
        embed.add_field(name=name, value=value, inline=False)

        components = [Button(style=ButtonStyle.green, label="Join", custom_id="join_meeting")]

        channel = Utils.get_channel(self.bot, GAME_CHANNEL)

        try:
            message = await channel.fetch_message(self.__meeting_message_id)
            await message.edit(content=f'<@&{CREWMATE_ROLE_ID}>', embed=embed, components=components)
        except discord.NotFound:
            await Utils.delete_history(channel)
            message = await channel.send(content=f'<@&{CREWMATE_ROLE_ID}>', embed=embed, components=components)
            self.__meeting_message_id = message.id

    async def __on_join_meeting(self, interaction):
        response = await self.__join_meeting_use_case.execute(interaction.user.id)

        if not response.success:
            await Utils.interact(interaction, response.error_message)
            return
        await Utils.interact(interaction, 'You joined the meeting')

        await self.__join_meeting_message(response.alive_player_count, response.joined_players)

        if response.meeting_started:
            await self.__meeting()

    async def __meeting(self):
        response = None
        message = None
        options = None
        channel = Utils.get_channel(self.bot, GAME_CHANNEL)

        async for response in self.__meeting_use_case.execute():
            if not isinstance(response, MeetingUpdateResponse):
                break

            description = 'Voting ends in:' if response.is_voting else 'Voting begins in:'
            embed = discord.Embed(
                title='Meeting',
                description=f'{description} {response.time_remaining}s',
                colour=self.THEME_COLOR_PRIMARY
            )
            embed.set_thumbnail(url=VOTING_URL if response.is_voting else DISCUSS_URL)

            participants = map(lambda player: player + (' [VOTED]' if player in response.voters else ''), response.player_options.values())
            embed.add_field(name='Participants:', value='\r\n'.join(participants))

            options = options or list(map(lambda kv: SelectOption(label=kv[1], value=kv[0]), response.player_options.items()))
            components = [
                Select(placeholder='Vote for player to eject', options=options, custom_id="vote", disabled=not response.is_voting),
                Button(style=ButtonStyle.red, label='Skip', custom_id="skip", disabled=not response.is_voting)
            ]

            if message:
                await message.edit(embed=embed, components=components)
            else:
                message = await channel.send(embed=embed, components=components)

            time.sleep(1)

        if response.ejected_player:
            if response.was_impostor is None:
                eject_message = f'{response.ejected_player} was ejected'
            else:
                was_impostor = 'was' if response.was_impostor else 'was not'
                eject_message = f'{response.ejected_player} {was_impostor} an Impostor.'
                if response.remaining_impostors != 0 and not response.is_game_over:
                    plurality = 'Impostors remain.' if response.remaining_impostors > 0 else 'Impostor remains.'
                    eject_message += f'\r\n{response.remaining_impostors} {plurality}'
        else:
            eject_message = f'No one was ejected ({response.no_ejection_reason}).'

        embed = discord.Embed(
            title='Meeting Results',
            description=eject_message,
            colour=self.THEME_COLOR_PRIMARY
        )
        embed.set_thumbnail(url=EJECT_URL)

        sleep = 3
        for recipient, vote_count in response.recipient_vote_count_list:
            sleep += 3
            value = f'{vote_count} Votes' if response.anonymous_voting else '>' + '\r\n>'.join(response.recipient_votes_map[recipient])
            embed.add_field(name=f'--{recipient}--', value=value, inline=False)

        await channel.send(embed=embed)
        time.sleep(sleep)

        if response.is_game_over:
            return await self.__end_game()

        await self.__start_round_use_case.execute()
        channel = Utils.get_channel(self.bot, GAME_CHANNEL)
        await Utils.delete_history(channel)
        await self.__game_hud()

        if response.is_electrical_sabotage:
            await self.__electrical_message(response.switch_states)
        elif response.is_com_sabotage:
            await self.__com_sabotage_message(response.rotation_options)

    def __tasks_embed(self, tasks: List[Task], completed_task_names: List[str]=None):
        embed = discord.Embed(
            title='Tasks',
            colour=self.THEME_COLOR_TERTIARY
        )
        embed.set_thumbnail(url=TASK_URL)

        completed_task_names = completed_task_names or []
        for task in tasks:
            name = f'[{str(task.task_type.value).upper()}] {task.name}'
            value = f'*{task.location}*\r\n{task.description}'
            if task.name in completed_task_names:
                name = '~~' + name + '~~'
                value = '~~' + value + '~~'
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def __dm_task_list(self, player_id: int, tasks: List[Task], completed_task_names: List[str]=None):
        user = self.bot.get_user(player_id)
        task_embed = self.__tasks_embed(tasks, completed_task_names)

        try:
            await self.__dm_task_list_message_set[user.id].edit(embed=task_embed)
        except (KeyError, Exception):
            self.__dm_task_list_message_set[user.id] = await user.send(embed=task_embed)

    async def __dm_player(self, player_id: int, message_content: str=None, embed: discord.Embed=None, image: str=None):
        user = self.bot.get_user(player_id)
        await user.send(content=message_content, embed=embed, file=discord.File(image) if image else None)

    async def __dm_code_users(self, code1: int, code2: int):
        embed1 = discord.Embed(
            title="Today's Code",
            colour=self.THEME_COLOR_PRIMARY
        )
        embed1.set_thumbnail(url=O2_PANEL_URL)

        embed2 = copy.copy(embed1)

        embed1.description = str(code1)
        embed2.description = str(code2)

        await self.__dm_player(O2_USER1_ID, embed=embed1)
        await self.__dm_player(O2_USER2_ID, embed=embed2)

    async def __game_hud(self, update_only=False):
        response = await self.__task_completion_use_case.execute()
        if not response.success:
            return

        embed = discord.Embed(
            title='Game in progress',
            colour=self.THEME_COLOR_PRIMARY
        )
        embed.set_thumbnail(url=QUIET_URL)

        lines = 2
        sections_per_line = 4
        bars_per_section = 3
        total_bars = lines * sections_per_line * bars_per_section

        filled_bars = math.floor((response.completed_task_count / (response.total_task_count or 1)) * total_bars)

        progress_bar = '|'
        for line in range(lines):
            for section in range(sections_per_line):
                for bar in range(bars_per_section):
                    if filled_bars:
                        progress_bar += '█'
                        filled_bars -= 1
                    else:
                        progress_bar += '░'
                progress_bar += '|'
            progress_bar += '\r\n|' if line != lines - 1 else ''

        embed.add_field(name='Total Tasks Completed', value=progress_bar, inline=False)

        components = [
            [
                Button(style=ButtonStyle.grey, label="Complete Task", emoji='✅', custom_id="task_list"),
                Button(style=ButtonStyle.grey, label="Report", emoji='📣', custom_id="report_list"),
            ],
            [
                Button(style=ButtonStyle.grey, label="Kill", emoji='🔪', custom_id="kill_list"),
                Button(style=ButtonStyle.grey, label='Sabotage', emoji='☢', custom_id='sabotage_options')
            ],
            [
                Button(style=ButtonStyle.grey, label="Emergency Meeting", emoji='🔴', custom_id="emergency_meeting"),
            ]
        ]

        channel = Utils.get_channel(self.bot, GAME_CHANNEL)

        try:
            message = await channel.fetch_message(self.__hud_message_id)
            await message.edit(embed=embed, components=components)
        except discord.NotFound:
            if update_only:
                return
            message = await channel.send(embed=embed, components=components)
            self.__hud_message_id = message.id

    async def __end_game(self):
        response = await self.__end_game_use_case.execute()

        channel = Utils.get_channel(self.bot, GAME_CHANNEL)

        if not response.success or response.is_impostor_win is None:
            return await channel.send(response.message)

        await Utils.delete_history(channel)

        try:
            file = self.__image_service.create_victory_screen(response.is_impostor_win, response.winner_color_pairs)
            await channel.send(file=discord.File(file))
        except Exception:
            await channel.send(response.message)

    async def __on_sabotage_option(self, interaction):
        response = await self.__can_sabotage_button_use_case.execute(interaction.user.id)

        if not response.success:
            await Utils.interact(interaction, response.message)
        else:
            sabotage_options = []
            if REACTOR_MESSAGE:
                sabotage_options.append(SelectOption(label=self.SABOTAGE_REACTOR, value=self.SABOTAGE_REACTOR))
            if ELECTRICAL_MESSAGE:
                sabotage_options.append(SelectOption(label=self.SABOTAGE_ELECTRICAL, value=self.SABOTAGE_ELECTRICAL))
            if O2_MESSAGE:
                sabotage_options.append(SelectOption(label=self.SABOTAGE_O2, value=self.SABOTAGE_O2))
            if COMMUNICATIONS_MESSAGE:
                sabotage_options.append(SelectOption(label=self.SABOTAGE_COM, value=self.SABOTAGE_COM))

            select = Select(placeholder='Call a Sabotage', options=sabotage_options, custom_id='sabotage')
            await Utils.interact(interaction, content='┗|｀O′|┛', components=[select])

    async def __electrical_sabotage(self, interaction):
        response = await self.__electrical_sabotage_use_case.execute(interaction.user.id)

        if not response.success:
            return await Utils.interact(interaction, response.error_message)

        await interaction.respond(type=self.DEFERRED_UPDATE_MESSAGE)
        await self.__electrical_message(response.switch_states)

    async def __electrical_message(self, switch_states: List[bool]):
        channel = Utils.get_channel(self.bot, GAME_CHANNEL)

        content = f'<@&{CREWMATE_ROLE_ID}> The lights went out (not really, just lock eye contact on your own feet while you can).' \
                  f'\r\n{ELECTRICAL_MESSAGE}'

        components = [ Button(emoji='🟢' if switch_states[i] else '⚫', custom_id=f'switch{i}') for i in range(0, len(switch_states)) ]
        component_chunks = [ components[i:i+5] for i in range(0, len(components), 5) ]

        try:
            message = await channel.fetch_message(self.__electrical_sabotage_message_id)
            await message.edit(content=content, components=component_chunks)
        except discord.NotFound:
            message = await channel.send(content=content, components=component_chunks)
            self.__electrical_sabotage_message_id = message.id

    async def __on_switch(self, interaction):
        request = FlipSwitchRequest(interaction.user.id, int(interaction.custom_id.removeprefix('switch')))
        response = await self.__flip_switch_use_case.execute(request)

        if not response.success:
            await Utils.interact(interaction, response.error_message)
            return

        await interaction.respond(type=self.DEFERRED_UPDATE_MESSAGE)

        if not response.is_resolved:
            return await self.__electrical_message(response.switch_states)

        channel = Utils.get_channel(self.bot, GAME_CHANNEL)
        try:
            message = await channel.fetch_message(self.__electrical_sabotage_message_id)
            await message.delete()
        except discord.NotFound:
            pass

    async def __on_rotate(self, interaction):
        request = RotateKnobRequest(interaction.user.id, int(interaction.custom_id.removeprefix('rotate')))
        response = await self.__rotate_knob_use_case.execute(request)

        await Utils.interact(interaction, response.message)

        if response.is_resolved:
            channel = Utils.get_channel(self.bot, GAME_CHANNEL)
            try:
                message = await channel.fetch_message(self.__com_sabotage_message_id)
                await message.delete()
            except discord.NotFound:
                pass

    async def __reactor_sabotage(self, interaction):
        channel = Utils.get_channel(self.bot, GAME_CHANNEL)
        message = None
        components = [[
            Button(style=ButtonStyle.grey, label="Left", emoji='☢', custom_id="reactor_left"),
            Button(style=ButtonStyle.grey, label="Right", emoji='☢', custom_id="reactor_right"),
        ]]
        response = None
        async for response in self.__reactor_sabotage_use_case.execute(interaction.user.id):
            if not isinstance(response, UrgentSabotageUpdateResponse):
                break

            content = f'<@&{CREWMATE_ROLE_ID}> {REACTOR_MESSAGE}' \
                      f'\r\nReactor meltdown in {response.time_remaining}s...'
            if message:
                await message.edit(content=content, components=components)
            else:
                message = await channel.send(content=content, components=components)
                await interaction.respond(type=self.DEFERRED_UPDATE_MESSAGE)

            time.sleep(1)

        if isinstance(response, UrgentSabotageErrorResponse):
            await Utils.interact(interaction, response.error_message)
        elif isinstance(response, UrgentSabotageFinalResponse):
            if response.is_game_over:
                return await self.__end_game()
            await message.delete()

    async def __o2_sabotage(self, interaction):
        channel = Utils.get_channel(self.bot, GAME_CHANNEL)
        message = None
        response = None
        async for response in self.__o2_sabotage_use_case.execute(interaction.user.id):
            if not isinstance(response, O2UpdateResponse):
                break

            content = f'<@&{CREWMATE_ROLE_ID}> O2 Systems down! Send <@&{SUS_BOT_ROLE_ID}> the codes displayed ' \
                      f'({response.completed_codes}/{response.required_codes}):' \
                      f'\r\n{O2_MESSAGE}' \
                      f'\r\nHypoxia in {response.time_remaining}s...'

            if message:
                await message.edit(content=content)
            else:
                await self.__dm_code_users(response.code1, response.code2)
                message = await channel.send(content=content)
            await interaction.respond(type=self.DEFERRED_UPDATE_MESSAGE)

            time.sleep(1)

        if isinstance(response, UrgentSabotageErrorResponse):
            await Utils.interact(interaction, response.error_message)
        elif isinstance(response, UrgentSabotageFinalResponse):
            if response.is_game_over:
                return await self.__end_game()
            await message.delete()

    async def __com_sabotage(self, interaction):
        response = await self.__com_sabotage_use_case.execute(interaction.user.id)

        if not response.success:
            return await Utils.interact(interaction, response.error_message)

        await interaction.respond(type=self.DEFERRED_UPDATE_MESSAGE)

        await self.__com_sabotage_message(response.rotation_options)

    async def __com_sabotage_message(self, rotation_options: List[int]):
        channel = Utils.get_channel(self.bot, GAME_CHANNEL)

        content = f'<@&{CREWMATE_ROLE_ID}> T̶a̸s̷k̴s̶ ̸m̷u̵s̵t̵ ̶b̶e̷ ̵c̴o̸m̶p̸l̸e̵t̶e̸d̷ ̴i̷n̶ ̸t̴o̴p̶ ̸d̷o̵w̶n̷ ̵o̴r̸d̴e̵r̶ ̴w̵h̷i̵l̶e̷ ̶c̶o̵m̴m̷u̸n̶i̷c̶a̵t̵i̸o̷n̸ ̵i̸s̷ ̴j̵a̵m̴m̸e̶d̵' \
                  f'\r\n{COMMUNICATIONS_MESSAGE}'

        def __rotate_button(rotate: int):
            turn = abs(rotate)
            if rotate > 0:
                emoji = '↩'
                direction = '+'
            else:
                emoji = '↪'
                direction = '-'
            return Button(label=f'{direction}{turn}°', emoji=emoji, custom_id=f'rotate{rotate}')

        components = list(
            map(lambda rotate: [__rotate_button(-rotate), __rotate_button(rotate)], rotation_options))

        message = await channel.send(content=content, components=components)
        self.__com_sabotage_message_id = message.id

    async def __press_reactor_button(self, interaction, is_left_button):
        request = PressReactorButtonRequest(interaction.user.id, is_left_button)
        response = await self.__press_reactor_button_use_case.execute(request)
        await Utils.interact(interaction, response.message)
