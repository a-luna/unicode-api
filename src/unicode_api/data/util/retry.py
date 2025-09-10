from collections.abc import Callable
from functools import wraps
from time import sleep
from typing import Any


class RetryLimitExceededError(Exception):
    """
    Exception raised when the retry decorator exceeds the maximum number of allowed attempts.

    Attributes:
        func (Callable): The function that was retried.
        max_attempts (int): The maximum number of retry attempts allowed.

    Args:
        func (Callable): The function that failed after maximum retries.
        max_attempts (int): The maximum number of retry attempts.

    Example:
        raise RetryLimitExceededError(my_function, 5)
    """

    def __init__(self, func: Callable[..., Any], max_attempts: int):
        error = f"Retry limit exceeded! (function: {func.__name__}, max attempts: {max_attempts})"
        super().__init__(error)


def retry[T, **P](
    *,
    max_attempts: int = 2,
    delay: int = 1,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    on_failure: Callable[[Callable[P, T], int, Exception, int], None] | None = None,
) -> Callable[[Callable[P, T]], Callable[P, T | None]] | None:
    """
    A decorator that retries the wrapped function when specified exceptions are raised, up to a maximum number
    of attempts.

    Parameters:
        max_attempts (int): The maximum number of attempts to call the function. Defaults to 2.
        delay (int): The number of seconds to wait between attempts. Defaults to 1.
        exceptions (tuple[type[Exception], ...]): A tuple of exception types that trigger a retry.
            Defaults to (Exception,).
        on_failure (Callable[[Callable, int, Exception, int], None] | None): Optional callback invoked after a failure,
            receiving the function, remaining attempts, exception, and delay.

    Returns:
        Callable: A decorator that wraps the target function, retrying it on failure up to the specified number of
            attempts. Returns None if all attempts fail.

    Raises:
        RetryLimitExceededError: If the function fails after the maximum number of attempts.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T | None]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | None:
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
