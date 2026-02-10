from __future__ import annotations
from functools import wraps
from typing import TYPE_CHECKING

from discord import app_commands, Interaction
from discord.ext import commands

from .standard import Standard


def log_command():
    def decorator(func):
        @wraps(func)
        async def wrapper(
            self: BaseCog, interaction: Interaction, *args, **kwargs
        ) -> None:
            cmd = interaction.command
            if isinstance(cmd, app_commands.Command) and cmd.parent:
                full_name = f"{cmd.parent.name}.{cmd.name}"
            elif cmd:
                full_name = cmd.name
            else:
                full_name = "Unknown"

            self.log.info(f"Command '{full_name}' ran by {interaction.user}: {kwargs}")

            return await func(self, interaction, *args, **kwargs)

        return wrapper

    return decorator


class BaseCog(commands.Cog):
    """
    A custom Cog that automatically sets specific shortcuts. Serves as a replacement for
    command.Cog.
    """

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

        self.bot = bot
        assert bot.user
        self.std = Standard(bot.user.name)

        self.auth = self.std.auth
        self.dates = self.std.dates
        self.log = self.std.logger


class BaseGroupCog(commands.GroupCog):
    """
    A custom Cog that automatically sets specific shortcuts. Serves as a replacement for
    command.GroupCog.
    """

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

        self.bot = bot
        assert bot.user
        self.std = Standard(bot.user.name)

        self.auth = self.std.auth
        self.dates = self.std.dates
        self.log = self.std.logger
