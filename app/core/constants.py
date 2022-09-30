import re
from pathlib import Path


HEX_REGEX = re.compile(r"^(0x)?[A-Fa-f0-9]+$")

APP_FOLDER = Path(__file__).parent.parent
DATA_FOLDER = APP_FOLDER.joinpath("data")
