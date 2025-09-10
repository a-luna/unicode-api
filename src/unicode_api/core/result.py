from collections.abc import Callable
from typing import Any


class Result[T]:
    """
    A generic Result type for handling success and failure states in a functional programming style.

    This class provides a way to encapsulate the result of an operation that may succeed or fail,
    eliminating the need for exception handling in many cases and enabling method chaining.

    Type Parameters:
        T: The type of the value contained in a successful result.

    Attributes:
        success (bool): True if the operation succeeded, False otherwise.
        value (T | None): The value of a successful operation, None if failed.
        error (str | None): Error message if the operation failed, None if successful.

    Properties:
        failure (bool): True if the operation failed (opposite of success).

    Methods:
        on_success: Chains another operation if this result is successful.
        on_failure: Chains another operation if this result failed.
        on_both: Chains an operation regardless of success or failure state.

    Class Methods:
        Ok: Creates a successful Result with an optional value.
        Fail: Creates a failed Result with an error message.

    Example:
        >>> result = Result.Ok("Hello")
        >>> print(result)  # [Success] value=Hello

        >>> failed = Result.Fail("Something went wrong")
        >>> print(failed)  # [Fail] error=Something went wrong

        >>> # Method chaining
        >>> result.on_success(lambda x: Result.Ok(x.upper()))
    """

    def __init__(self, success: bool, value: T | None = None, error: str | None = None) -> None:
        """Initialize a Result object.

        Args:
            success (bool): Whether the operation was successful.
            value (T | None, optional): The value returned by the operation if successful. Defaults to None.
            error (str | None, optional): The error message if the operation failed. Defaults to None.
        """
        self.success = success
        self.value = value
        self.error = error or ""

    def __str__(self) -> str:
        """Return a string representation of the Result object.

        Returns:
            str: A formatted string showing the result status (Success/Fail) and either
                 the error message if it's a failure, or the value if it's a success.
                 Format: "[Success/Fail] error=<error_msg>" or "[Success/Fail] value=<value>"
        """
        result = "Success" if self.success else "Fail"
        detail = f" error={self.error}" if self.failure else f" value={self.value}" if self.value else " value=None"
        return f"[{result}]{detail}"

    def __repr__(self) -> str:
        """Return a string representation of the Result object.

        Returns:
            str: A formatted string showing the success status and either the error
                 (if failure) or the value (if success). Format is:
                 "Result(True/False, error=<error_repr>)" for failures or
                 "Result(True/False, value=<value_repr>)" for successes.
        """
        detail = f"error={self.error!r}" if self.failure else f"value={self.value!r}" if self.value else "value=None"
        return f"Result({'True' if self.success else 'False'}, {detail})"

    @property
    def failure(self) -> bool:
        """Check if the result represents a failure.

        Returns:
            bool: True if the operation failed, False if it succeeded.
        """
        return not self.success

    def on_success(
        self, func: Callable[..., "Result[T]"], *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> "Result[T]":
        """
        Execute a function on the successful result value, enabling method chaining.

        This method implements a monadic bind operation for the Result type. If the current
        Result is a failure, it returns itself unchanged. If the current Result is successful,
        it executes the provided function with the Result's value (if not None) plus any
        additional arguments and keyword arguments.

        Args:
            func: A callable that takes the success value as its first argument (if value is not None)
                and returns a Result[T]. The function should handle the case where no value
                is passed if the current Result's value is None.

            *args: Additional positional arguments to pass to the function.

            **kwargs: Additional keyword arguments to pass to the function.

        Returns:
            Result[T]: If the current Result is a failure, returns self unchanged.
                If the current Result is successful, returns the Result returned by func.
                If func raises an exception, returns a failed Result with an error message.

        Example:
            >>> result = Result.Ok(5)
            >>> result.on_success(lambda x: Result.Ok(x * 2))
            Result.Ok(10)
            >>> failed_result = Result.Fail("error")
            >>> failed_result.on_success(lambda x: Result.Ok(x * 2))
            Result.Fail("error")
        """

        if self.failure:
            return self
        try:
            return func(self.value, *args, **kwargs) if self.value is not None else func(*args, **kwargs)
        except Exception as e:
            return Result[T].Fail(f"Error in chained operation: {str(e)}")

    def on_failure(
        self, func: Callable[..., "Result[T]"], *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> "Result[T]":
        """
        Execute a function on the failure result value, enabling method chaining.

        This method allows for chaining operations that should only execute when the current
        Result represents a failure. If the current Result is successful, it returns itself
        unchanged. If the current Result is a failure, it executes the provided function
        with the error value as the first argument, followed by any additional args and kwargs.

        Args:
            func: A callable that takes the error value as its first parameter and returns
                a Result[T]. This function will only be called if the current Result
                represents a failure.

            *args: Additional positional arguments to pass to the function.

            **kwargs: Additional keyword arguments to pass to the function.

        Returns:
            Result[T]: If the current Result is successful, returns self unchanged.
                If the current Result is a failure, returns the Result from executing
                the provided function. If an exception occurs during function execution,
                returns a new failure Result with the exception message.

        Example:
            >>> result = Result.Fail("initial error")
            >>> result.on_failure(lambda err: Result.Ok("recovered"))
            Result.Ok("recovered")
            >>> result = Result.Ok("success")
            >>> result.on_failure(lambda err: Result.Ok("recovered"))
            Result.Ok("success")
        """

        if self.success:
            return self
        try:
            return func(self.error, *args, **kwargs)
        except Exception as e:
            return Result[T].Fail(f"Error in chained operation: {str(e)}")

    def on_both(
        self, func: Callable[..., "Result[T]"], *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> "Result[T]":
        """
        Apply a function to this Result instance regardless of whether it's Success or Failure.

        This method calls the provided function with this Result instance as the first argument,
        followed by any additional positional and keyword arguments. The function should accept
        a Result as its first parameter and return a new Result.

        Args:
            func: A callable that takes a Result instance as its first argument and returns a Result[T]
            *args: Additional positional arguments to pass to the function
            **kwargs: Additional keyword arguments to pass to the function

        Returns:
            Result[T]: The result returned by the provided function

        Example:
            >>> def log_result(result: Result[int]) -> Result[int]:
            ...     print(f"Processing result: {result}")
            ...     return result
            >>> success_result = Success(42)
            >>> success_result.on_both(log_result)
            Success(42)
        """

        return func(self, *args, **kwargs)

    @classmethod
    def Fail(cls, error_message: str) -> "Result[T]":  # noqa: N802
        """
        Create a Result instance representing a failed operation.

        This is a factory method that creates a Result instance representing a failed operation.

        Args:
            error_message (str): The error message describing why the operation failed.

        Returns:
            Result[T]: A Result instance with success=False and the provided error message.
        """
        return cls(False, error=error_message)

    @classmethod
    def Ok(cls, value: T | None = None) -> "Result[T]":  # noqa: N802
        """
        Create a successful Result instance.

        This is a factory method that creates a Result instance representing a successful operation.

        Args:
            value (T | None, optional): The value to be wrapped in the successful Result.
                Defaults to None.

        Returns:
            Result[T]: A new Result instance indicating success, containing the provided value.
        """
        return cls(True, value=value)
