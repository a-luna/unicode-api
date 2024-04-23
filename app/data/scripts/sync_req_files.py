import re
from pathlib import Path

from app.core.result import Result
from app.data.util.command import run_command

REQ_REGEX = re.compile(r"(?P<package>[\w-]+)==(?P<version>[\w.]+)")


def sync_requirements_files(project_dir: Path):
    result = pin_requirements(project_dir)
    if result.failure:
        return Result.Fail(result.error)
    pinned_versions = result.value

    if (req_base := project_dir.joinpath("requirements.txt")).exists():
        update_req_file(req_base, pinned_versions)
    if (req_dev := project_dir.joinpath("requirements-dev.txt")).exists():
        update_req_file(req_dev, pinned_versions)
    return Result.Ok()


def pin_requirements(project_dir: Path) -> Result[dict[str, str]]:
    result = create_lock_file(project_dir)
    if result.failure:
        return Result.Fail(result.error)
    lock_file = result.value
    return Result.Ok(parse_lock_file(lock_file))


def create_lock_file(project_dir: Path) -> Result[Path]:
    lock_file = project_dir.joinpath("requirements-lock.txt")
    result = run_command(f"pip freeze > {lock_file}")
    if result.failure:
        return result
    return Result.Ok(lock_file)


def parse_lock_file(req_file: Path) -> dict[str, str]:
    return dict(pkg for line in req_file.read_text().splitlines() if (pkg := parse_lock_file_entry(line)))


def parse_lock_file_entry(req: str) -> tuple[str, str] | None:
    match = REQ_REGEX.match(req)
    if not match:
        return None
    groups = match.groupdict()
    package = groups.get("package") or ""
    version = groups.get("version") or "0.0"
    return (package, version)


def update_req_file(req_file: Path, pinned: dict[str, str]):
    updated_versions = {package: pinned.get(package) for package in parse_lock_file(req_file) if package in pinned}
    req_file.write_text("\n".join([f"{name}=={ver}" for name, ver in updated_versions.items()]))


if __name__ == "__main__":
    project_dir = Path.cwd()
    sync_requirements_files(project_dir)
