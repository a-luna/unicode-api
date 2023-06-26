import os
from pathlib import Path


class DotEnvFile:
    def __init__(self, dotenv_filepath: Path):
        self.dotenv_filepath = dotenv_filepath
        self.read_dotenv_file()

    def read_dotenv_file(self):
        if not self.dotenv_filepath.is_file():  # pragma: no cover
            raise TypeError(f"Unable to open file: {self.dotenv_filepath}")
        env_var_pairs = [
            s.split("=", maxsplit=1) for s in self.dotenv_filepath.read_text().splitlines() if s and "=" in s
        ]
        env_var_dict = {v[0]: v[1].strip('"').strip("'").strip() for v in env_var_pairs if len(v) == 2}
        for var_name, value in env_var_dict.items():
            os.environ[var_name] = value
