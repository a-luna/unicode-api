from pathlib import Path
from urllib.parse import urlsplit

import requests

from unicode_api.core.result import Result

CHUNK_SIZE = 1024
REQUEST_EXCEPTIONS = (
    requests.exceptions.ConnectionError,
    requests.exceptions.ConnectTimeout,
    requests.exceptions.HTTPError,
    requests.exceptions.Timeout,
    requests.exceptions.RequestException,
)


def download_file(url: str, dest_folder: Path) -> Result[Path]:
    """
    Downloads a file from the specified URL to the given destination folder.

    If the file already exists and its size matches the remote file, the download is verified.
    If the file exists but is incomplete, the download is resumed.
    If the file does not exist, a new download is initiated.

    Args:
        url (str): The URL of the file to download.
        dest_folder (Path): The destination folder where the file will be saved.

    Returns:
        Result[Path]: A Result object containing the path to the downloaded file on success,
                      or an error on failure.
    """
    (dest_file_path, remote_file_size) = _get_file_details(url, dest_folder)
    if not remote_file_size:
        return _initiate_download(url, dest_file_path)
    if dest_file_path.exists():
        result = _resume_download(url, dest_file_path, remote_file_size)
    else:
        result = _initiate_download(url, dest_file_path)
    return _verify_download(dest_file_path, remote_file_size) if result.success else result


def _get_file_details(url: str, dest_folder: Path) -> tuple[Path, int]:
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest_file_path = dest_folder.joinpath(Path(urlsplit(url).path).name)
    r = requests.head(url)
    remote_file_size = int(r.headers.get("content-length", 0))
    return (dest_file_path, remote_file_size)


def _initiate_download(url: str, dest_file_path: Path) -> Result[Path]:
    print(f"{dest_file_path.name!r} does not exist. Downloading...")
    return _download_file_in_chunks(url, dest_file_path)


def _resume_download(url: str, dest_file_path: Path, remote_file_size: int) -> Result[Path]:
    local_file_size = dest_file_path.stat().st_size
    if local_file_size == remote_file_size:
        print(f"{dest_file_path.name!r} is complete. Skipping...")
        return Result[Path].Ok(dest_file_path)
    print(f"{dest_file_path.name!r} is incomplete. Resuming...")
    return _download_file_in_chunks(url, dest_file_path, local_file_size)


def _download_file_in_chunks(url: str, dest_file_path: Path, local_file_size: int | None = None) -> Result[Path]:
    resume_header = {"Range": f"bytes={local_file_size}-"} if local_file_size else None
    fopen_mode = "ab" if local_file_size else "wb"
    try:
        r = requests.get(url, stream=True, headers=resume_header)
        with Path(dest_file_path).open(fopen_mode) as f:
            for chunk in r.iter_content(32 * CHUNK_SIZE):
                f.write(chunk)
        return Result[Path].Ok(dest_file_path)
    except REQUEST_EXCEPTIONS as ex:
        error = (
            f"Error! {type(ex)} occurred while attempting to download file:"
            f"\n\tURL: {url}"
            f"\n\tFile: {dest_file_path}"
            f"\n\tError: {repr(ex)}"
        )
        return Result[Path].Fail(error)


def _verify_download(dest_file_path: Path, remote_file_size: int) -> Result[Path]:
    local_file_size = dest_file_path.stat().st_size
    if local_file_size == remote_file_size:
        return Result[Path].Ok(dest_file_path)
    more_or_fewer = "more" if local_file_size > remote_file_size else "fewer"
    error = (
        f"Recieved {more_or_fewer} bytes than expected for {dest_file_path.name!r}!"
        f"\n\tExpected File Size: {remote_file_size:,} bytes"
        f"\n\tReceived File Size: {local_file_size:,} bytes"
    )
    return Result[Path].Fail(error)
