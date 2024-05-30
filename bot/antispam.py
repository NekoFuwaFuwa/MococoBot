# This is part of the automod but separate onto a different file to avoid any confusion.

import discord
import time
import threading
import logging
import datetime

from collections import defaultdict, deque
from discord.ext import commands
from .config import *
from .automod import handle_mute

logger = logging.getLogger(__file__)

async def purge_messages(user: discord.Member, channel: discord.TextChannel, amount:int):
    try: # yes i know its ugly and slow .... but it works
        deleted = 0
        async for message in channel.history(limit=100):
            if message.author == user:
                await message.delete()
                deleted += 1
                if deleted >= amount:
                    break
    except:
        pass

def report():
    time.sleep(4)
    print("Antispam Init")

class Automod(commands.Cog):
    def __init__(self, neko):
        self.neko = neko
        self.user_messages = defaultdict(lambda: deque(maxlen=7))
    
    @commands.Cog.listener()
    async def on_ready(self):
        threading.Thread(target=report).start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.neko.user:
            return  # Ignore messages from the bot itself
        
        if admin_role_id in [role.id for role in message.author.roles]:
            return  # Ignore messages from admins
        
        if message.author.timed_out_until is not None:
            now_aware = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            if message.author.timed_out_until > now_aware:
                return  # Ignore messages from users who are currently timed out
        
        log= self.neko.get_channel(logs_channel_id)
        uid = message.author.id

        # anti-spam
        now = datetime.datetime.utcnow().timestamp()
        self.user_messages[uid].append(now)

        if len(self.user_messages[uid]) == 7 and (now - self.user_messages[uid][0]) <= 10:
            await handle_mute(message.author, 120, message, log, reason="Spamming")
            await purge_messages(message.author, message.channel, 7)
            self.user_messages[uid].clear()  # clear messages after muting
            return


async def setup(neko: commands.Bot) -> None:
    await neko.add_cog(Automod(neko))
