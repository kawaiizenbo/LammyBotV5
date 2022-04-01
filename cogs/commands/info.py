from asyncio.windows_events import NULL
import discord, datetime, time, platform

from discord.commands import slash_command, Option
from discord.ext import commands
from lamconfig import LamConfig

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 
        global startTime
        startTime = time.time()

    @slash_command(name="userinfo")
    async def userinfo(self, ctx, member: Option(discord.Member, "User to see info of")):
        """Gets user info."""
        user = member
        cd: str = user.created_at.strftime("%Y %b %d %H:%M:%S")
        jd: str = user.joined_at.strftime("%Y %b %d %H:%M:%S")
        froles: str = ""
        for r in user.roles:
            if r.name == "@everyone":
                continue
            froles += f"{r.mention} "
        _permissions_dict = dict(iter(user.guild_permissions))
        permissions = (
            ", ".join(
            [
            (permission.replace("_", " ").title())
            for permission in _permissions_dict
            if _permissions_dict[permission]
            ]
        )
        if not _permissions_dict["administrator"]
        else "Administrator"
        )
        if user == ctx.guild.owner:
            permissions = "Server Owner"
        embed = discord.Embed(
            color = 0xfbbfcb,
            title = f"User info",
        )
        embed.set_author(name=user, icon_url=user.display_avatar)
        embed.add_field(name="User ID", value=f"`{user.id}`", inline=False)
        embed.add_field(name="Creation Date", value=f"`{cd}`")
        embed.add_field(name="Join Date", value=f"`{jd}`")
        embed.add_field(name="Roles", value=froles, inline=False)
        embed.add_field(name="Permissions", value=permissions, inline=False)
        await ctx.respond(embed = embed)

    @slash_command(name="riitag")
    async def riitag(self, ctx, member: Option(discord.Member, "User to see RiiTag of")):
        """Gets user's RiiTag"""
        user = member or ctx.author
        embed = discord.Embed(
            color = 0xfbbfcb,
            title = f"RiiTag",
        )
        embed.set_author(name=user, icon_url=user.display_avatar)
        embed.set_image(url=f"https://tag.rc24.xyz/{user.id}/tag.max.png")
        await ctx.respond(embed = embed)

    @slash_command(name="about")
    async def about(self, ctx):
        """Get bot info."""
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        embed = discord.Embed(
            color = 0xfbbfcb,
            title = "LammyBot V5 Info",
        )
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name="Latency", value=round(self.bot.latency*1000, 1))
        embed.add_field(name="Pycord Version", value=discord.__version__,)
        embed.add_field(name="Host OS", value=f"{platform.system()} {platform.release()}")
        await ctx.respond(embed = embed)
    
    @slash_command(name="kill")
    async def kill(self, ctx):
        """stop bot (bot owner only)"""
        if ctx.author.id != self.bot.owner_id:
            await ctx.respond("You arent allowed to do that.")
        else:
            await ctx.respond("Lammy fell out of this world.")
            exit(0)

    @slash_command(name="source")
    async def source(self, ctx):
        """show bot source"""
        embed = discord.Embed(
            color = 0xfbbfcb,
            title = f"LammyBot V5 Source code",
        )
        embed.description = "https://github.com/kawaiizenbo/LammyBotV5"
        await ctx.respond(embed = embed)

    @slash_command(name="xp")
    async def xp(self, ctx, member: Option(discord.Member, "User to see xp of")):
        """Gets user XP."""
        user = member
        embed = discord.Embed(
            color = 0xfbbfcb,
            title = f"User XP",
        )
        embed.set_author(name=user, icon_url=user.display_avatar)
        db_cursor = LamConfig.database.cursor()
        db_cursor.execute(f"SELECT xp FROM users WHERE id = '{user.id}'")
        xp = db_cursor.fetchone()
        if xp == None:
            db_cursor.execute(f"INSERT INTO users (id, xp) VALUES ('{user.id}', '0')")
            LamConfig.database.commit()
            xp = [0]
        embed.add_field(name="XP", value=str(xp[0]))
        await ctx.respond(embed = embed)
