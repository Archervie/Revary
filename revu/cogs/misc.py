import logging

import discord
from discord import app_commands
from discord.ext import commands

from utils import is_authorized, BaseGroupCog


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
class MiscCog(BaseGroupCog, name="misc"):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    # /test
    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(description="Test!", name="test")
    @is_authorized()
    async def test(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Test complete!", ephemeral=True)
        self.log.info("Test complete!")

    # /ship
    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(description="ship two users", name="ship")
    @is_authorized()
    async def ship(
        self, interaction: discord.Interaction, user1: discord.User, user2: discord.User
    ) -> None:
        user1_value = user1.id
        user2_value = user2.id

        perc = (user1_value + user2_value) % 100
        await interaction.response.send_message(
            f"Ship between {user1} and {user2}: {perc}%"
        )


# Adds the misc cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MiscCog(bot))
