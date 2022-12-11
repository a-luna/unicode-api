import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

import requests

from app.core.result import Result
from app.schemas import UnicodeBlockResult, UnicodeCharacterResult

CHUNK_SIZE = 1024


def get_codepoint_string(codepoint: int) -> str:
    return f"U+{codepoint:04X}"


def download_file(url: str, local_folder: Path):
    file_name = Path(urlsplit(url).path).name
    local_file_path = local_folder.joinpath(file_name)
    r = requests.head(url)
    remote_file_size = int(r.headers.get("content-length", 0))
    if not remote_file_size:
        return Result.Fail(
            f'Request for "{file_name}" did not return a response containing the file size.'
        )
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


def paginate_search_results(
    results: list[UnicodeCharacterResult | UnicodeBlockResult],
    per_page: int,
    page_number: int,
) -> Result:
    (full_page_count, final_page_length) = divmod(len(results), per_page)
    total_pages = full_page_count if final_page_length == 0 else (full_page_count + 1)
    if page_number > total_pages:
        return Result.Fail(f"Request for page #{page_number} is invalid since there are {total_pages} total pages.")
    has_more = page_number < total_pages
    page_start = per_page * (page_number - 1)
    page_end = min(len(results), page_start + per_page)
    paginated = {}
    paginated["total_results"] = len(results)
    paginated["has_more"] = has_more
    if has_more:
        paginated["next_page"] = page_number + 1
    paginated["results"] = results[page_start:page_end]
    return Result.Ok(paginated)
