"""
This module provides utility functions and classes for various purposes, including:

1. **Named Tuple Type Checking**:
    - `INamedTuple`: A protocol for named tuples.
    - `isinstance_of_namedtuple`: Checks if an object is a named tuple.

2. **String Utilities**:
    - `s`: Determines singular or plural form of a word based on input.
    - `slugify`: Converts a string into a URL-friendly slug.

3. **Unicode Version Utilities**:
    - `get_unicode_version_release_date`: Retrieves the release date of a specific Unicode version.

4. **Datetime and Timezone Utilities**:
    - `make_tzaware`: Converts a naive datetime to a timezone-aware datetime.
    - `get_local_utcoffset`: Retrieves the local UTC offset as a timezone object.
    - `dtaware_fromtimestamp`: Converts a UNIX timestamp to a timezone-aware datetime.
    - `format_timedelta_str`: Formats a timedelta object into a human-readable string.
    - `get_time_until_timestamp`: Calculates the time remaining until a given timestamp.
    - `get_duration_between_timestamps`: Calculates the duration between two UNIX timestamps.

5. **Dictionary Reporting**:
    - `get_dict_report`: Generates a formatted report of a dictionary-like object.

These utilities are designed to simplify common operations such as string manipulation,
datetime handling, and dictionary formatting.
"""

import re
import time
from collections.abc import Mapping, Sequence, Sized
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Any, Protocol, TypeGuard, runtime_checkable

from unicode_api.constants import DATE_MONTH_NAME, UNICODE_VERSION_RELEASE_DATES
from unicode_api.custom_types import JSON
from unicode_api.models.util import to_lower_camel


@runtime_checkable
class INamedTuple(Protocol):
    def _asdict(self) -> dict[str, Any]: ...
    def _fields(self) -> tuple[str, ...]: ...


def isinstance_of_namedtuple(obj: Any) -> TypeGuard[INamedTuple]:
    return isinstance(obj, tuple) and isinstance(obj, INamedTuple)


def s(x: Sized | int | float | str, single: str = "", plural: str = "s") -> str:
    """
    Determines whether to return the singular or plural form of a word
    based on the input value.

    Args:
        x (list | int | float | str): The input value used to determine
            singular or plural form. If `x` is a list, its length is used.
            If `x` is a string, it is converted to a float (if possible)
            to determine the form. If `x` is an int or float, its value
            is directly used.
        single (str, optional): The string to return for the singular form.
            Defaults to an empty string.
        plural (str, optional): The string to return for the plural form.
            Defaults to "s".

    Returns:
        str: The singular or plural form based on the input value.
    """
    if isinstance(x, Sized):
        return plural if len(x) > 1 else single
    if isinstance(x, str):
        try:
            return plural if float(x) > 1 else single
        except ValueError:
            return single
    return plural if x > 1 else single


def slugify(text: str, separator: str = "-") -> str:
    """
    Converts a given text into a URL-friendly slug.

    This function transforms the input text into a lowercase, trimmed string
    with words separated by the specified separator. It removes special
    characters, replaces spaces with the separator, and ensures no duplicate
    or trailing separators are present.

    Args:
        text (str): The input string to be slugified.
        separator (str, optional): The character to use as a word separator.
            Defaults to "-".

    Returns:
        str: A slugified version of the input text.
    """
    text = text.lower().strip()
    text = re.sub(r"\s+", separator, text)
    text = re.sub(rf"([^A-Za-z0-9{separator}])+", separator, text)
    text = re.sub(rf"{separator}{separator}+", separator, text)
    text = re.sub(rf"(^{separator}|{separator}$)", "", text)
    return text


def get_unicode_version_release_date(version: str) -> str:
    """
    Retrieve the release date of a specific Unicode version.

    Args:
        version (str): The Unicode version string (e.g., "15.0").

    Returns:
        str: The release date formatted as "Mon DD, YYYY" (e.g., "Sep 13, 2022")
             if the version exists in the UNICODE_VERSION_RELEASE_DATES dictionary,
             otherwise an empty string.
    """
    if release_date := UNICODE_VERSION_RELEASE_DATES.get(version):
        return release_date.strftime(DATE_MONTH_NAME)
    return ""


