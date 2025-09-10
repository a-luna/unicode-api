import subprocess
import time
from datetime import timedelta
from random import randint

from halo import Halo

from unicode_api.core.util import format_timedelta_str

CHUNK_SIZE = 1024
ONE_PERCENT = 0.01


class Spinner:
    """
    A utility class for displaying a progress spinner with status updates in the terminal.

    Attributes:
        spinner (Halo): The spinner instance used for displaying progress.
        total (int): The total number of steps for completion.
        current (int): The current progress count.
        last_reported (float): The last reported percentage of completion.
        message (str): The message displayed alongside the spinner.
        start_time (float): The time when the spinner started.
        end_time (float): The time when the spinner finished.

    Properties:
        percent_complete (float): The percentage of completion (0.0 to 1.0).
        elapsed_time (timedelta): The elapsed time since the spinner started.

    Methods:
        start(message: str, total: int = 0, clear_screen: bool = False) -> None:
            Starts the spinner with an optional message, total steps, and screen clearing.

        increment(amount: int = 1) -> None:
            Increments the current progress by the specified amount and updates the spinner
            text if progress has advanced.

        stop_and_persist() -> None:
            Stops the spinner and persists its current state.

        successful(message: str) -> None:
            Marks the spinner as successful with a final message.

        failed(message: str) -> None:
            Marks the spinner as failed with a final message.

        finish(success: bool, message: str):
            Finishes the spinner, marking it as successful or failed, and displays the final
            message with elapsed time.
    """

    spinner: Halo
    total: int
    current: int
    last_reported: float
    message: str
    start_time: float
    end_time: float

    def __init__(self) -> None:
        self.spinner = Halo(color="cyan", spinner=f"dots{randint(2, 9)}")
        self.total = 0
        self.current = 0
        self.last_reported = 0.0
        self.message = ""
        self.start_time = 0.0
        self.end_time = 0.0

    @property
    def percent_complete(self) -> float:
        if self.total == 0:
            return 0.0
        return self.current / float(self.total)

    @property
    def elapsed_time(self) -> timedelta:
        end = time.perf_counter() if self.end_time == 0.0 else self.end_time
        return timedelta(seconds=(end - self.start_time))

    def start(self, message: str, total: int = 0, clear_screen: bool = False) -> None:
        if clear_screen:
            subprocess.run(["clear"])  # noqa: PLW1510
        self.total = total
        self.current = 0
        self.message = message
        self.spinner.text = self._get_current_message()
        self.start_time = time.perf_counter()
        self.spinner.start()

    def increment(self, amount: int = 1) -> None:
        self.current += amount
        if self.percent_complete - self.last_reported > ONE_PERCENT:
            self.spinner.text = self._get_current_message()
            self.last_reported = self.percent_complete

    def _get_current_message(self) -> str:
        progress = f"{self.current}/{self.total} {self.percent_complete:.0%}"
        elapsed = f"elapsed: {format_timedelta_str(self.elapsed_time)}"
        return f"{self.message} ({progress}) ({elapsed})"

    def stop_and_persist(self) -> None:
        self.spinner.stop_and_persist()

    def successful(self, message: str) -> None:
        self.finish(True, message)

    def failed(self, message: str) -> None:
        self.finish(False, message)

    def finish(self, success: bool, message: str):
        self.end_time = time.perf_counter()
        message = f"{message} (elapsed: {format_timedelta_str(self.elapsed_time)})"
        if success:
            self.spinner.succeed(message)
        else:
            self.spinner.fail(message)
        self.spinner.clear()
