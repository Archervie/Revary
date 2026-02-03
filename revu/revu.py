import discord
from discord.ext import commands

from utils import Standard

initial_cogs = ["auth", "misc", "user"]


class Revu(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=".", intents=discord.Intents.all())
        self.std = Standard("Revu")

    async def setup_hook(self) -> None:
        for cog in initial_cogs:
            await self.load_extension(f"revu.cogs.{cog}")
            self.std.logger.info(f"Loaded {cog}!")
        await self.load_extension("utils.error_handler")
        await self.tree.sync()
        return await super().setup_hook()

    async def on_ready(self) -> None:
        await self.change_presence(activity=discord.Game(""))
        latency = round(self.latency, 3)
        self.std.logger.info(f"Successfully connected! Latency: {latency}ms")
