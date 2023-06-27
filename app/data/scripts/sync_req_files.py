from pathlib import Path

from app.core.config import ROOT_FOLDER

REQ_BASE = ROOT_FOLDER.joinpath('requirements.txt')
REQ_DEV = ROOT_FOLDER.joinpath('requirements-dev.txt')
REQ_LOCK = ROOT_FOLDER.joinpath('requirements-lock.txt')

def sync_requirements_files():
    pinned_versions = parse_lock_file()
    update_requirements(REQ_BASE, pinned_versions)
    update_requirements(REQ_DEV, pinned_versions)


def parse_lock_file() -> dict[str, str]:
    lines = [s.split("==", maxsplit=1) for s in REQ_LOCK.read_text().splitlines() if s]
    return {r[0]: r[1] for r in lines if len(r) == 2}


def update_requirements(req_file: Path, pinned_versions: dict[str, str]):
    package_names = [s.split("==", maxsplit=1)[0] for s in req_file.read_text().splitlines() if s]
    updated_versions = {package: pinned_versions.get(package) for package in package_names if package in pinned_versions}
    REQ_BASE.write_text("\n".join([f"{name}=={ver}" for name, ver in updated_versions.items()]))