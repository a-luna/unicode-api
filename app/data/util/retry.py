"""decorators.log_call"""
from datetime import timedelta
from functools import wraps
from time import sleep
from typing import Callable, ParamSpec, Type, TypeVar

DT_NAIVE = "%m/%d/%Y %I:%M:%S %p"
T = TypeVar("T")
P = ParamSpec("P")


class RetryLimitExceededError(Exception):
    """Custom error raised by retry decorator when max_attempts have failed."""

    def __init__(self, func: Callable, max_attempts: int):
        error = f"Retry limit exceeded! (function: {func.__name__}, max attempts: {max_attempts})"
        super().__init__(error)


def retry(
    *,
    max_attempts: int = 2,
    delay: int = 1,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
    on_failure: Callable[[Callable, int, Exception, int], None] | None = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Retry the wrapped function when an exception is raised until max_attempts have failed."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:  # type: ignore
            for remaining in reversed(range(max_attempts)):
                try:
                    return func(*args, **kwargs)
                except exceptions as ex:
                    if remaining <= 0:
                        raise RetryLimitExceededError(func, max_attempts) from ex
                    if on_failure:
                        on_failure(func, remaining, ex, delay)
                    sleep(delay)

        return wrapper

    return decorator


def format_timedelta_str(td: timedelta, precise: bool = True) -> str:
    """Convert timedelta to an easy-to-read string value."""
    (milliseconds, microseconds) = divmod(td.microseconds, 1000)
    (minutes, seconds) = divmod(td.seconds, 60)
    (hours, minutes) = divmod(minutes, 60)
    if td.days == -1:
        hours += -24
        return f"{hours:.0f}h {minutes:.0f}m {seconds}s" if precise else f"{hours:.0f} hours {minutes:.0f} minutes"
    if td.days != 0:
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
