import discord
from discord.ext import commands

from utils import Standard

cogs = ["ai"]


# Main class for GARY
class GARY(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=".", intents=discord.Intents.all())
        self.std = Standard("GARY")

    # Loads all GARY commands
    async def setup_hook(self) -> None:
        for cog in cogs:
            await self.load_extension(f"gary.cogs.{cog}")
            self.std.logger.info(f"Loaded {cog}!")
        await self.load_extension("utils.error_handler")
        await self.tree.sync()
        return await super().setup_hook()

    # Sends when GARY is connected
    async def on_ready(self) -> None:
        await self.change_presence(activity=discord.Game(""))
        latency = round(self.latency, 3)
        self.std.logger.info(f"Successfully connected! Latency: {latency}ms")

