import discord
from discord.ext import commands
from lamconfig import LamConfig

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        embed = discord.Embed(
            color = discord.Colour.yellow(),
            title = "Message edited",
        )
        embed.set_author(name=before.author, icon_url=before.author.display_avatar)
        embed.add_field(name="Before", value=before.content or "null", inline=False)
        embed.add_field(name="After", value=after.content or "null", inline=False)
        embed.add_field(name="Channel", value=before.channel.mention, inline=False)
        embed.add_field(name="Message ID", value=before.id)
        embed.add_field(name="User ID", value=before.author.id)
        db_cursor = LamConfig.database.cursor()
        db_cursor.execute(f"SELECT private_log_id FROM guilds WHERE id = '{before.author.guild.id}'")
        plid = db_cursor.fetchone()
        channel = before.author.guild.get_channel(int(plid[0]))
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(
            color = discord.Colour.red(),
            title = "Message deleted",
        )
        embed.set_author(name=message.author, icon_url=message.author.display_avatar)
        embed.add_field(name="Content", value=message.content or "null", inline=False)
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Message ID", value=message.id)
        embed.add_field(name="User ID", value=message.author.id)
        db_cursor = LamConfig.database.cursor()
        db_cursor.execute(f"SELECT private_log_id FROM guilds WHERE id = '{message.author.guild.id}'")
        plid = db_cursor.fetchone()
        channel = message.author.guild.get_channel(int(plid[0]))
        await channel.send(embed = embed)
