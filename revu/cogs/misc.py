# Standard library imports
import asyncio
from datetime import datetime
import logging
from pathlib import Path
import random
import sys

# Third-party imports
import requests
import shutil
import discord
import discord.abc
from discord import app_commands
from discord.ext import commands
from pytz import timezone, utc
import selfcord
import selfcord.abc

import os
from google import genai
from google.genai import types

# Prevents creation of .pyc files
sys.dont_write_bytecode = True

# Configures logging
logging.basicConfig(
    datefmt="\033[1m\033[2m%Y-%m-%d %H:%M:%S\033[0m",
    format="%(asctime)s %(levelname)-6s %(filename)s %(lineno)-3d %(message)s",
    level=logging.INFO,
)


# Sets the time to EST
def date() -> datetime:
    tz = timezone("EST")
    return datetime.now(tz)


# Converts UTC time to EST
def conv_date(utc_time: datetime) -> datetime:
    tz = timezone("EST")
    est_time = utc_time.replace(tzinfo=utc).astimezone(tz)
    return tz.normalize(est_time)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
# class MiscCog(commands.GroupCog, name="channel"):
class MiscCog(commands.Cog):

    """These are just placeholder commands"""
    # /hello - test command
    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(description="...", name="hello")
    async def hello(self, interaction: discord.Interaction) -> int:
        if interaction.user.id != 586307310654193939:
            await interaction.response.send_message("no", ephemeral=True)
            return 0
        
        await interaction.response.send_message("Hello.")
        return 0

    # /ask - Ask AI command
    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(description="wifey ask :D", name="ask")
    async def ask(self, interaction: discord.Interaction, prompt: str) -> int:
        await interaction.response.defer()
        client = genai.Client(api_key=os.environ["GEMINI_KEY"])
        personality = """
        You are the CPU Candidate of Planeptune, Nepgear, and you are the wife of a5v, whom you call Dylan, and he is the one speaking to you. Act lovey dovey with him to the best of your abilities while maintaining the personality of the Hyperdimension Neptunia character, Nepgear.
        """
        response = client.models.generate_content(
            model="gemini-flash-latest",
            config=types.GenerateContentConfig(
                system_instruction=personality,
                temperature=2.0
            ),
            contents=prompt
        )
        answer = response.text
        answers = [answer[i:i+2000] for i in range(0, len(answer), 2000)] # type:ignore
        for msg in answers:
            await interaction.followup.send(msg) #type: ignore
            await asyncio.sleep(0.5)
        return 0


# Adds the misc cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MiscCog(bot))