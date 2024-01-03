import subprocess
from random import randint

from halo import Halo

CHUNK_SIZE = 1024
ONE_PERCENT = 0.01


class Spinner:
    def __init__(self) -> None:
        self.spinner = Halo(color="cyan", spinner=f"dots{randint(2, 9)}")
        self.total = 0
        self.current = 0
        self.last_reported = 0.0
        self.message = ""

    @property
    def percent_complete(self) -> float:
        return self.current / float(self.total)

    def start(self, message: str, total: int = 0, clear_screen: bool = False) -> None:
        if clear_screen:
            subprocess.run(["clear"])  # noqa: PLW1510
        self.total = total
        self.current = 0
        self.message = message
        self.spinner.text = message
        self.spinner.start()

    def increment(self, amount: int = 1) -> None:
        self.current += amount
        if self.percent_complete - self.last_reported > ONE_PERCENT:
            self.spinner.text = f"{self.message} ({self.current}/{self.total}) {self.percent_complete:.0%}..."
            self.last_reported = self.percent_complete

    def stop_and_persist(self) -> None:
        self.spinner.stop_and_persist()

    def successful(self, message: str) -> None:
        self.finish(True, message)

    def failed(self, message: str) -> None:
        self.finish(False, message)

    def finish(self, success: bool, message: str):
        if success:
            self.spinner.succeed(message)
        else:
            self.spinner.fail("{message}")
        self.spinner = None