def make_tzaware(dt: datetime, use_tz: tzinfo | None = None, localize: bool = True) -> datetime:
    """
    Convert a datetime object to a timezone-aware datetime.

    This function either translates an already timezone-aware datetime object
    to a different timezone or adds a timezone to a naive datetime object.

    Args:
        dt (datetime): The datetime object to be converted. It can be either
            naive or timezone-aware.
        use_tz (tzinfo | None, optional): The target timezone to apply. If not
            provided, the local UTC offset will be used. Defaults to None.
        localize (bool, optional): If True, the function will convert the
            datetime to the specified timezone. If False, it will only set the
            timezone without converting the time. Defaults to True.

    Returns:
        datetime: A timezone-aware datetime object.
    """
    if not use_tz:
        use_tz = get_local_utcoffset()
    return dt.astimezone(use_tz) if localize else dt.replace(tzinfo=use_tz)


def get_local_utcoffset() -> timezone:
    """
    Get the local UTC offset as a timezone object.

    This function retrieves the UTC offset of the local system by accessing
    the `tm_gmtoff` attribute of the `time.localtime()` result, which represents
    the offset in seconds from UTC. It then converts this offset into a
    `datetime.timedelta` object and returns it wrapped in a `datetime.timezone` object.

    Returns:
        timezone: A `datetime.timezone` object representing the local UTC offset.
    """
    utc_offset = timedelta(seconds=time.localtime().tm_gmtoff)
    return timezone(offset=utc_offset)


def dtaware_fromtimestamp(timestamp: float, use_tz: tzinfo | None = None) -> datetime:
    """
    Convert a UNIX timestamp to a timezone-aware datetime object.

    Args:
        timestamp (float): The UNIX timestamp to convert.
        use_tz (tzinfo | None, optional): The timezone to use for the conversion.
            If None, the system's local timezone will be used. Defaults to None.

    Returns:
        datetime: A timezone-aware datetime object representing the given timestamp.
    """
    return make_tzaware(datetime.fromtimestamp(timestamp), use_tz, True)


def format_timedelta_str(td: timedelta, precise: bool = True) -> str:
    """
    Format a timedelta object into a human-readable string.

    Args:
        td (timedelta): The timedelta object to format.
        precise (bool, optional): If True, includes more precise units (e.g., milliseconds, microseconds).
                                  If False, uses a less detailed format. Defaults to True.

    Returns:
        str: A formatted string representation of the timedelta.

    Examples:
        >>> from datetime import timedelta
        >>> format_timedelta_str(timedelta(days=1, hours=2, minutes=30))
        '1d 2h 30m 0s'
        >>> format_timedelta_str(timedelta(days=1, hours=2, minutes=30), precise=False)
        '1 days 2 hours'
        >>> format_timedelta_str(timedelta(seconds=45, microseconds=123456))
        '45s 123ms'
        >>> format_timedelta_str(timedelta(seconds=-45, microseconds=123456))
        '-45s 123ms'
    """
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
    """
    Calculate the time remaining until a given timestamp.

    Args:
        ts (float): The target timestamp as a Unix timestamp (seconds since epoch).

    Returns:
        timedelta: A timedelta object representing the duration between the current time
                   and the specified timestamp.
    """
    return get_duration_between_timestamps(datetime.now().timestamp(), ts)


def get_duration_between_timestamps(ts_start: float, ts_end: float) -> timedelta:
    """
    Calculate the duration between two UNIX timestamps.

    Args:
        ts_start (float): The starting timestamp in seconds since the UNIX epoch.
        ts_end (float): The ending timestamp in seconds since the UNIX epoch.

    Returns:
        timedelta: The duration between the two timestamps as a timedelta object.
    """
    return dtaware_fromtimestamp(ts_end) - dtaware_fromtimestamp(ts_start)


