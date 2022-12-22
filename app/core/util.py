import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

import requests

from app.core.db import NO_NAME_BLOCKS
from app.core.enums.block_name import UnicodeBlockName
from app.core.result import Result
from app.data.cache import cached_data

CHUNK_SIZE = 1024


def get_codepoint_string(codepoint: int) -> str:
    return f"U+{codepoint:04X}"


def download_file(url: str, local_folder: Path):
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


def codepoint_is_assigned(codepoint: int) -> bool:
    return codepoint in cached_data.char_name_map or get_unicode_block_containing_character(codepoint) in NO_NAME_BLOCKS


def get_unicode_block_containing_character(codepoint: int) -> UnicodeBlockName:
    found = [
        block["id"]
        for block in cached_data.blocks
        if int(block["start_dec"]) <= codepoint and codepoint <= int(block["finish_dec"])
    ]
    return UnicodeBlockName.from_block_id(found[0]) if found else UnicodeBlockName.NONE
