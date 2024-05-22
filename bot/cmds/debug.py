import discord
import os
import time
import threading
import psutil

from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone

def report():
    time.sleep(4)
    print("Debug Init")

def bytes_to_gb(data):
    return round(data / (1024 ** 3), 1)

class Debug(commands.Cog):
    def __init__(self, neko):
        self.neko = neko
        self.neko_time = datetime.now(timezone.utc)

    @commands.Cog.listener()
    async def on_ready(self):
        threading.Thread(target=report).start()

    @app_commands.command(name="debug", description="Current status")
    async def debug(self, interaction: discord.Interaction):
        # uptime
        now = datetime.now(timezone.utc)
        uptime = now - self.neko_time
        days = uptime.days
        hrs, re = divmod(uptime.seconds, 3600)
        mins , _ = divmod(re, 60)

        #cpu and ram usage
        #time.sleep(0.5)
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        ram_used = bytes_to_gb(psutil.virtual_memory().used)
        ram_total = bytes_to_gb(psutil.virtual_memory().total)


        embed = discord.Embed(title="Debug | Fuwa fetch", description=f"""***Ping***: {round(self.neko.latency * 1000)}ms
***Uptime***: {days} days, {hrs} hours, {mins} mins
***PID***: {os.getpid()}
***CPU***: {cpu}%
***Memory***: {ram}% | {ram_used} / {ram_total} GB

""")
        await interaction.response.send_message(embed=embed)

async def setup(neko: commands.Bot):
    await neko.add_cog(Debug(neko))
