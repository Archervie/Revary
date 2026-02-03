import logging
from .auth_utils import Authorization
from .date_utils import Dates


class Standard:
    """
    A unified toolbox that holds all local utility instances.
    """

    def __init__(self):
        self.auth = Authorization()
        self.date = Dates("EST")
        self.logger = logging.getLogger("Bot_Standard")
