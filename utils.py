from typing import List

import discord


class Utils:
    @staticmethod
    def get_channel(bot, name):
        return discord.utils.get(bot.get_all_channels(), name=name, type=discord.ChannelType.text)

    @staticmethod
    async def history(channel, message_contains=None, exclude_message_id=None) -> List[discord.Message]:
        messages = await channel.history().flatten()

        if exclude_message_id:
            messages = list(filter(lambda message: exclude_message_id != message.id, messages))

        if message_contains:
            messages = list(filter(lambda message: message_contains in message.content, messages))

        return messages

    @staticmethod
    async def delete_history(channel, message_contains=None, exclude_message_id=None):
        history = await Utils.history(channel, message_contains, exclude_message_id)
        if history:
            await channel.delete_messages(history)

    @staticmethod
    async def interact(interaction, content=None, components=None):
        try:
            await interaction.send(content=content, components=components)
        except (discord.NotFound, discord.DiscordServerError):
            pass
