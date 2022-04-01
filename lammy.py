from operator import truediv
import discord

from lamconfig import LamConfig

from cogs.commands.info import InfoCommands
from cogs.commands.fun import FunCommands
#from cogs.commands.config import ConfigCommands
from cogs.commands.mod import ModCommands

from cogs.listeners.userjoinleave import UserJoinLeave
from cogs.listeners.filter import Filter
from cogs.listeners.logger import Logger
from cogs.listeners.xp import XP

description = """lammy bot v5"""

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.presences = True

bot = discord.Bot(intents = intents)

# Command Cogs
bot.add_cog(InfoCommands(bot))
bot.add_cog(FunCommands(bot))
#bot.add_cog(ConfigCommands(bot))
bot.add_cog(ModCommands(bot))

# Listener Cogs
bot.add_cog(UserJoinLeave(bot))
bot.add_cog(Filter(bot))
bot.add_cog(Logger(bot))
bot.add_cog(XP(bot))

# Events
@bot.event
async def on_ready():
    print("Lammy Bot V5 init")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    if LamConfig.database:
        print("Database connection success.")
    print("------")

@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f"Joined new guild! '{guild.name}' ({guild.id})")
    db_cursor = LamConfig.database.cursor()
    db_cursor.execute(f"INSERT INTO guilds (id) VALUES ('{guild.id}')")
    LamConfig.database.commit()

@bot.event
async def on_guild_remove(guild: discord.Guild):
    print(f"Removed from guild :( '{guild.name}' ({guild.id})")
    db_cursor = LamConfig.database.cursor()
    db_cursor.execute(f"DELETE FROM guilds WHERE '{guild.id}'")
    LamConfig.database.commit()

bot.run(LamConfig.cfg["token"])
