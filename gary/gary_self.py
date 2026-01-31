# Standard library imports
import logging
import sys

# Third-party imports
import selfcord
from selfcord.ext import commands


# Initialize bot
bot = commands.Bot(
    command_prefix=">",
    description="bot",
    help_command=None,
    self_bot=True,
)

# Configures logging
logging.basicConfig(
    datefmt="\033[1m\033[2m%Y-%m-%d %H:%M:%S\033[0m",
    format="%(asctime)s %(levelname)-6s %(filename)s %(lineno)-3d %(message)s",
    level=logging.INFO,
)


# Sends when GARY connects
@bot.event
async def on_ready() -> None:
    global gary_user
    gary_user = bot
    logging.info("GARY: SELF has successfully connected.")


# Runs function for commands/cogs
@bot.event
async def setup_hook() -> None:
    await load_extensions()


# Test command message
@bot.event
async def on_message(message: selfcord.Message) -> int:
    if message.content == "bishi" and message.author.id == 586307310654193939:
        await message.channel.send("```bishi!```")
    return 0


# Loads the command cogs
async def load_extensions() -> int:

    # shell = GARYShell(term_configs)
    # shell.cmdloop()
    # if term_configs["default"]:
    #     for cog in term_configs["d_cogs"]:
    #         await bot.load_extension(f"GARY.cogs.{cog}")
    #         logging.info(f"GARY: Loaded {cog}!")
    # else:
    #     for cog in term_configs["cogs"]:
    #         await bot.load_extension(f"GARY.cogs.{cog}")
    #         logging.info(f"GARY: Loaded {cog}!")
    return 0


# Used for giving Revu access to GARY
async def get_gary() -> commands.Bot:
    await bot.wait_until_ready()
    return gary_user


# Returns bot to run GARY
def get_bot() -> commands.Bot:
    return bot
