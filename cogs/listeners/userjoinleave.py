import discord
from discord.ext import commands
from lamconfig import LamConfig

class UserJoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        server = member.guild
        embed = discord.Embed(
            color = 0xfbbfcb,
            description = f"Welcome, {member.mention}"
        )
        db_cursor = LamConfig.database.cursor()
        db_cursor.execute(f"SELECT autorole_id FROM guilds WHERE id = '{server.id}'")
        arid = db_cursor.fetchone()
        db_cursor = LamConfig.database.cursor()
        db_cursor.execute(f"SELECT welcome_channel_id FROM guilds WHERE id = '{server.id}'")
        wcid = db_cursor.fetchone()
        await server.get_channel(int(wcid[0])).send(embed = embed)
        await member.add_roles(server.get_role(int(arid[0])), reason="Autorole")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        server = member.guild
        embed = discord.Embed(
            color = 0xfbbfcb,
            description = f"Goodbye, {member.mention}"
        )
        db_cursor = LamConfig.database.cursor()
        db_cursor.execute(f"SELECT welcome_channel_id FROM guilds WHERE id = '{server.id}'")
        wcid = db_cursor.fetchone()
        await server.get_channel(int(wcid[0])).send(embed = embed)
