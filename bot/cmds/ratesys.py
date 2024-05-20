import discord
import threading
import time
import logging
import asyncio
import re

from discord.ext import commands
from discord import app_commands
from .config import *

logger = logging.getLogger(__file__)

def report():
    time.sleep(4)
    print("Rating System Init")

class RateSys(commands.Cog):
    def __init__(self, neko):
        self.neko = neko

    @commands.Cog.listener()
    async def on_ready(self):
        threading.Thread(target=report).start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.neko.user:
            return # dont let the bot react to its own message
        
        tenor_links = re.compile(r'https://tenor\.com/view/.*')
        
        if message.channel.id == memes_channel_id:
            if any(message.attachments) or tenor_links.search(message.content):
                await message.add_reaction('👍')
                await asyncio.sleep(1)
                await message.add_reaction('👎')

async def setup(neko: commands.Bot) -> None:
    await neko.add_cog(RateSys(neko))