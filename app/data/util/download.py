from pathlib import Path
from urllib.parse import urlsplit

from requests import Response
from requests import get as requests_get
from requests import head as requests_head
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError, RequestException, Timeout

from app.core.result import Result
from app.data.util.retry import RetryLimitExceededError, retry

CHUNK_SIZE = 1024
REQUEST_EXCEPTIONS = (ConnectionError, ConnectTimeout, HTTPError, Timeout, RequestException)


def download_file(url: str, dest_folder: Path) -> Result[Path]:
    (dest_file_path, remote_file_size) = _get_file_details(url, dest_folder)
    if not remote_file_size:
        return _initiate_download(url, dest_file_path)
    result = (
        _initiate_download(url, dest_file_path)
        if not dest_file_path.exists()
        else _resume_download(url, dest_file_path, remote_file_size)
    )
    return _verify_download(dest_file_path, remote_file_size) if result.success else result


def _get_file_details(url: str, dest_folder: Path) -> tuple[Path, int]:
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest_file_path = dest_folder.joinpath(Path(urlsplit(url).path).name)
    r = requests_head(url)
    remote_file_size = int(r.headers.get("content-length", 0))
    return (dest_file_path, remote_file_size)


def _initiate_download(url: str, dest_file_path: Path) -> Result[Path]:
    print(f"{dest_file_path.name!r} does not exist. Downloading...")
    return _download_file_in_chunks(url, dest_file_path)


def _resume_download(url: str, dest_file_path: Path, remote_file_size: int) -> Result[Path]:
    local_file_size = dest_file_path.stat().st_size
    if local_file_size == remote_file_size:
        print(f"{dest_file_path.name!r} is complete. Skipping...")
        return Result.Ok(dest_file_path)
    print(f"{dest_file_path.name!r} is incomplete. Resuming...")
    return _download_file_in_chunks(url, dest_file_path, local_file_size, fopen_mode="ab")


def _download_file_in_chunks(
    url: str, dest_file_path: Path, local_file_size: int | None = None, fopen_mode: str = "wb"
) -> Result[Path]:
    resume_header = {"Range": f"bytes={local_file_size}-"} if local_file_size else None
    try:
        r = requests_get(url, stream=True, headers=resume_header)
        with open(dest_file_path, fopen_mode) as f:
            for chunk in r.iter_content(32 * CHUNK_SIZE):
                f.write(chunk)
        return Result.Ok(dest_file_path)
    except REQUEST_EXCEPTIONS as ex:
        error = (
            f"Error! {type(ex)} occurred while attempting to download file:\n"
            f"\tFile: {dest_file_path}\n"
            f"\tError: {repr(ex)}"
        )
        return Result.Fail(error)


def _verify_download(dest_file_path: Path, remote_file_size: int) -> Result[Path]:
    local_file_size = dest_file_path.stat().st_size
    if local_file_size == remote_file_size:
        return Result.Ok(dest_file_path)
    more_or_fewer = "more" if local_file_size > remote_file_size else "fewer"
    error = (
        f"Recieved {more_or_fewer} bytes than expected for {dest_file_path.name!r}!\n"
        f"Expected File Size: {remote_file_size:,} bytes\n"
        f"Received File Size: {local_file_size:,} bytes"
    )
    return Result.Fail(error)


def request_url_with_retries(url: str) -> Result[Response]:
    @retry(max_attempts=5, delay=5, exceptions=REQUEST_EXCEPTIONS)
    def request_url(url: str) -> Response:
        response = requests_get(url, timeout=(5, 10))
        response.raise_for_status()
        return response

    try:
        response = request_url(url)
        return Result.Ok(response)
    except RetryLimitExceededError as ex:
        error = f"Error! {__name__} occurred while requesting URL:\n" f"\tURL: {url}\n" f"\tError: {repr(ex)}"
        return Result.Fail(error)
