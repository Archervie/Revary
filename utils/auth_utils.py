import json
import hashlib
import os

import discord
from discord import app_commands


# We add a salt to prevent from cracking the hashes
salt = os.environ["SALT"]


class Authorization:
    """
    Handle all authorization operations.
    """

    def __init__(self) -> None:
        pass

    def verify(self, id: int) -> bool:
        """
        Verify that the given user is authorized.

        Args:
            id (int): The unique identifier of the user.

        Returns:
            bool: True if authorized, False otherwise.
        """

        hashed_id = hashlib.sha256((str(id) + salt).encode("utf-8"))
        hashed_id = hashed_id.hexdigest()

        try:
            with open("data/auth.json", "r") as f:
                id_list = json.load(f)

        # We use a try here because the formatting can be messed up
        except (json.JSONDecodeError, FileNotFoundError):
            id_list = {"ids": []}

        return hashed_id in id_list["ids"]

    def authorize(self, id: int) -> None:
        """
        Authorize a user.

        Args:
            id (int): The unique identifier of the user.
        """
        hashed_id = hashlib.sha256((str(id) + salt).encode("utf-8"))
        hashed_id = hashed_id.hexdigest()

        try:
            with open("data/auth.json", "r") as f:
                id_list = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            id_list = {"ids": []}

        with open("data/auth.json", "w") as f:
            id_list["ids"].append(hashed_id)
            json.dump(id_list, f, indent=4)


auth_system = Authorization()


class UnauthorizedError(app_commands.CheckFailure):
    """Custom error for when a user isn't authorized."""

    pass


def is_authorized():
    """
    A decorator that checks if the user is authorized before running the command.
    """

    def verify_auth(interaction: discord.Interaction) -> bool:
        if auth_system.verify(interaction.user.id):
            return True
        raise UnauthorizedError("You do not have permission to run this command.")

    return app_commands.check(verify_auth)
