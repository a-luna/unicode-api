import re
import time
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Any

from app.constants import DATE_MONTH_NAME, UNICODE_VERSION_RELEASE_DATES


def s(x: list | int | float | str, single: str = "", plural: str = "s") -> str:
    if isinstance(x, list):
        return plural if len(x) > 1 else single
    if isinstance(x, str):
        try:
            return plural if float(x) > 1 else single
        except ValueError:
            return single
    return plural if x > 1 else single


def slugify(text: str, separator: str = "-") -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", separator, text)
    text = re.sub(rf"([^A-Za-z0-9{separator}])+", separator, text)
    text = re.sub(rf"{separator}{separator}+", separator, text)
    text = re.sub(rf"(^{separator}|{separator}$)", "", text)
    return text


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
    duration = ""
    if td.days < 0:
        td = -td
        duration = "-"
    (ms, us) = divmod(td.microseconds, 1000)
    (minutes, seconds) = divmod(td.seconds, 60)
    (hours, minutes) = divmod(minutes, 60)
    (years, days) = divmod(td.days, 365)
    if years > 0:
        duration += f"{years}y {days}d {hours:.0f}h {minutes:.0f}m {seconds}s" if precise else f"{years}y {days} days"
    elif days > 0:
        duration += f"{days}d {hours:.0f}h {minutes:.0f}m {seconds}s" if precise else f"{days} days {hours:.0f} hours"
    elif hours > 0:
        duration += f"{hours:.0f}h {minutes:.0f}m {seconds}s" if precise else f"{hours:.0f} hours {minutes:.0f} minutes"
    elif minutes > 0:
        duration += f"{minutes:.0f}m {seconds}s {ms:.0f}ms" if precise else f"{minutes:.0f} minutes {seconds} seconds"
    elif seconds > 0:
        duration += f"{seconds}s {ms:.0f}ms" if precise else f"{seconds} seconds"
    elif ms > 0:
        duration += f"{ms}ms {us}us" if precise else f"{ms}ms"
    else:
        duration += f"{us}us"
    return duration


def get_time_until_timestamp(ts: float) -> timedelta:
    return get_duration_between_timestamps(datetime.now().timestamp(), ts)


def get_duration_between_timestamps(ts1: float, ts2: float) -> timedelta:
    return dtaware_fromtimestamp(ts2) - dtaware_fromtimestamp(ts1)


def get_dict_report(data: Mapping[str, Any], title: str | None = None, indent: int | None = None) -> list[str]:
    def dots(key: str, max_len: int) -> str:
        return "." * ((max_len - len(key)) + 2)

    report: list[str] = []
    indent = indent or 0
    max_key_len = max(len(str(key)) for key in data)
    if title:
        report.append(f"{' ' * indent}{'#' * 5} {title} {'#' * 5}")
    for key, value in data.items():
        item_name = f"{' ' * indent}{key}{dots(str(key), max_key_len)}:"
        if isinstance(value, list | dict):
            list_or_dict = value if isinstance(value, dict) else {str(i): x for i, x in enumerate(value)}
            open_char, close_char = ("{", "}") if isinstance(value, dict) else ("[", "]")
            report.append(f"{item_name} {open_char}")
            report.extend(get_dict_report(list_or_dict, indent=(len(item_name) + 4)))
            report.append(f"{' ' * len(item_name)} {close_char}")
        else:
            report.append(f"{item_name} {value}")
    return report
