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
    async def hello(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != 586307310654193939:
            await interaction.response.send_message("no", ephemeral=True)
            return

        await interaction.response.send_message("Hello.")
        return

    # /ship
    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(description="ship two users", name="ship")
    async def ship(
        self, interaction: discord.Interaction, user1: discord.User, user2: discord.User
    ) -> None:
        if interaction.user.id != 586307310654193939:
            await interaction.response.send_message("no", ephemeral=True)
            return

        user1_value = user1.id
        user2_value = user2.id

        perc = (user1_value + user2_value) % 100
        await interaction.response.send_message(
            f"Ship between {user1} and {user2}: {perc}%"
        )
        return


# Adds the misc cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MiscCog(bot))
