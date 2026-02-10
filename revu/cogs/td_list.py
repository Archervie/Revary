from datetime import datetime
import json

import discord
from discord import app_commands
from discord.ext import commands

from utils import BaseGroupCog, is_authorized, log_command


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
class ToDoCog(BaseGroupCog, name="to-do"):
    """ """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__(bot)

    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(description="to-do list", name="list")
    @is_authorized()
    @log_command()
    async def to_do_list(self, interaction: discord.Interaction) -> None:
        """ """

        try:
            with open("data/td_list.json", "r") as f:
                td_list = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            td_list = {"List": []}

        await interaction.response.send_message(
            f"List: {td_list["List"]}", ephemeral=True
        )

    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(description="write to to-do list", name="add")
    @is_authorized()
    @log_command()
    async def to_do_list_write(
        self, interaction: discord.Interaction, task: str, date: str
    ) -> None:
        """ """

        try:
            with open("data/td_list.json", "r") as f:
                id_list = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            id_list = {"List": []}

        with open("data/td_list.json", "w") as f:
            id_list["List"].append(f"{task} due {date}")
            json.dump(id_list, f, indent=4)

        await interaction.response.send_message(
            f"Added {task} to to-do list!", ephemeral=True
        )


# Adds the misc cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ToDoCog(bot))
