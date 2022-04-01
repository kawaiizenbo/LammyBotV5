import discord
import time

from discord.commands import slash_command, Option
from discord.ext import commands

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 
        global startTime
        startTime = time.time()

    @slash_command(name="tnt")
    async def tnt(self, ctx):
        """dumb."""
        await ctx.respond(f"BOOOOOOOOOOOM!!!\n\n\n\n{ctx.user.mention} you died by an explosion\n\n\n\nThe WALMART is on fire\n\n\n\n{ctx.user.mention} you blew up {ctx.guild.name}")
