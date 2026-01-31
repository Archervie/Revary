# Standard library imports
import asyncio
import logging
import os
import sys
from aiohttp import web
from pathlib import Path
from typing import Union

# Third-party imports
from dotenv import load_dotenv

# Local application imports
from revu.revu import Revu
from gary.gary import GARY
from gary.gary_self import get_bot as GARY_SELF


# Configures logging
logging.basicConfig(
    datefmt="\033[1m\033[2m%Y-%m-%d %H:%M:%S\033[0m",
    format="%(asctime)s %(levelname)-6s %(filename)s %(lineno)-3d %(message)s",
    level=logging.INFO,
)


# Adds health checks so Koyeb doesn't kill bot
async def health_check(request):
    return web.Response(text="Bot is alive!")


async def start_health_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    # Koyeb looks for 0.0.0.0 and Port 8000 by default
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    logging.info("Health check server started on port 8000")


# Main function
async def main() -> None:
    revu = Revu()
    gary = GARY()
    gary_self = GARY_SELF()

    sys.dont_write_bytecode = True

    dotenv_path: Union[str, os.PathLike[str]] = Path(".env")
    load_dotenv(dotenv_path=dotenv_path)

    await start_health_server()

    await asyncio.gather(
        revu.start(os.environ["REVU_TOKEN"]),
        gary.start(os.environ["GARY_TOKEN"]),
        gary_self.start(os.environ["GARY_SELF_TOKEN"]),
    )


# Runs everything
asyncio.run(main())
