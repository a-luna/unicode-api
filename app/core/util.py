import time
from datetime import date, datetime, timedelta, timezone, tzinfo
from typing import Generator

from dateutil import tz

DATE_ONLY_2 = "%m/%d/%Y"
DT_AWARE = "%m/%d/%Y %I:%M:%S %p %z"
DT_STR_FORMAT_ALL = "%Y-%m-%d %H:%M:%S.%f %Z%z"
DT_NAIVE = "%m/%d/%Y %I:%M:%S %p"

TIME_ZONE_LA = tz.gettz("America/Los_Angeles")
TIME_ZONE_NEW_YORK = tz.gettz("America/New_York")
TIME_SPAN_ONE_DAY = timedelta(days=1)


def get_date_range(start: datetime, end: datetime, inc=TIME_SPAN_ONE_DAY) -> Generator[datetime, None, None]:
    if start > end:
        error = f"Start date ({start.strftime(DATE_ONLY_2)}) must be BEFORE end date ({end.strftime(DATE_ONLY_2)})"
        raise ValueError(error)
    current = start
    while current <= end:
        yield current
        current += inc


def utc_now() -> datetime:
    """Current UTC date and time with the microsecond value normalized to zero."""
    return datetime.now(timezone.utc).replace(microsecond=0)


def localized_dt_string(dt: datetime, use_tz: tzinfo | None = None) -> str:
    """Convert datetime value to a string, localized for the specified timezone."""
    if not dt.tzinfo and not use_tz:
        return dt.strftime(DT_NAIVE)
    if not dt.tzinfo:
        return dt.replace(tzinfo=use_tz).strftime(DT_AWARE)
    return dt.astimezone(use_tz).strftime(DT_AWARE) if use_tz else dt.strftime(DT_AWARE)


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


def today_str() -> str:
    return date.today().strftime(DATE_ONLY_2)


def current_year() -> int:
    return datetime.now().year


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


def get_duration_from_timestamp(ts: float):
    now = dtaware_fromtimestamp(datetime.now().timestamp())
    dt = dtaware_fromtimestamp(ts)
    return format_timedelta_str(dt - now, precise=True)
