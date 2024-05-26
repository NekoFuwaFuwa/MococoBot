import discord
import time
import threading
import logging
import re
import datetime
import random

from discord.ext import commands
from .config import *

logger = logging.getLogger(__file__)

warning_count = {}

gifs = ["cute.gif", "gawrgura.gif"]

def get_rand_gif():
    return discord.File(f"../media/{random.choice(gifs)}", filename="vtuber.gif")

def report():
    time.sleep(4)
    print("Automod Init")

class Automod(commands.Cog):
    def __init__(self, neko):
        self.neko = neko

    @commands.Cog.listener()
    async def on_ready(self):
        threading.Thread(target=report).start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.neko.user:
            return
            
        if admin_role_id in [role.id for role in message.author.roles]:
            return
        
        log = self.neko.get_channel(logs_channel_id)
        
        # block invite links
        invite_links = r"(discord\.gg|discordapp\.com/invite)/[a-zA-Z0-9]+"
        if re.search(invite_links, message.content):
            try:
                await message.delete()

                uid = message.author.id
                if uid not in warning_count:
                    warning_count[uid] = 0
                warning_count[uid] += 1
                await message.channel.send(f"{message.author.mention} Invite links are not allowed! Warning {warning_count[uid]}/3", delete_after=7)

                if warning_count[uid] >= 2 and warning_count[uid] == 2: # only send message at 2
                    await message.author.send("I told you to stawwwp!")

                if warning_count[uid] >= 3:
                    embed = discord.Embed(title="Muted", color=discord.Color.red(), description=f"{message.author.mention} has been muted")
                    embed.set_image(url="attachment://vtuber.gif")
                    embed.add_field(name="Reason", value="Sending Invite links", inline=False)
                    await message.author.timeout(datetime.timedelta(minutes=5), reason="Spamming invite links")
                    await message.author.send(f"You have been muted for 5 minutes in {message.guild.name}. Reason: Spamming invite links")
                    await message.channel.send(embed=embed, file=get_rand_gif)

                    warning_count[uid] = 0 # reset after mute

            except Exception as e:
                await log.send(f"[automod] Error: {e}")
                    

async def setup(neko: commands.Bot) -> None:
    await neko.add_cog(Automod(neko))
