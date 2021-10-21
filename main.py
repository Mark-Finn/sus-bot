import sys

import discord
from discord.ext import commands
from discord_components import ComponentsBot

from Container import Container
from config import BOT_KEY

from cogs.game import Game


def main():
    intents = discord.Intents.default()
    intents.members = True
    bot = ComponentsBot(command_prefix='.', intents=intents)
    bot.add_cog(Game(bot))

    @bot.command()
    @commands.has_role('admin')
    async def load(ctx, extension):
        bot.load_extension(f'cogs.{extension}')

    @bot.command()
    @commands.has_role('admin')
    async def unload(ctx, extension):
        bot.unload_extension(f'cogs.{extension}')

    bot.run(BOT_KEY)

if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[sys.modules[__name__]])

    main()

