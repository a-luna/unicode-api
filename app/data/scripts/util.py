import subprocess
import sys
from pathlib import Path
from random import randint
from urllib.parse import urlsplit

import requests
from halo import Halo

from app.core.result import Result

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


def run_command(command: str, cwd: Path | None = None, shell: bool = True, text: bool = True) -> Result:
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


def download_file(url: str, dest_folder: Path) -> Result[Path]:
    (dest_file_path, remote_file_size) = get_file_details(url, dest_folder)
    if not remote_file_size:
        return initiate_download(url, dest_file_path)
    download_result = (
        initiate_download(url, dest_file_path)
        if not dest_file_path.exists()
        else resume_download(url, dest_file_path, remote_file_size)
    )
    if download_result.error:
        return download_result
    verify_result = verify_download(dest_file_path, remote_file_size)
    if verify_result.failure:
        return verify_result
    return Result.Ok(dest_file_path)


def get_file_details(url: str, dest_folder: Path) -> tuple[Path, int]:
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest_file_path = dest_folder.joinpath(Path(urlsplit(url).path).name)
    r = requests.head(url)
    remote_file_size = int(r.headers.get("content-length", 0))
    return (dest_file_path, remote_file_size)


def initiate_download(url: str, dest_file_path: Path) -> Result[Path]:
    print(f"{dest_file_path.name!r} does not exist. Downloading...")
    return download_file_in_chunks(url, dest_file_path)


def resume_download(url: str, dest_file_path: Path, remote_file_size: int) -> Result[Path]:
    local_file_size = dest_file_path.stat().st_size
    if local_file_size == remote_file_size:
        print(f"{dest_file_path.name!r} is complete. Skipping...")
        return Result.Ok(dest_file_path)
    print(f"{dest_file_path.name!r} is incomplete. Resuming...")
    return download_file_in_chunks(url, dest_file_path, local_file_size, fopen_mode="ab")


def download_file_in_chunks(
    url: str, dest_file_path: Path, local_file_size: int | None = None, fopen_mode: str = "wb"
) -> Result[Path]:
    resume_header = {"Range": f"bytes={local_file_size}-"} if local_file_size else None
    r = requests.get(url, stream=True, headers=resume_header)
    with open(dest_file_path, fopen_mode) as f:
        for chunk in r.iter_content(32 * CHUNK_SIZE):
            f.write(chunk)
    return Result.Ok(dest_file_path)


def verify_download(dest_file_path: Path, remote_file_size: int) -> Result:
    local_file_size = dest_file_path.stat().st_size
    if local_file_size == remote_file_size:
        return Result.Ok()
    more_or_fewer = "more" if local_file_size > remote_file_size else "fewer"
    error = (
        f"Recieved {more_or_fewer} bytes than expected for {dest_file_path.name!r}!\n"
        f"Expected File Size: {remote_file_size:,} bytes\n"
        f"Received File Size: {local_file_size:,} bytes"
    )
    return Result.Fail(error)
