import os
from pathlib import Path
from pprint import pprint


def read_dotenv_file(dotenv_filepath: Path) -> dict[str, str]:
    if not dotenv_filepath.is_file():  # pragma: no cover
        raise TypeError(f"Unable to open file: {dotenv_filepath}")
    env_var_pairs = [s.split("=", maxsplit=1) for s in dotenv_filepath.read_text().splitlines() if s and "=" in s]
    env_var_dict = {v[0]: v[1].strip('"').strip("'").strip() for v in env_var_pairs if len(v) == 2}
    for var_name, value in env_var_dict.items():
        os.environ[var_name] = value
    print(f"{'#' * 10} ENV_VAR_PAIRS (read_dotenv_file) {'#' * 10}\n\n")
    pprint(env_var_pairs)
    print(f"\n\n{'#' * 35}\n\n")
    print(f"{'#' * 10} ENV_VAR_DICT (read_dotenv_file) {'#' * 10}\n\n")
    pprint(env_var_dict)
    print(f"\n\n{'#' * 34}\n\n")
    return env_var_dict
