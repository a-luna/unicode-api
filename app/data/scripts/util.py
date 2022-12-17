import subprocess
from random import randint

from halo import Halo


def start_task(message, clear_screen=False):
    if clear_screen:
        subprocess.run(["clear"])
    spinner = Halo(color="cyan", spinner=f"dots{randint(2, 9)}")
    spinner.text = message
    spinner.start()
    return spinner


def update_progress(spinner, message, current, total):
    percent = current / float(total)
    spinner.text = f"{message} ({current}/{total}) {percent:.0%}..."


def finish_task(spinner, success, message):
    if success:
        spinner.succeed(message)
    else:
        spinner.fail(f"Errror! {message}")
