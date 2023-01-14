from pathlib import Path

from app.api_docs import get_api_docs_for_readme
from app.core.config import ROOT_FOLDER


def update_readme():
    ROOT_FOLDER.joinpath("README.md").write_text(get_api_docs_for_readme())


if __name__ == "__main__":
    update_readme()
