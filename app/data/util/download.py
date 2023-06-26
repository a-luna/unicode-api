from pathlib import Path
from urllib.parse import urlsplit

from requests import Response
from requests import get as requests_get
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError, RequestException, Timeout

from app.core.result import Result
from app.data.util.retry import RetryLimitExceededError, retry

CHUNK_SIZE = 1024


def download_file(url: str, dest_folder: Path) -> Result[Path]:
    (dest_file_path, remote_file_size) = get_file_details(url, dest_folder)
    if not remote_file_size:
        return initiate_download(url, dest_file_path)
    result = (
        initiate_download(url, dest_file_path)
        if not dest_file_path.exists()
        else resume_download(url, dest_file_path, remote_file_size)
    )
    if result.error:
        return result
    result = verify_download(dest_file_path, remote_file_size)
    if result.failure:
        return Result.Fail(result.error if result.error else "")
    return Result.Ok(dest_file_path)


def get_file_details(url: str, dest_folder: Path) -> tuple[Path, int]:
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest_file_path = dest_folder.joinpath(Path(urlsplit(url).path).name)
    r = requests_get.head(url)
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
    r = requests_get.get(url, stream=True, headers=resume_header)
    with open(dest_file_path, fopen_mode) as f:
        for chunk in r.iter_content(32 * CHUNK_SIZE):
            f.write(chunk)
    return Result.Ok(dest_file_path)


def verify_download(dest_file_path: Path, remote_file_size: int) -> Result[Response]:
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


def request_url_with_retries(url: str) -> Result[Response]:
    @retry(max_attempts=5, delay=5, exceptions=(ConnectionError, ConnectTimeout, HTTPError, Timeout, RequestException))
    def request_url(url: str) -> Response:
        response = requests_get(url, timeout=(5, 10))
        response.raise_for_status()
        return response

    try:
        response = request_url(url)
        return Result.Ok(response)
    except RetryLimitExceededError as e:
        return Result.Fail(repr(e))
