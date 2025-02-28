import subprocess
import sys
from pathlib import Path

from app.core.result import Result


def run_command(command: str, cwd: Path | None = None, shell: bool = True, text: bool = True) -> Result[None]:
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
            f"An error occurred while executing the command below:\n\tCommand: {e.cmd} (return code = {e.returncode})"
        )
        if e.stderr:
            error += f"\n\tError: {e.stderr}"
        return Result.Fail(error)
