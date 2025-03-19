from typing import overload


class Result[T]:
    """Represent the outcome of an operation."""

    def __init__(self, success: bool, value: T | None, error: str = "") -> None:
        self.success = success
        self.error = error
        self.value = value

    def __str__(self) -> str:
        """Informal string representation of a result."""
        result = "Success" if self.success else "Fail"
        detail = f"error={self.error}" if self.failure else f"value={self.value}" if self.value is not None else ""
        return f"{result}, {detail}"

    def __repr__(self) -> str:
        """Official string representation of a result."""
        detail = (
            f"value=None, error={self.error!r}"
            if self.failure
            else f"value={self.value!r}, error=None"
            if self.value is not None
            else "value=None, error=None"
        )
        return f"Result(success={self.success}, {detail})"

    @property
    def failure(self) -> bool:
        """Flag that indicates if the operation failed."""
        return not self.success

    @staticmethod
    def Fail(error_message: str) -> "Result":  # noqa: N802
        """Create a Result object for a failed operation."""
        return Result(False, value=None, error=error_message)

    @overload
    @staticmethod
    def Ok() -> "Result[None]": ...

    @overload
    @staticmethod
    def Ok(value: None) -> "Result[None]": ...

    @overload
    @staticmethod
    def Ok(value: T) -> "Result[T]": ...

    @staticmethod
    def Ok(value: T | None = None) -> "Result[None] | Result[T]":  # noqa: N802
        """Create a Result object for a successful operation."""
        return Result(True, value=value)
