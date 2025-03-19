from functools import cached_property
from textwrap import dedent
from typing import TYPE_CHECKING

from pydantic import ValidationError

import app.db.models as db
from app.core.cache import cached_data
from app.core.result import Result
from app.core.util import get_dict_report, s
from app.models.util import normalize_string_lm3

if TYPE_CHECKING:  # pragma: no cover
    from app.custom_types import DatabaseCharacterProperty, UnicodePropertyGroupValues


class FilterParameterMatcher[T: db.CharacterFilterFlag | db.CharPropertyGroup]:
    def __init__(self, param_name: str, param_type: type[T]):
        self.param_name = param_name
        self.param_type = param_type

    def parse_filter_params(self, values: list[str]) -> Result[list[T]]:
        try:
            invalid_results: list[str] = []
            valid_results: list[db.CharacterFilterFlag | db.CharPropertyGroup] = []
            for str_val in values:
                if did_parse := self.param_type.match_loosely(str_val):
                    valid_results.append(did_parse)
                else:
                    invalid_results.append(str_val)
            return (
                Result.Ok(valid_results)
                if not invalid_results
                else Result.Fail(get_error_report(self.param_name, invalid_results))
            )
        except AttributeError:  # pragma: no cover
            return Result.Fail(
                f"Filter parameter type {self.param_type} does not contain a classmethod named match_loosely!"
            )


class DatabaseFilterParameterMatcher[T: "DatabaseCharacterProperty"]:
    def __init__(self, prop_group: str, param_name: str, param_type: type[T]):
        self.prop_group = prop_group
        self.param_name = param_name
        self.param_type = param_type

    @cached_property
    def prop_value_map(self) -> dict[str, "UnicodePropertyGroupValues"]:
        prop_value_map = {}
        for v in cached_data.get_all_values_for_property_group(self.prop_group):
            if self.param_name == "ccc":
                prop_value_map[str(v["id"])] = v
            prop_value_map[normalize_string_lm3(v["short_name"])] = v
            prop_value_map[normalize_string_lm3(v["long_name"])] = v
        return prop_value_map

    def parse_filter_params(self, values: list[str]) -> Result[list[T]]:
        results = {str_val: self.parse_value_from_string(str_val) for str_val in values}
        return self.evaluate_parse_results(self.param_name, results)

    def parse_value_from_string(self, value: str) -> Result[T]:
        if (parsed := self.prop_value_map.get(normalize_string_lm3(value), None)) is None:
            return Result.Fail(f"{value!r} is not a valid value for the {self.param_name!r} property")
        try:
            prop_value = self.param_type.model_validate(parsed)
            return Result.Ok(prop_value)
        except ValidationError as ex:
            error = f"""\
            Failed to validate dict value as a valid object of type {self.param_type}:
            Pydantic Error: {ex}
            {get_dict_report(parsed)}
            """
            return Result.Fail(dedent(error))

    def evaluate_parse_results(self, param_name: str, results: dict[str, Result[T]]) -> Result[list[T]]:
        invalid_results = [str_val for str_val, result in results.items() if result.failure]
        valid_results = [result.value for result in results.values() if result.success and result.value]
        return (
            Result.Ok(list(valid_results))
            if not invalid_results
            else Result.Fail(get_error_report(param_name, invalid_results))
        )


def get_error_report(param_name: str, invalid_results: list[str]) -> str:
    return (
        f"{len(invalid_results)} value{s(invalid_results)} provided for the {param_name!r} parameter "
        f"{s(invalid_results, single='is', plural='are')} invalid: {invalid_results}"
    )
