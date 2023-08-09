from typing import Generic, TypeVar

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

T = TypeVar("T")


class FilterParameterMatcher(Generic[T]):
    param_name: str
    param_type: type[T]

    def __init__(self, param_name, param_type):
        self.param_name = param_name
        self.param_type = param_type
        self.method_name = "match_loosely"

    def parse_enum_values(self, values: list[str]) -> Result[list[T]]:
        if hasattr(self.param_type, "match_loosely"):
            match_loosely = getattr(self.param_type, self.method_name)
            results = {str_val: match_loosely(str_val) for str_val in values}
            invalid_results = [str_val for str_val, did_parse in results.items() if not did_parse]
            return (
                Result.Ok(list(results.values()))
                if not invalid_results
                else Result.Fail(self.get_error_report(invalid_results))
            )
        return Result.Fail(
            f"Filter parameter type {self.param_type} does not contain a classmethod named match_loosely!"
        )  # pragma: no cover

    def get_error_report(self, invalid_results: list[str]) -> str:
        plural = len(invalid_results) > 1
        return (
            f'{len(invalid_results)} value{"s" if plural else ""} provided for the {self.param_name!r} parameter '
            f'{"are" if plural else "is"} invalid: {invalid_results}'
        )


FilterParamType = (
    UnicodeBlockName
    | GeneralCategory
    | UnicodeAge
    | ScriptCode
    | BidirectionalClass
    | DecompositionType
    | LineBreakType
    | CombiningClassCategory
    | NumericType
    | JoiningType
    | CharacterFilterFlags
    | CharPropertyGroup
)


def get_filter_param_matcher() -> dict[FilterParamType, FilterParameterMatcher[FilterParamType]]:
    matcher = {
        UnicodeBlockName: FilterParameterMatcher[UnicodeBlockName]("block", UnicodeBlockName),
        GeneralCategory: FilterParameterMatcher[GeneralCategory]("category", GeneralCategory),
        UnicodeAge: FilterParameterMatcher[UnicodeAge]("age", UnicodeAge),
        ScriptCode: FilterParameterMatcher[ScriptCode]("script", ScriptCode),
        BidirectionalClass: FilterParameterMatcher[BidirectionalClass]("bidi_class", BidirectionalClass),
        DecompositionType: FilterParameterMatcher[DecompositionType]("decomp_type", DecompositionType),
        LineBreakType: FilterParameterMatcher[LineBreakType]("line_break", LineBreakType),
        CombiningClassCategory: FilterParameterMatcher[CombiningClassCategory]("ccc", CombiningClassCategory),
        NumericType: FilterParameterMatcher[NumericType]("num_type", NumericType),
        JoiningType: FilterParameterMatcher[JoiningType]("join_type", JoiningType),
        CharacterFilterFlags: FilterParameterMatcher[CharacterFilterFlags]("flag", CharacterFilterFlags),
        CharPropertyGroup: FilterParameterMatcher[CharPropertyGroup]("show_props", CharPropertyGroup),
    }
    return matcher


filter_param_matcher = get_filter_param_matcher()
