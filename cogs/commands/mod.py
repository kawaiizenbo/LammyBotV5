import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from lamconfig import LamConfig

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 

    @slash_command(name="kick")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: Option(discord.User, "User to kick"), reason: Option(str, "Reason of kick", required=False, default="No reason specified")):
        """Kick a specified user."""
        await ctx.guild.kick(user = user, reason = f"Kicked by {ctx.author}: {reason}")
        embed = discord.Embed()
        embed.color = 0xfbbfcb
        embed.title = "Kicked user."
        embed.description = f"`{user.name}#{user.discriminator}` was kicked\nReason: `{reason}`\nUser ID: `{user.id}`"
        embed.set_thumbnail(url = user.avatar.url)
        await ctx.respond(embed = embed, delete_after=5.0)
        db_cursor = LamConfig.database.cursor()
        db_cursor.execute(f"SELECT public_log_id FROM guilds WHERE id = '{ctx.guild.id}'")
        plid = db_cursor.fetchone()
        await ctx.guild.get_channel(int(plid)).send(embed = embed)

    @slash_command(name="ban")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user: Option(discord.User, "User to ban"), reason: Option(str, "Reason of ban", required=False, default="No reason specified")):
        """Ban a specified user."""
        await ctx.guild.ban(user = user, delete_message_days = 0, reason = f"Banned by {ctx.author}: {reason}")
        embed = discord.Embed()
        embed.color = 0xfbbfcb
        embed.title = "Banned user."
        embed.description = f"`{user.name}#{user.discriminator}` was banned\nReason: `{reason}`\nUser ID: `{user.id}`"
        embed.set_thumbnail(url = user.avatar.url)
        await ctx.respond(embed = embed, delete_after=5.0)
        db_cursor = LamConfig.database.cursor()
        db_cursor.execute(f"SELECT public_log_id FROM guilds WHERE id = '{ctx.guild.id}'")
        plid = db_cursor.fetchone()
        await ctx.guild.get_channel(int(plid)).send(embed = embed)

    @slash_command(name="unban")
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, user: Option(discord.User, "User to unban"), reason: Option(str, "Reason of unban", required=False, default="No reason specified")):
        """Unban a specified user."""
        await ctx.guild.unban(user = user, reason = f"Unbanned by {ctx.author}: {reason}")
        embed = discord.Embed()
        embed.color = 0xfbbfcb
        embed.title = "Unbanned user."
        embed.description = f"`{user.name}#{user.discriminator}` was unbanned\nReason: `{reason}`\nUser ID: `{user.id}`"
        embed.set_thumbnail(url = user.avatar.url)
        await ctx.respond(embed = embed, delete_after=5.0)
        db_cursor = LamConfig.database.cursor()
        db_cursor.execute(f"SELECT public_log_id FROM guilds WHERE id = '{ctx.guild.id}'")
        plid = db_cursor.fetchone()
        await ctx.guild.get_channel(int(plid)).send(embed = embed)
