import os
from pathlib import Path

from unicode_api.core.result import Result


def load_dotenv_file() -> Result[None]:
    dotenv_path = _get_env_file_path()
    if not dotenv_path.is_file():  # pragma: no cover
        return Result[None].Fail(f".env file not found: {dotenv_path}")
    env_vars_from_file = [
        var_name_and_value
        for line in dotenv_path.read_text().splitlines()
        if (var_name_and_value := _parse_env_line(line))
    ]
    os.environ.update(dict(env_vars_from_file))
    return Result[None].Ok()


def _get_env_file_path() -> Path:
    env = os.environ.get("ENV", "DEV")
    app_folder = Path(__file__).parent.parent
    root_folder = app_folder.parent if env.upper() == "PROD" else app_folder.parent.parent
    return root_folder.joinpath(".env")


def _parse_env_line(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        return None
    key, value = line.split("=", maxsplit=1)
    key = key.strip()
    value = value.strip().strip("\"'")
    if not key:
        return None
    return key, value
