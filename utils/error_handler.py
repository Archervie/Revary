import logging

import discord
from discord import app_commands
from discord.ext import commands

from .base import BaseCog
from .auth_utils import UnauthorizedError


class GlobalErrorHandler(BaseCog):
    """
    Handle all specific errors.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        """
        Respond to specific errors that can occur.

        Args:
            interaction (discord.Interaction): The interaction where the error occurred.
            error (app_commands.AppCommandError): The specific error raised.
        """

        # This handles any unauthorized command access and gives a response
        if isinstance(error, UnauthorizedError):
            bot_name = self.bot.user.name if self.bot.user else "Bot"

            await interaction.response.send_message(
                f"Sorry, Dylan says you aren't allowed to do that.",
                ephemeral=True,
            )

            self.log.warning(
                f"Unauthorized access attempt by {interaction.user} on {bot_name}"
            )

        # This handles missing permissions
        elif isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(
                "Sorry, you don't have permission to do this.", ephemeral=True
            )

        # This handles any cooldown errors.
        elif isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"There seems to be a cooldown. Try again in {error.retry_after:.1f} seconds.",
                ephemeral=True,
            )

            self.log.info(f"Cooldown needed.")

        # For any unexpected bugs
        else:
            self.log.error(
                f"Ignoring exception in command {interaction.command}: {error}"
            )

            # Only send a message if we haven't already responded
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "An unknown error seems to have occurred. Please investigate",
                    ephemeral=True,
                )
            logging.warning(
                "An unknown error seems to have occurred. Please investigate"
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(GlobalErrorHandler(bot))
