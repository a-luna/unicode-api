"""
Synchronizes package versions across Python requirements files.

This script ensures that all packages referenced in requirements.txt and requirements-dev.txt
use consistent version pins based on the current virtual environment. It helps maintain
dependency consistency across development and production environments.

Process:
1. Creates a lock file using `pip freeze` to capture current environment versions
2. Extracts package name and version information from the lock file
3. Updates each requirements file with pinned versions for existing packages
4. Preserves the original package selection (doesn't add/remove packages)

Functions:
    sync_requirements_files(project_dir: Path) -> Result[None]:
        Main entry point that synchronizes all requirement files.

    _get_pinned_versions(project_dir: Path) -> Result[dict[str, str]]:
        Generates a dictionary of package names to pinned versions.

    _create_lock_file(project_dir: Path) -> Result[Path]:
        Creates a temporary requirements-lock.txt file using pip freeze.

    _extract_packages_from_file(req_file: Path) -> dict[str, str]:
        Parses a requirements file into a package name to version dictionary.

    _parse_requirement_line(req: str) -> tuple[str, str] | None:
        Extracts package name and version from a single requirement line.

    _update_requirements_file(req_file: Path, pinned: dict[str, str]) -> None:
        Updates a single requirements file with pinned versions.

Constants:
    REQ_REGEX: Regular expression for parsing package==version format

Usage:
    Run directly to synchronize requirements in the current directory:
    $ python -m unicode_api.data.scripts.sync_req_files
"""

import re
from pathlib import Path

from unicode_api.core.result import Result
from unicode_api.data.util.command import run_command

REQ_REGEX = re.compile(r"(?P<package>[\w-]+)==(?P<version>[\w.]+)")


def sync_requirements_files(project_dir: Path) -> Result[None]:
    """
    Synchronizes the pinned package versions in the project's requirements files.

    This function first generates a set of pinned package versions by calling a helper function.
    It then updates the 'requirements.txt' and 'requirements-dev.txt' files in the specified
    project directory with these pinned versions, if those files exist.

    Args:
        project_dir (Path): The root directory of the project containing the requirements files.

    Returns:
        Result[None]: A Result object indicating success or failure. On failure, the error
        from the pinning process is propagated.
    """
    result = _get_pinned_versions(project_dir)
    if result.failure or not (pinned_versions := result.value):
        return Result[None].Fail(result.error)

    if (req_base := project_dir.joinpath("requirements.txt")).exists():
        _update_requirements_file(req_base, pinned_versions)
    if (req_dev := project_dir.joinpath("requirements-dev.txt")).exists():
        _update_requirements_file(req_dev, pinned_versions)
    return Result[None].Ok()


def _get_pinned_versions(project_dir: Path) -> Result[dict[str, str]]:
    result = _create_lock_file(project_dir)
    if result.failure or not result.value:
        return Result[dict[str, str]].Fail(result.error)
    lock_file = result.value
    return Result[dict[str, str]].Ok(_extract_packages_from_file(lock_file))


def _create_lock_file(project_dir: Path) -> Result[Path]:
    lock_file = project_dir.joinpath("requirements-lock.txt")
    result = run_command(f"pip freeze > {lock_file}")
    if result.failure:
        return Result[Path].Fail(result.error)
    return Result[Path].Ok(lock_file)


def _extract_packages_from_file(requirements_file: Path) -> dict[str, str]:
    package_versions: dict[str, str] = {}
    for line in requirements_file.read_text().splitlines():
        if requirement := _parse_requirement_line(line):
            package_name, version = requirement
            package_versions[package_name] = version
    return package_versions


def _parse_requirement_line(req: str) -> tuple[str, str] | None:
    match = REQ_REGEX.match(req)
    if not match:
        return None
    groups = match.groupdict()
    package = groups.get("package") or ""
    version = groups.get("version") or "0.0"
    return (package, version)


def _update_requirements_file(requirements_file: Path, pinned_versions: dict[str, str]) -> None:
    try:
        lines = requirements_file.read_text().splitlines()
        updated_lines: list[str] = []

        for line in lines:
            # If line is a package requirement, update its version
            if parsed := _parse_requirement_line(line):
                package_name, _ = parsed
                if package_name in pinned_versions:
                    updated_lines.append(f"{package_name}=={pinned_versions[package_name]}")
                else:
                    # Preserve original line if package not in pinned versions
                    updated_lines.append(line)
            else:
                # Preserve comments, blank lines, and other non-package content
                updated_lines.append(line)

        requirements_file.write_text("\n".join(updated_lines))
    except OSError as e:
        print(f"Error updating {requirements_file}: {e}")


if __name__ == "__main__":
    project_dir = Path.cwd()
    sync_requirements_files(project_dir)
