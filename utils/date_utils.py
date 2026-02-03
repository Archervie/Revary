"""
Used for any datetime conversions
"""

from datetime import datetime
from pytz import timezone, utc


class Dates:
    """
    Handle all date & timezone operations.

    Args:
        timezone (str): The target timezone.
    """

    def __init__(self, timezone: str) -> None:
        self.timezone = timezone

    def date(self) -> datetime:
        """
        Return the current time for the target timezone.

        Returns:
            datetime: Current time as a datetime object.
        """
        tz = timezone(self.timezone)
        return datetime.now(tz)

    def utc_conv(self, utc_time: datetime) -> datetime:
        """
        Convert the time from UTC to the target timezone.
        Args:
            utc_time (datetime): Current UTC time as a datetime object.

        Returns:
            datetime: The converted datetime object.
        """
        tz = timezone(self.timezone)
        given_time = utc_time.astimezone(tzinfo=utc).astimezone(tz)
        return tz.normalize(given_time)
