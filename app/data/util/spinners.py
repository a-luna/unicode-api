import subprocess
from random import randint

from halo import Halo

CHUNK_SIZE = 1024


def start_task(message: str, clear_screen: bool = False) -> Halo:
    if clear_screen:
        subprocess.run(["clear"])
    spinner = Halo(color="cyan", spinner=f"dots{randint(2, 9)}")
    spinner.text = message
    spinner.start()
    return spinner


def update_progress(spinner: Halo, message: str, current: int, total: int) -> None:
    percent = current / float(total)
    spinner.text = f"{message} ({current}/{total}) {percent:.0%}..."


def finish_task(spinner: Halo, success: bool, message: str):
    if success:
        spinner.succeed(message)
    else:
        spinner.fail(f"Errror! {message}")
