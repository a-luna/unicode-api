from pathlib import Path

from app.core.config import ROOT_FOLDER
from app.data.util.command import run_command

REQ_BASE = ROOT_FOLDER.joinpath("requirements.txt")
REQ_DEV = ROOT_FOLDER.joinpath("requirements-dev.txt")
REQ_LOCK = ROOT_FOLDER.joinpath("requirements-lock.txt")


def sync_requirements_files():
    pinned_versions = parse_lock_file(REQ_LOCK)
    update_requirements(REQ_BASE, pinned_versions)
    update_requirements(REQ_DEV, pinned_versions)


def create_lock_file():
    run_command(f"pip freeze > {REQ_LOCK}")


def parse_lock_file(req_file: Path) -> dict[str, str]:
    parsed_reqs = [tuple(s.split("==", maxsplit=1)) for s in req_file.read_text().splitlines() if s]
    return {name: version for (name, version) in parsed_reqs}


def update_requirements(req_file: Path, pinned_versions: dict[str, str]):
    requirements = parse_lock_file(req_file)
    updated_versions = {p: pinned_versions.get(p) for p in requirements.keys() if p in pinned_versions}
    req_file.write_text("\n".join([f"{name}=={ver}" for name, ver in updated_versions.items()]))
