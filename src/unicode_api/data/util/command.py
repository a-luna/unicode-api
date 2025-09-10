import subprocess
import sys
from pathlib import Path

from unicode_api.core.result import Result


def run_command(command: str, cwd: Path | None = None, shell: bool = True, text: bool = True) -> Result[None]:
    """
    Executes a shell command in a subprocess and returns a Result indicating success or failure.

    Args:
        command (str): The command to execute.
        cwd (Path | None, optional): The working directory in which to execute the command. Defaults to None.
        shell (bool, optional): Whether to execute the command through the shell. Defaults to True.
        text (bool, optional): Whether to treat input and output as text. Defaults to True.

    Returns:
        Result[None]: Result.Ok() if the command executes successfully, or Result.Fail(error_message) if
        an error occurs.
    """
    try:
        subprocess.check_call(
            command,
            stdout=sys.stdout,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            shell=shell,
            text=text,
        )
        return Result[None].Ok()
    except subprocess.CalledProcessError as e:
        error = (
            f"An error occurred while executing the command below:\n\tCommand: {e.cmd} (return code = {e.returncode})"
        )
        if e.stderr:
            error += f"\n\tError: {e.stderr}"
        return Result[None].Fail(error)
