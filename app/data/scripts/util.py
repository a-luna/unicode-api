import subprocess
import sys
from random import randint

from halo import Halo

import app.db.engine as db
from app.core.result import Result

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


def run_command(command, cwd=None, shell=True, text=True):
    try:
        subprocess.check_call(
            command,
            stdout=sys.stdout,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            shell=shell,
            text=text,
        )
        return Result.Ok()
    except subprocess.CalledProcessError as e:
        error = (
            f"An error occurred while executing the command below:\n"
            f"\tCommand: {e.cmd} (return code = {e.returncode})"
        )
        if e.stderr:
            error += f"\n\tError: {e.stderr}"
        return Result.Fail(error)
