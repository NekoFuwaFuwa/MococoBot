import discord
import threading
import time
import logging
import time
import requests
import random

from discord.ext import commands
from discord import app_commands
from .config import *

logger = logging.getLogger(__file__)

blkls = [] # niggas id

def report():
    time.sleep(4)
    print("Presence Init")

class Verification(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
    
    @discord.ui.button(label="Verify", custom_id= "verify_button", style= discord.ButtonStyle.success)
    async def verify(self, interaction: discord.Interaction, button):
        role = verify_role_id
        user = interaction.user
        if role not in [y.id for y in user.roles]:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message("You have been verified! UwU", ephemeral=True)
        else:
            await interaction.response.send_message("You are already verified! UwU", ephemeral=True)

class presence(commands.Cog):
    def __init__(self, neko: commands.Bot):
        self.neko = neko

    @commands.Cog.listener()
    async def on_ready(self):
        threading.Thread(target=report).start()
        self.neko.add_view(Verification())
        channel =  self.neko.get_channel(verify_channel_id)
        try:
            await channel.purge(limit = 1)
        except:
            pass # ignore

        file1 = discord.File("../media/fatekissrules.gif", filename="rules.gif")
        file2 = discord.File("../media/mococo-lick.gif", filename="lick.gif")

        embed =  discord.Embed(title = "Rules", color = 0xff0099, description = "Before view other channels, plz read the rules or else ...")
        embed.add_field(name="***No Slurs***", value="Do not use slurs especically if you cannot claim them.", inline=False)
        embed.add_field(name="***Be Kind***", value="Respect everyone in the server!", inline=False)
        embed.add_field(name="***English Only***", value="Talk in English so the cute neko maids can monitor the chats and make sure you're not breaking any rules while chatting", inline=False)
        embed.add_field(name="***No Spamming***", value="Do not spam in chats", inline=False)
        embed.add_field(name="***No Venting***", value="Do not vent in the server as we can to keep good enviornment and a comfortable place for everyone.", inline=False)
        embed.add_field(name="***Minimum Age***", value="According to the rules of discord you have to be at least 13 years old.", inline=False)
        embed.add_field(name="***Discord Guidelines***", value="Here is the link of the global discord rules https://discord.com/guidelines", inline=False)
        embed.set_footer(text="Consequences: 3 times time out will result in a kick and 5 times time out will result in ban please listen to the moderators.")
        embed.set_image(url="attachment://rules.gif")
        embed.set_thumbnail(url="attachment://lick.gif")


        await channel.send(embed = embed, view = Verification(), files=[file1, file2])

    # welcome message
    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member: discord.Member):
        greetings_quotes = ["Hallo, Hallo,  BAU BAU!", "We hope you have a howl of a day!", "BAU BAU!", "How about we get you all nice and fluffy~?"]
        user = f"{member.name}#{member.discriminator}"
        logger.info(f"{user} joined the server")
        guild = self.neko.get_guild(guild_id)
        if (time.time() - member.created_at.timestamp() < required_minimum_time):
            if not member.bot: # dont kick bots
                log = self.neko.get_channel(logs_channel_id)
                await member.send(f"You have been kicked from ***{guild.name}***. You can always join back at https://discord.hololewd.com/ . \nReason: Account too young.")
                await member.kick(reason="Account too young. ")
                await log.send(f"User {user} was kicked by Mococo. Reason: Account too young.")
                return

        quote = random.choice(greetings_quotes)
        niggas = member.guild.member_count
        channel = self.neko.get_channel(welcome_channel_id)
        #api = requests.get(f'https://api.hololewd.com/makegif/?caption={member.name}').json()

        embed = discord.Embed(title="Catgirls", description="Welcome to the server!", color=0xff0099)
        embed.set_author(name=f"{user}", icon_url=member.avatar.url)
        embed.set_thumbnail(url=guild.icon.url)
        #embed.set_image(url=api['result'])
        embed.set_footer(text=f"{niggas} Members")

        await channel.send(f"{member.mention} {quote}", embed=embed)

    @commands.Cog.listener(name="on_member_remove")
    async def on_member_remove(self, member: discord.Member):
        if member.id in blkls:
            return

        user = f"{member.name}#{member.discriminator}"
        channel = self.neko.get_channel(welcome_channel_id)
        niggas = member.guild.member_count
        embed = discord.Embed(title=f"{user} left the server", color=discord.Color.red())
        embed.set_author(name=f"{user}", icon_url=member.avatar.url)
        embed.set_footer(text=f"{niggas} Members")

        await channel.send(embed=embed)

async def setup(neko: commands.Bot) -> None:
    await neko.add_cog(presence(neko))
