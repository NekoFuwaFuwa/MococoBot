import discord
import threading
import time
import logging

from discord.ext import commands
from discord import app_commands

logger = logging.getLogger(__file__)

def report():
    time.sleep(4)
    print("Tmp Init")

class method(commands.Cog):
    def __init__(self, neko):
        self.neko = neko

    @commands.Cog.listener()
    async def on_ready(self):
        threading.Thread(target=report).start()

    @app_commands.command(name="TMP", description="This and that")
    async def cmd(self, interaction: discord.Interaction, arg):
        print(arg)

async def setup(neko: commands.Bot) -> None:
    await neko.add_cog(method(neko))