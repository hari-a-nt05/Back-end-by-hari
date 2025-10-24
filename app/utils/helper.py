from datetime import datetime

import pytz


def get_current_time(tz: str = "UTC") -> datetime:
    """
    Returns the current time in the specified timezone.

    Args:
        tz (str): Timezone string (e.g., 'UTC', 'Asia/Kolkata', 'Europe/London').

    Returns:
        datetime: Timezone-aware current datetime.
    """
    timezone = pytz.timezone(tz)
    return datetime.now(timezone)
