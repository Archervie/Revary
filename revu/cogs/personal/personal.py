from datetime import datetime
import json

import discord
from discord import app_commands
from discord.ext import commands

from utils import BaseGroupCog, is_authorized


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
class PersonalCog(BaseGroupCog, name="personal"):
    """ """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__(bot)

    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(description="to-do list", name="tdlist")
    @is_authorized()
    async def to_do_list(self, interaction: discord.Interaction) -> None:
        """ """

        try:
            with open("data/auth.json", "r") as f:
                td_list = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            td_list = {"Today": []}

        await interaction.response.send_message("", ephemeral=True)
        self.log.info(f"{interaction.command.name} ran by {interaction.user}.")


# Adds the misc cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PersonalCog(bot))
