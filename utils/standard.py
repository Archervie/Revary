import logging
from .auth_utils import Authorization
from .date_utils import Dates


class Standard:
    """
    A unified toolbox that holds all local utility instances.
    """

    def __init__(self, name):
        self.auth = Authorization()
        self.dates = Dates("EST")
        self.logger = logging.getLogger(name)
