from functools import cached_property
from textwrap import dedent

from pydantic import ValidationError

import unicode_api.db.models as db
from unicode_api.core.cache import cached_data
from unicode_api.core.result import Result
from unicode_api.core.util import get_dict_report, s
from unicode_api.custom_types import UnicodePropertyGroupValues
from unicode_api.models.util import normalize_string_lm3


class CharacterFlagParameterMatcher:
    def __init__(self, param_name: str) -> None:
        self.param_name = param_name

    def parse_filter_params(self, values: list[str]) -> Result[list[db.CharacterFilterFlag]]:
        try:
            invalid_results: list[str] = []
            valid_results: list[db.CharacterFilterFlag] = []
            for str_val in values:
                if (did_parse := db.CharacterFilterFlag.match_loosely(str_val)) is not None:
                    valid_results.append(did_parse)
                else:
                    invalid_results.append(str_val)
            if not invalid_results:
                return Result[list[db.CharacterFilterFlag]].Ok(valid_results)
            error = get_error_report(self.param_name, invalid_results)
            return Result[list[db.CharacterFilterFlag]].Fail(error)
        except AttributeError:  # pragma: no cover
            error = (
                f"Filter parameter type {db.CharacterFilterFlag} does not contain a classmethod named match_loosely!"
            )
            return Result[list[db.CharacterFilterFlag]].Fail(error)


class CharacterPropGroupParameterMatcher:
    def __init__(self, param_name: str) -> None:
        self.param_name = param_name

    def parse_filter_params(self, values: list[str]) -> Result[list[db.CharPropertyGroup]]:
        try:
            invalid_results: list[str] = []
            valid_results: list[db.CharPropertyGroup] = []
            for str_val in values:
                if (did_parse := db.CharPropertyGroup.match_loosely(str_val)) is not None:
                    valid_results.append(did_parse)
                else:
                    invalid_results.append(str_val)
            if not invalid_results:
                return Result[list[db.CharPropertyGroup]].Ok(valid_results)
            error = get_error_report(self.param_name, invalid_results)
            return Result[list[db.CharPropertyGroup]].Fail(error)
        except AttributeError:  # pragma: no cover
            error = f"Filter parameter type {db.CharPropertyGroup} does not contain a classmethod named match_loosely!"
            return Result[list[db.CharPropertyGroup]].Fail(error)


class DatabaseFilterParameterMatcher[T: db.DatabaseCharacterProperty]:
    def __init__(self, prop_group: str, param_name: str, param_type: type[T]):
        self.prop_group = prop_group
        self.param_name = param_name
        self.param_type = param_type

    @cached_property
    def prop_value_map(self) -> dict[str, "UnicodePropertyGroupValues"]:
        prop_value_map: dict[str, UnicodePropertyGroupValues] = {}
        for v in cached_data.get_all_values_for_property_group(self.prop_group):
            if self.param_name == "ccc":
                prop_value_map[str(v["id"])] = v
            prop_value_map[normalize_string_lm3(v["short_name"])] = v
            prop_value_map[normalize_string_lm3(v["long_name"])] = v
        return prop_value_map

    def parse_filter_params(self, values: list[str]) -> Result[list[T]]:
        results = {str_val: self.parse_value_from_string(str_val) for str_val in values}
        return self.evaluate_parse_results(results)

    def parse_value_from_string(self, value: str) -> Result[T]:
        if (parsed := self.prop_value_map.get(normalize_string_lm3(value), None)) is None:
            return Result[T].Fail(f"{value!r} is not a valid value for the {self.param_name!r} property")
        try:
            prop_value = self.param_type.model_validate(parsed)
            return Result[T].Ok(prop_value)
        except ValidationError as ex:  # pragma: no cover
            error = f"""\
            Failed to validate dict value as a valid object of type {self.param_type}:
            Pydantic Error: {ex}\n
            {"\n".join(get_dict_report(parsed, title="INVALID DATA"))}
            """
            return Result[T].Fail(dedent(error))

    def evaluate_parse_results(self, results: dict[str, Result[T]]) -> Result[list[T]]:
        invalid_results = [str_val for str_val, result in results.items() if result.failure]
        valid_results = [result.value for result in results.values() if result.success and result.value]
        return (
            Result[list[T]].Ok(list(valid_results))
            if not invalid_results
            else Result[list[T]].Fail(get_error_report(self.param_name, invalid_results))
        )


def get_error_report(param_name: str, invalid_results: list[str]) -> str:
    return (
        f"{len(invalid_results)} value{s(invalid_results)} provided for the {param_name!r} parameter "
        f"{s(invalid_results, single='is', plural='are')} invalid: {invalid_results}"
    )
