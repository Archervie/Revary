import discord
from discord import app_commands
from discord.ext import commands

from utils import BaseGroupCog, is_authorized, log_command


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
class ExampleCog(BaseGroupCog, name=""):
    """ """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__(bot)

    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(description="", name="")
    @is_authorized()
    @log_command()
    async def example(self, interaction: discord.Interaction) -> None:
        """ """
        await interaction.response.send_message("", ephemeral=True)
        assert interaction.command
        self.log.info(f"{interaction.command.name} ran by {interaction.user}.")


# Adds the misc cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExampleCog(bot))
