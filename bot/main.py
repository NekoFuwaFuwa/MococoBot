import discord
import asyncio
import os
import logging

from discord.ext import commands
from cmds import config

intents = discord.Intents.all()
intents.message_content = True

prefix = "./"
neko = commands.Bot(command_prefix= prefix, intents=intents)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
@neko.event
async def on_ready():
    await neko.change_presence(activity=discord.Game("FUWAMOCO"))
    await neko.tree.sync()
    print("uwu")

async def load():
    for file in os.listdir('./cmds'):
        if file.endswith('.py') and not file.startswith('config'):
            await neko.load_extension(f"cmds.{file[:-3]}")

async def main():
    await load()
    await neko.start(config.token())

asyncio.run(main())
