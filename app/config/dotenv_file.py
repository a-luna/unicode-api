import os
from pathlib import Path


def read_dotenv_file(dotenv_filepath: Path) -> dict[str, str]:
    if not dotenv_filepath.is_file():  # pragma: no cover
        raise TypeError(f"Unable to open file: {dotenv_filepath}")
    env_var_pairs = [s.split("=", maxsplit=1) for s in dotenv_filepath.read_text().splitlines() if s and "=" in s]
    env_var_dict = {v[0]: v[1].strip('"').strip("'").strip() for v in env_var_pairs if len(v) == 2}
    for var_name, value in env_var_dict.items():
        os.environ[var_name] = value
    return env_var_dict
