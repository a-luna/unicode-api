import subprocess
from random import randint

from halo import Halo

import app.core.db as db

# NULL OBJECTS
NULL_PLANE = db.UnicodePlane(
    number=-1,
    name="Invalid Codepoint",
    abbreviation="N/A",
    start="",
    start_dec=0,
    finish="",
    finish_dec=0,
    start_block_id=0,
    finish_block_id=0,
    total_allocated=0,
    total_defined=0,
)

NULL_BLOCK = db.UnicodeBlock(
    id=0,
    name="",
    plane_id=0,
    start="",
    start_dec=0,
    finish="",
    finish_dec=0,
    total_allocated=0,
    total_defined=0,
)


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
