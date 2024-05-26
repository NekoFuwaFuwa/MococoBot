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

# mute user
async def handle_mute(user: discord.Member, duration, message: discord.Message, log, reason=None):
    embed = discord.Embed(title="Muted", color=discord.Color.red(), description=f"{user.mention} has been muted")
    embed.set_image(url="attachment://vtuber.gif")
    embed.add_field(name="Reason", value=reason, inline=False)
    
    await user.timeout(duration, reason=reason)
    await user.send(f"You have been muted for {duration} in {message.guild.name}. Reason: {reason}")
    await message.channel.send(embed=embed, file=get_rand_gif())
    await log.send(f"User {user.name} [{user.id}] has been muted by nekobot. Reason: {reason}")

    warning_count[user.id] = 0  # Reset warning count after mute

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
            return # ignore messages from bot itself
        
        if admin_role_id in [role.id for role in message.author.roles]:
            return # ignore messages from admins
        
        log = self.neko.get_channel(logs_channel_id)
        uid = message.author.id

        if uid not in warning_count:
            warning_count[uid] = 0 # add member to list

        # block invite links
        invite_links = r"(discord\.gg|discordapp\.com/invite)/[a-zA-Z0-9]+"

        # prevent mass mentions
        member_mention = set(message.mentions)
        total_mentions = sum(message.content.count(f"<@{user.id}>") for user in member_mention)

        if re.search(invite_links, message.content): # block invite links
            try:
                await message.delete()
                warning_count[uid] += 1
                await message.channel.send(f"{message.author.mention} Invite links are not allowed! Warning: {warning_count[uid]}/3", delete_after=7)
                 
                if warning_count[uid] >= 2 and warning_count[uid] == 2: 
                    await message.author.send("I told you to stawwwp!")

                if warning_count[uid] >= 3:
                    mute_duration = datetime.timedelta(minutes=5)
                    reason = "Mass mentions"
                    await handle_mute(message.author, mute_duration, message=message,log=log, reason=reason)

            except Exception as e:
                await log.send(f"[automod] Error: {e}")
            
        elif len(message.mentions) >= 4 or total_mentions >= 4: # prevent mass mentions
            try:
                await message.delete()

                warning_count[uid] += 1
                await message.channel.send(f"{message.author.mention} your message contained too many mentions and was deleted. Warning: {warning_count[message.author.id]}/3", delete_after=7)

                if warning_count[uid] >= 3:
                    mute_duration = datetime.timedelta(minutes=5)
                    reason = "Mass mentions"
                    await handle_mute(message.author, mute_duration, message=message,log=log, reason=reason)

            except Exception as e:
                await log.send(f"[automod] Error: {e}")
            
        else:
            pass
                
async def setup(neko: commands.Bot) -> None:
    await neko.add_cog(Automod(neko))
