import asyncio
import logging
import os
from pathlib import Path
from typing import Union

import discord
from dotenv import load_dotenv

from gary import GARY
from gary.gary_self import get_bot as GARY_SELF
from revu import Revu

discord.utils.setup_logging(level=logging.INFO, root=True)


async def main() -> None:
    """
    Runs all three bots concurrently via asyncio.
    """

    revu = Revu()
    gary = GARY()
    gary_self = GARY_SELF()

    dotenv_path: Union[str, os.PathLike[str]] = Path(".env")
    load_dotenv(dotenv_path=dotenv_path)

    await asyncio.gather(
        revu.start(os.environ["REVU_TOKEN"]),
        gary.start(os.environ["GARY_TOKEN"]),
        gary_self.start(os.environ["GARY_SELF_TOKEN"]),
    )


# Runs everything
asyncio.run(main())
