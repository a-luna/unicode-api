from collections.abc import Callable
from functools import wraps
from time import sleep
from typing import ParamSpec, TypeVar

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
    exceptions: tuple[type[Exception], ...] = (Exception,),
    on_failure: Callable[[Callable, int, Exception, int], None] | None = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Retry the wrapped function when an exception is raised until max_attempts have failed."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)  # type: ignore  # noqa: PGH003
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:  # type: ignore  # noqa: PGH003
            for remaining in reversed(range(max_attempts)):
                try:
                    return func(*args, **kwargs)
                except exceptions as ex:  # noqa: PERF203
                    if remaining <= 0:
                        raise RetryLimitExceededError(func, max_attempts) from ex
                    if on_failure:
                        on_failure(func, remaining, ex, delay)
                    sleep(delay)

        return wrapper

    return decorator
