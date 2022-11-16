import re
from pathlib import Path

# REGEXES
CODE_POINT_REGEX = re.compile(r"(?:U\+(?P<code_point_prefix>[A-Fa-f0-9]{4,6}))|(?:(0x)?(?P<code_point>[A-Fa-f0-9]{2,6}))")

# STRINGS
DEFAULT_REDIS_URL = "redis://127.0.0.1:6379"

# NUMBERS
MAX_CODE_POINT = 1114111

# FOLDER PATHS
ROOT_FOLDER = Path(__file__).parent.parent.parent
APP_FOLDER = ROOT_FOLDER.joinpath("app")
DATA_FOLDER = APP_FOLDER.joinpath("data")

# FILE PATHS
DOTENV_FILE = ROOT_FOLDER.joinpath(".env")
