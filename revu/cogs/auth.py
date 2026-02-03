import logging

import discord
from discord import app_commands
from discord.ext import commands

from utils import BaseGroupCog, is_authorized


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
class AuthCog(BaseGroupCog, name="auth"):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__(bot)

    # /authorize - test command
    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(
        description="Authorize a user to use the bot.", name="authorize"
    )
    @is_authorized()
    async def authorize(
        self, interaction: discord.Interaction, user: discord.User | None = None
    ) -> None:
        if not user:
            user = interaction.user.name
            user_id = interaction.user.id
        else:
            user_id = user.id

        if self.std.auth.verify(user_id):
            await interaction.response.send_message(
                f"User {user} is already authorized.", ephemeral=True
            )
        else:
            self.std.auth.authorize(user_id)
            await interaction.response.send_message(
                f"Successfully authorized user {user}", ephemeral=True
            )
            self.log.info(f"Successfully authorized user {user}")


# Adds the auth cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AuthCog(bot))
