import random
from discord.ext import commands
from lamconfig import LamConfig

class XP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 

    @commands.Cog.listener()
    async def on_message(self, message):
        db_cursor = LamConfig.database.cursor()
        db_cursor.execute(f"SELECT xp FROM users WHERE id = '{message.author.id}'")
        old_xp = db_cursor.fetchone()
        if old_xp == None:
            db_cursor.execute(f"INSERT INTO users (id, xp) VALUES ('{message.author.id}', '0')")
            old_xp = [0]
        db_cursor.execute(f"UPDATE users SET xp = '{old_xp[0] + random.randint(0, 10)}' WHERE id = '{message.author.id}'")
        LamConfig.database.commit()
