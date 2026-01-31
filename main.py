# Standard library imports
import asyncio
import os
import sys
from pathlib import Path
from typing import Union

# Third-party imports
from dotenv import load_dotenv

# Local application imports
from revu.revu import Revu
from gary.gary import GARY
from gary.gary_self import get_bot as GARY_SELF


# Main function
async def main() -> None:
    revu = Revu()
    gary = GARY()
    gary_self = GARY_SELF()

    sys.dont_write_bytecode = True

    dotenv_path: Union[str, os.PathLike[str]] = Path(".env")
    load_dotenv(dotenv_path=dotenv_path)

    await asyncio.gather(
        revu.start(os.environ["REVU_TOKEN"]),
        gary.start(os.environ["GARY_TOKEN"]),
        gary_self.start(os.environ["GARY_SELF_TOKEN"]),
    )


# Runs everything
asyncio.run(main())