def get_dict_report(
    data: Mapping[str, Any], title: str | None = None, indent: int | None = None, show_types: bool = False
) -> list[str]:
    """
    Generates a formatted report of a dictionary-like object as a list of strings.

    Args:
        data (Mapping[str, Any]): The dictionary-like object to generate the report for.
        title (str | None, optional): An optional title for the report. Defaults to None.
        indent (int | None, optional): The number of spaces to indent the report. Defaults to None.
        show_types (bool, optional): Whether to include the data type of each value in the report. Defaults to False.

    Returns:
        list[str]: A list of strings representing the formatted report.

    Notes:
        - Keys and values in the mapping are formatted with dots to align the output.
        - Nested structures such as lists, sets, tuples, named tuples, and dictionaries are recursively processed.
        - Lists, sets and tuples are converted to dictionaries with their indices as keys for uniform formatting.
        - Named tuples are converted to dictionaries using their `_asdict()` method.
    """

    def dots(key: str, max_len: int) -> str:
        return "." * ((max_len - len(key)) + 2)

    report: list[str] = []
    indent = indent or 0
    if title:
        report.append(f"{' ' * indent}{'#' * 5} {title} {'#' * 5}")
    if not data:
        report.append(f"{' ' * indent}No data to report")
        return report
    data_formatted = _get_dict_with_formatted_key_names(data, show_types)
    max_key_len = max(len(key) for key in data_formatted)
    for key, value in data_formatted.items():
        item_name = f"{' ' * indent}{key}{dots(str(key), max_key_len)}:"
        value: Sequence[Any] | INamedTuple | dict[str, Any] | set[Any] | str | int | float | None
        match value:
            case str():
                report.append(f'{item_name} "{value}"')
            case Sequence() | set() | INamedTuple() | dict():
                item_elements, open_char, close_char = _extract_mapping_elements_and_delimiters(value)
                report.append(f"{item_name} {open_char}")
                report.extend(get_dict_report(item_elements, indent=(len(item_name) + 4), show_types=show_types))
                report.append(f"{' ' * len(item_name)} {close_char}")
            case _:
                report.append(f"{item_name} {value}")
    return report


def _get_dict_with_formatted_key_names(data: Mapping[str, Any], show_types: bool) -> dict[str, Any]:
    return (
        {f"{key} ({value.__class__.__name__})": value for key, value in data.items()}
        if show_types
        else {str(key): value for key, value in data.items()}
    )


def _extract_mapping_elements_and_delimiters(
    data: Sequence[Any] | INamedTuple | dict[str, Any] | set[Any],
) -> tuple[dict[str, Any], str, str]:
    if isinstance(data, INamedTuple):
        return (data._asdict(), "(", ")")  # type: ignore[reportPrivateUsage]
    if isinstance(data, dict):
        return (data, "{", "}")
    if isinstance(data, set):
        return ({str(i): x for i, x in enumerate(data)}, "{", "}")
    if isinstance(data, tuple):
        return ({str(i): x for i, x in enumerate(data)}, "(", ")")
    return ({str(i): x for i, x in enumerate(data)}, "[", "]")


def convert_keys_to_camel_case(response: dict[str, JSON]) -> dict[str, JSON]:
    """
    Recursively formats the property names of a response dictionary to lower camel case.

    Args:
        response (dict[str, Any]): The input dictionary whose property names are to be formatted.

    Returns:
        dict[str, Any]: A new dictionary with all property names converted to lower camel case.
            Nested dictionaries and lists of dictionaries are processed recursively.

    Note:
        Assumes the existence of a `to_lower_camel` function that converts a string to lower camel case.
    """
    converted: dict[str, JSON] = {}
    for name, value in response.items():
        name_camel = to_lower_camel(name)
        if isinstance(value, dict):
            converted[name_camel] = convert_keys_to_camel_case(value)
        if isinstance(value, list):
            formatted_list: list[Any] = []
            for item in value:
                if isinstance(item, dict):
                    formatted_list.append(convert_keys_to_camel_case(item))
                else:
                    formatted_list.append(item)
            converted[name_camel] = formatted_list
        else:
            converted[name_camel] = value
    return converted
