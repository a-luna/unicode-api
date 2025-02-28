import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

from app.config.api_settings import UnicodeApiSettings, get_settings
from app.constants import ALL_PROP_GROUPS
from app.core.result import Result
from app.core.util import slugify
from app.data.util import download_file

if TYPE_CHECKING:  # pragma: no cover
    from app.custom_types import UnicodePropertyGroupMap

FILE_HEADER_END_REGEX = re.compile(r"^# ==+")

NO_VALUE = {
    "id": 1,
    "short_name": "N",
    "long_name": "No                               ; F                                ; False",
}
YES_VALUE = {
    "id": 2,
    "short_name": "Y",
    "long_name": "Yes                              ; T                                ; True",
}
BOOL_PROP_VALUES = {"1": NO_VALUE, "2": YES_VALUE}


def get_prop_values(settings: UnicodeApiSettings) -> Result[None]:
    result = download_prop_value_aliases_txt_file(settings)
    if result.failure:
        if "Recieved more bytes than expected" in result.error:
            result.value = settings.PROP_VALUES_FILE
        else:
            return Result.Fail(result.error)
    if not (txt_file := result.value):
        return Result.Fail("No file downloaded.")
    return parse_prop_value_aliases_txt_file(settings, txt_file)


def download_prop_value_aliases_txt_file(settings: UnicodeApiSettings) -> Result[Path]:
    result = download_file(settings.PROP_VALUES_URL, settings.TXT_FOLDER)
    if result.failure:
        return result
    if not (txt_file := result.value):
        return Result.Fail("Download attempt failed, please check internet connection.")
    if not txt_file.exists() or not txt_file.is_file():
        return Result.Fail("Download attempt failed, please check internet connection.")
    return Result.Ok(txt_file)


def parse_prop_value_aliases_txt_file(settings: UnicodeApiSettings, txt_file: Path) -> Result[None]:
    result = PropertyValueAliasesTextFileReader(txt_file).parse_file()
    if result.failure:
        return Result.Fail(result.error)
    settings.PROP_VALUES_JSON.write_text(json.dumps(result.value, indent=4))
    return Result.Ok()


