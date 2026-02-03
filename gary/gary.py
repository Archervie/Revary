import discord
from discord.ext import commands

from utils import Standard

cogs = ["ai", "misc"]


# Main class for GARY
class GARY(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=".", intents=discord.Intents.all())
        self.std = Standard()

    # Loads all GARY commands
    async def setup_hook(self) -> None:
        for cog in cogs:
            await self.load_extension(f"gary.cogs.{cog}")
            self.std.log(f"GARY: Loaded {cog}!")
        await self.load_extension("utils.error_handler")
        await self.tree.sync()
        return await super().setup_hook()

    # Sends when GARY is connected
    async def on_ready(self) -> None:
        await self.change_presence(activity=discord.Game("test"))
        self.std.log("GARY has successfully connected!")
