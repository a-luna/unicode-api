from collections.abc import Callable
from typing import Self, overload


class Result[T]:
    """Represent the outcome of an operation."""

    def __init__(self, success: bool, value: T | None, error: str | None) -> None:
        self.success = success
        self.error = error
        self.value = value

    def __str__(self) -> str:
        """Informal string representation of a result."""
        result = "Success" if self.success else "Fail"
        detail = f" {self.error}" if self.failure else f" value={self.value}" if self.value else ""
        return f"[{result}]{detail}"

    def __repr__(self) -> str:
        """Official string representation of a result."""
        detail = (
            f"value=None, error={self.error!r}"
            if self.failure
            else f"value={self.value!r}, error=None"
            if self.value
            else "value=None, error=None"
        )
        return f"Result({"True" if self.success else "False"}, {detail})"

    @property
    def failure(self) -> bool:
        """Flag that indicates if the operation failed."""
        return not self.success

    def on_success(self, func: Callable, *args, **kwargs) -> Self:
        """Pass result of successful operation (if any) to subsequent function."""
        return self if self.failure else func(self.value, *args, **kwargs) if self.value else func(*args, **kwargs)

    def on_failure(self, func: Callable, *args, **kwargs) -> Self:
        """Pass error message from failed operation to subsequent function."""
        return self if self.success else func(self.error, *args, **kwargs)

    def on_both(self, func: Callable, *args, **kwargs) -> Self:
        """Pass result (either succeeded/failed) to subsequent function."""
        return func(self, *args, **kwargs)

    @staticmethod
    def Fail(error_message: str) -> Self:  # noqa: N802
        """Create a Result object for a failed operation."""
        return Result(False, value=None, error=error_message)

    @overload
    @staticmethod
    def Ok() -> "Result": ...

    @overload
    @staticmethod
    def Ok(value: T) -> "Result[T]": ...

    @staticmethod
    def Ok(value: T | None = None) -> "Result | Result[T]":  # noqa: N802
        """Create a Result object for a successful operation."""
        return Result(True, value=value, error=None)