class PropertyValueAliasesTextFileReader:
    txt_file: Path
    begin_parsing_file: bool
    begin_parsing_prop_values: bool
    skipped_initial_blank_line: bool
    group_name: str
    group_map: dict
    prop_value_map: "UnicodePropertyGroupMap"
    boolean_prop_names: list[str]

    def __init__(self, txt_file: Path) -> None:
        self.txt_file = txt_file

    def parse_file(self) -> Result["UnicodePropertyGroupMap"]:
        self._initialize_file_reader()
        self._read_txt_file()
        self._perform_final_processes()
        return Result.Ok(self.prop_value_map)

    def _initialize_file_reader(self) -> None:
        self.begin_parsing_file = False
        self.begin_parsing_prop_values = False
        self.skipped_initial_blank_line = False
        self.group_name = ""
        self.group_map = {}
        self.prop_value_map: UnicodePropertyGroupMap = {}  # type: ignore[reportAssignmentType]
        self.boolean_prop_names = []

    def _read_txt_file(self) -> None:
        with self.txt_file.open(encoding="utf-8") as f:
            end_of_file = self._read_line(f.readline())
            while not end_of_file:
                end_of_file = self._read_line(f.readline())

    def _read_line(self, line: str) -> bool:
        if "# EOF" in line:
            return True
        if not self.begin_parsing_file:
            if FILE_HEADER_END_REGEX.match(line):
                self.begin_parsing_file = True
            return False
        elif not self.begin_parsing_prop_values:
            if line.startswith("# "):
                self._begin_parsing_property_group(line)
            return False
        elif self.begin_parsing_prop_values and not self.skipped_initial_blank_line:
            if line == "\n":
                self.skipped_initial_blank_line = True
            return False
        if line.startswith("# @missing"):
            return False
        elif line != "\n":
            self._parse_entry_for_group_map(line)
        else:
            self._handle_complete_group_map()
        return False

    def _begin_parsing_property_group(self, line: str) -> None:
        self.begin_parsing_prop_values = True
        self.skipped_initial_blank_line = False
        _, self.group_name, _ = line.split(" ", maxsplit=2)
        self.group_name = self.group_name.strip()
        self.group_map = {}

    def _parse_entry_for_group_map(self, line: str) -> None:
        split = line.split(";", maxsplit=2)
        if len(split) < 3:
            raise ValueError(f"Unable to parse entry in PropertyValueAliases.txt:\n\nData: {line}\nSplit: {split}")
        value_id, short_name, long_name = (len(self.group_map) + 1, split[1].strip(), split[2].strip())
        if self.group_name == "Age" and short_name in ["n/a", "NA"] and long_name.lower() != "unassigned":
            short_name = long_name
            long_name = self._create_unicode_version_long_name_from_short_name(short_name)
        if self.group_name == "Canonical_Combining_Class":
            value_id = int(short_name)
            short_name, long_name = (s.strip() for s in long_name.split(";", maxsplit=1))
        self.group_map[str(value_id)] = {"id": value_id, "short_name": short_name, "long_name": long_name}

    def _create_unicode_version_long_name_from_short_name(self, short_name: str) -> str:
        split = short_name.split(".", maxsplit=1)
        major, minor = split[0].strip(), split[1].strip()
        return f"V{major}_{minor}"

    def _handle_complete_group_map(self):
        if self.group_map == BOOL_PROP_VALUES:
            self.boolean_prop_names.append(self.group_name)
        elif len(self.group_map) > 0:
            self.prop_value_map[self.group_name] = self.group_map
        self.begin_parsing_prop_values = False
        self.skipped_initial_blank_line = False

    def _perform_final_processes(self) -> None:
        self._refine_general_category_values()
        self._refine_canonical_combining_class_values()
        self._sanitize_prop_value_long_names()
        self.prop_value_map["boolean_properties"] = self.boolean_prop_names
        self.prop_value_map["missing_prop_groups"] = self._get_missing_prop_group_names()

    def _refine_general_category_values(self) -> None:
        general_category_values = self.prop_value_map["General_Category"]
        for value_dict in general_category_values.values():
            if "#" in value_dict["long_name"]:
                long_name, grouped_values = value_dict["long_name"].split("#", maxsplit=1)
                value_dict["long_name"] = long_name.strip()
                value_dict["is_group"] = True
                value_dict["grouped_values"] = grouped_values.strip()
            else:
                value_dict["is_group"] = False
                value_dict["grouped_values"] = ""

    def _refine_canonical_combining_class_values(self) -> None:
        ccc_values = self.prop_value_map["Canonical_Combining_Class"]
        for n in range(10, 200):
            if f"{n}" in ccc_values:
                continue
            ccc_values[f"{n}"] = {"id": n, "short_name": f"CCC{n}", "long_name": f"CCC{n}"}

        if "214" not in ccc_values:
            ccc_values["214"] = {"id": 214, "short_name": "ATA", "long_name": "Attached_Above"}

    def _sanitize_prop_value_long_names(self) -> None:
        for prop_values in self.prop_value_map.values():
            if isinstance(prop_values, list):
                continue
            elif isinstance(prop_values, dict):
                for value_dict in prop_values.values():
                    if any((s := sep) in value_dict["long_name"] for sep in [";", "#"]):
                        long_name, _ = value_dict["long_name"].split(s, maxsplit=1)
                        value_dict["long_name"] = long_name.strip()

    def _get_missing_prop_group_names(self) -> list[str]:
        missing_prop_groups = list(set(ALL_PROP_GROUPS) - set(self.prop_value_map.keys()))
        return [slugify(group_name, "_") for group_name in missing_prop_groups]


if __name__ == "__main__":
    settings = get_settings()
    result = parse_prop_value_aliases_txt_file(settings, settings.PROP_VALUES_FILE)
    if result.failure:
        print(result.error)
