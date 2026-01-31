# Standard library imports
import cmd
import logging
import sys

# Third-party imports
import discord
from discord.ext import commands

# Local imports
from terminal import GARYShell

# Prevents creation of .pyc files
sys.dont_write_bytecode = True

# Configures logging
logging.basicConfig(
    datefmt="\033[1m\033[2m%Y-%m-%d %H:%M:%S\033[0m",
    format="%(asctime)s %(levelname)-6s %(filename)s %(lineno)-3d %(message)s",
    level=logging.INFO,
)


# Main class for GARY
class GARY(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=".", intents=discord.Intents.all())

    # Loads all GARY commands
    async def setup_hook(self) -> None:
        term_configs = {
            "cogs": [],
            "a_cogs": [
                ""
            ],
            "d_cogs": [
                "misc", "ai"
            ],
            "default": False
        }

        shell = GARYShell(term_configs)
        shell.cmdloop()

        if term_configs["default"]:
            for cog in term_configs["d_cogs"]:
                await self.load_extension(f"gary.cogs.{cog}")
                logging.info(f"GARY: Loaded {cog}!")
        else:
            for cog in term_configs["cogs"]:
                await self.load_extension(f"gary.cogs.{cog}")
                logging.info(f"GARY: Loaded {cog}!")

        await self.tree.sync()
        return await super().setup_hook()

    # Sends when GARY is connected
    async def on_ready(self) -> None:
        await self.change_presence(activity=discord.Game("test"))
        logging.info("GARY has successfully connected!")

