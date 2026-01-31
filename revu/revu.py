# Standard library imports
import cmd
import logging
import sys

# Third-party imports
import discord
from discord.ext import commands

# Prevents creation of .pyc files
sys.dont_write_bytecode = True

# Configures logging
logging.basicConfig(
    datefmt="\033[1m\033[2m%Y-%m-%d %H:%M:%S\033[0m",
    format="%(asctime)s %(levelname)-6s %(filename)s %(lineno)-3d %(message)s",
    level=logging.INFO,
)


cogs = ["misc"]


# Main class for Revu
class Revu(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=".", intents=discord.Intents.all())

    # Loads all Revu commands
    async def setup_hook(self) -> None:
        for cog in cogs:
            await self.load_extension(f"revu.cogs.{cog}")
            logging.info(f"Revu: Loaded {cog}!")

        await self.tree.sync()
        return await super().setup_hook()

    # Sends when Revu is connected
    async def on_ready(self) -> None:
        await self.change_presence(activity=discord.Game("test"))
        logging.info("Revu has successfully connected!")
