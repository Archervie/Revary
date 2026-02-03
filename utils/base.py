from discord.ext import commands
from .standard import Standard


class BaseCog(commands.Cog):
    """
    A custom Cog that automatically sets specific shortcuts. Serves as a replacement for
    command.Cog.
    """

    def __init__(self, bot: commands.Bot):
        super().__init__()

        self.bot = bot
        self.std = Standard()

        self.auth = self.std.auth
        self.dates = self.std.dates
        self.log = self.std.logger


class BaseGroupCog(commands.GroupCog):
    """
    A custom Cog that automatically sets specific shortcuts. Serves as a replacement for
    command.GroupCog.
    """

    def __init__(self, bot: commands.Bot):
        super().__init__()

        self.bot = bot
        self.std = Standard()

        self.auth = self.std.auth
        self.dates = self.std.dates
        self.log = self.std.logger
