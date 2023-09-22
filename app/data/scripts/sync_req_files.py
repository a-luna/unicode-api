import re
from pathlib import Path

from app.core.result import Result
from app.data.util.command import run_command

ROOT_FOLDER = Path(__file__).parent.parent.parent.parent
REQ_BASE = ROOT_FOLDER.joinpath("requirements.txt")
REQ_DEV = ROOT_FOLDER.joinpath("requirements-dev.txt")
REQ_LOCK = ROOT_FOLDER.joinpath("requirements-lock.txt")
REQ_REGEX = re.compile(r"(?P<package>[\w-]+)==(?P<version>[\w.]+)")


def sync_requirements_files():
    result = create_lock_file()
    if result.failure:
        return result
    pinned_versions = parse_lock_file(REQ_LOCK)
    update_requirements(REQ_BASE, pinned_versions)
    update_requirements(REQ_DEV, pinned_versions)
    return Result.Ok()


def create_lock_file():
    return run_command(f"pip freeze > {REQ_LOCK}")


def parse_lock_file(req_file: Path) -> dict[str, str]:
    return dict(parsed for s in req_file.read_text().splitlines() if (parsed := parse_installed_package(s)))


def parse_installed_package(req: str) -> tuple[str, str] | None:
    match = REQ_REGEX.match(req)
    if not match:
        return None
    groups = match.groupdict()
    package = groups.get("package") or ""
    version = groups.get("version") or "0.0"
    return (package, version)


def update_requirements(req_file: Path, pinned_versions: dict[str, str]):
    requirements = parse_lock_file(req_file)
    updated_versions = {p: pinned_versions.get(p) for p in requirements if p in pinned_versions}
    req_file.write_text("\n".join([f"{name}=={ver}" for name, ver in updated_versions.items()]))


if __name__ == "__main__":
    sync_requirements_files()
