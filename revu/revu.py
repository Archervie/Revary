import discord
from discord.ext import commands

from utils import Standard

cogs = ["misc", "auth"]


class Revu(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=".", intents=discord.Intents.all())
        self.std = Standard()

    async def setup_hook(self) -> None:
        for cog in cogs:
            await self.load_extension(f"revu.cogs.{cog}")
            self.std.log(f"Revu: Loaded {cog}!")
        await self.load_extension("utils.error_handler")
        await self.tree.sync()
        return await super().setup_hook()

    async def on_ready(self) -> None:
        await self.change_presence(activity=discord.Game("test"))
        self.std.log("Revu has successfully connected!")
