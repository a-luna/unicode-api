import time
from datetime import datetime, timedelta, timezone, tzinfo

from app.data.constants import UNICODE_VERSION_RELEASE_DATES

DATE_MONTH_NAME = "%b %d, %Y"


def get_unicode_version_release_date(version: str) -> str:
    if release_date := UNICODE_VERSION_RELEASE_DATES.get(version, None):
        return release_date.strftime(DATE_MONTH_NAME)
    return ""


def make_tzaware(dt: datetime, use_tz: tzinfo | None = None, localize: bool = True) -> datetime:
    """Translate an aware datetime to a different timezone OR add timezone to naive datetime."""
    if not use_tz:
        use_tz = get_local_utcoffset()
    return dt.astimezone(use_tz) if localize else dt.replace(tzinfo=use_tz)


def get_local_utcoffset() -> timezone:
    """Get UTC offset from local system and return as timezone object."""
    utc_offset = timedelta(seconds=time.localtime().tm_gmtoff)
    return timezone(offset=utc_offset)


def dtaware_fromtimestamp(timestamp: float, use_tz: tzinfo | None = None) -> datetime:
    """Time-zone aware datetime object from UNIX timestamp."""
    return make_tzaware(datetime.fromtimestamp(timestamp), use_tz, True)


def format_timedelta_str(td: timedelta, precise: bool = True) -> str:
    """Convert timedelta to an easy-to-read string value."""
    (milliseconds, microseconds) = divmod(td.microseconds, 1000)
    (minutes, seconds) = divmod(td.seconds, 60)
    (hours, minutes) = divmod(minutes, 60)
    if td.days == -1:
        hours += -24
        return f"{hours:.0f}h {minutes:.0f}m {seconds}s" if precise else f"{hours:.0f} hours {minutes:.0f} minutes"
    if td.days != 0:
        (years, days) = divmod(td.days, 365)
        if years > 0:
            return f"{years}y {days}d {hours:.0f}h {minutes:.0f}m {seconds}s" if precise else f"{td.days} days"
        return f"{td.days}d {hours:.0f}h {minutes:.0f}m {seconds}s" if precise else f"{td.days} days"
    if hours > 0:
        return f"{hours:.0f}h {minutes:.0f}m {seconds}s" if precise else f"{hours:.0f} hours {minutes:.0f} minutes"
    if minutes > 0:
        return f"{minutes:.0f}m {seconds}s" if precise else f"{minutes:.0f} minutes"
    if td.seconds > 0:
        return f"{td.seconds}s {milliseconds:.0f}ms" if precise else f"{td.seconds} seconds"
    if milliseconds > 0:
        return f"{milliseconds}ms"
    return f"{microseconds}us"


def get_time_until_timestamp(ts: float, precise: bool = True) -> str:
    return get_duration_between_timestamps(datetime.now().timestamp(), ts, precise)


def get_duration_between_timestamps(ts1: float, ts2: float, precise: bool = True) -> str:
    return format_timedelta_str(dtaware_fromtimestamp(ts2) - dtaware_fromtimestamp(ts1), precise)
