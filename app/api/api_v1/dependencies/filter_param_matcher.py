from typing import Generic, Protocol, TypeVar

from app.core.result import Result
from app.schemas.enums import (
    BidirectionalClass,
    CharacterFilterFlags,
    CharPropertyGroup,
    CombiningClassCategory,
    DecompositionType,
    GeneralCategory,
    JoiningType,
    LineBreakType,
    NumericType,
    ScriptCode,
)
from app.schemas.enums.block_name import UnicodeBlockName
from app.schemas.enums.unicode_age import UnicodeAge

T = TypeVar("T", bound="IFilterable")


class IFilterable(Protocol):
    @classmethod
    def match_loosely(cls: type[T], value: str) -> T:
        """
        Return the enum value that matches the given value according to the Unicode loose-matching rule UAX44-LM3.
        ref: https://www.unicode.org/reports/tr44/#UAX44-LM3
        """
        ...


class FilterParameterMatcher:
    def __init__(self, param_name: str, param_type: IFilterable):
        self.param_name = param_name
        self.param_type = param_type

    def parse_enum_values(self, values: list[str]) -> Result[list[IFilterable]]:
        try:
            results = {str_val: self.param_type.match_loosely(str_val) for str_val in values}
            invalid_results = [str_val for str_val, did_parse in results.items() if not did_parse]
            return (
                Result.Ok(list(results.values()))
                if not invalid_results
                else Result.Fail(self._get_error_report(invalid_results))
            )
        except AttributeError:  # pragma: no cover
            return Result.Fail(
                f"Filter parameter type {self.param_type} does not contain a classmethod named match_loosely!"
            )

    def _get_error_report(self, invalid_results: list[str]) -> str:
        plural = len(invalid_results) > 1
        return (
            f'{len(invalid_results)} value{"s" if plural else ""} provided for the {self.param_name!r} parameter '
            f'{"are" if plural else "is"} invalid: {invalid_results}'
        )


def get_filter_param_matcher() -> dict[IFilterable, FilterParameterMatcher]:
    matcher = {
        UnicodeBlockName: FilterParameterMatcher("block", UnicodeBlockName),
        GeneralCategory: FilterParameterMatcher("category", GeneralCategory),
        UnicodeAge: FilterParameterMatcher("age", UnicodeAge),
        ScriptCode: FilterParameterMatcher("script", ScriptCode),
        BidirectionalClass: FilterParameterMatcher("bidi_class", BidirectionalClass),
        DecompositionType: FilterParameterMatcher("decomp_type", DecompositionType),
        LineBreakType: FilterParameterMatcher("line_break", LineBreakType),
        CombiningClassCategory: FilterParameterMatcher("ccc", CombiningClassCategory),
        NumericType: FilterParameterMatcher("num_type", NumericType),
        JoiningType: FilterParameterMatcher("join_type", JoiningType),
        CharacterFilterFlags: FilterParameterMatcher("flag", CharacterFilterFlags),
        CharPropertyGroup: FilterParameterMatcher("show_props", CharPropertyGroup),
    }
    return matcher


filter_param_matcher = get_filter_param_matcher()
