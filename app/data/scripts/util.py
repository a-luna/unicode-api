import re
import subprocess
import sys
from pathlib import Path
from random import randint
from urllib.parse import urlsplit

import requests
from halo import Halo

import app.db.engine as db
from app.core.result import Result

CHUNK_SIZE = 1024


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


def download_file(url: str, local_folder: Path):
    local_folder.mkdir(parents=True, exist_ok=True)
    file_name = Path(urlsplit(url).path).name
    local_file_path = local_folder.joinpath(file_name)
    r = requests.head(url)
    remote_file_size = int(r.headers.get("content-length", 0))
    if not remote_file_size:
        return Result.Fail(f'Request for "{file_name}" did not return a response containing the file size.')
    local_file_size = 0
    resume_header = None
    fopen_mode = "wb"
    if not local_file_path.exists():
        print(f'"{file_name}" does not exist. Downloading...')
    else:
        local_file_size = local_file_path.stat().st_size
        if local_file_size == remote_file_size:
            print(f'"{file_name}" is complete. Skipping...')
            return Result.Ok(local_file_path)
        print(f'"{file_name}" is incomplete. Resuming...')
        resume_header = {"Range": f"bytes={local_file_size}-"}
        fopen_mode = "ab"

    r = requests.get(url, stream=True, headers=resume_header)
    with open(local_file_path, fopen_mode) as f:
        for chunk in r.iter_content(32 * CHUNK_SIZE):
            f.write(chunk)

    local_file_size = local_file_path.stat().st_size
    if local_file_size == remote_file_size:
        return Result.Ok(local_file_path)
    more_or_fewer = "more" if local_file_size > remote_file_size else "fewer"
    error = (
        f'Recieved {more_or_fewer} bytes than expected for "{file_name}"!\n'
        f"Expected File Size: {remote_file_size:,} bytes\n"
        f"Received File Size: {local_file_size:,} bytes"
    )
    return Result.Fail(error)
