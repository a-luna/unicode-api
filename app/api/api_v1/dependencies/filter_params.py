from __future__ import annotations

from http import HTTPStatus
from typing import Generic, Type, TypeVar

from fastapi import HTTPException, Query

import app.schemas.enums as enum
from app.core.result import Result
from app.docs.dependencies.custom_parameters import (
    CHAR_NAME_FILTER_DESCRIPTION,
    PAGE_NUMBER_DESCRIPTION,
    PER_PAGE_DESCRIPTION,
    get_description_and_values_table_for_bidi_class,
    get_description_and_values_table_for_combining_class_category,
    get_description_and_values_table_for_decomp_type,
    get_description_and_values_table_for_flags,
    get_description_and_values_table_for_general_category,
    get_description_and_values_table_for_joining_type,
    get_description_and_values_table_for_line_break_type,
    get_description_and_values_table_for_numeric_type,
    get_description_and_values_table_for_property_group,
    get_description_and_values_table_for_script_code,
    get_description_and_values_table_for_unicode_age,
)

T = TypeVar("T")


class FilterParameterMatcher(Generic[T]):
    param_name: str
    param_type: Type[T]

    def __init__(self, param_name, param_type):
        self.param_name = param_name
        self.param_type = param_type

    def parse_enum_values(self, values: list[str]) -> Result[list[T]]:
        if hasattr(self.param_type, "match_loosely"):
            match_loosely = getattr(self.param_type, "match_loosely")
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


class FilterParameters:
    def __init__(
        self,
        name: str | None = Query(default=None, description=CHAR_NAME_FILTER_DESCRIPTION),
        category: list[str]
        | None = Query(default=None, description=get_description_and_values_table_for_general_category()),
        age: list[str] | None = Query(default=None, description=get_description_and_values_table_for_unicode_age()),
        script: list[str] | None = Query(default=None, description=get_description_and_values_table_for_script_code()),
        bidi_class: list[str]
        | None = Query(default=None, description=get_description_and_values_table_for_bidi_class()),
        decomp_type: list[str]
        | None = Query(default=None, description=get_description_and_values_table_for_decomp_type()),
        line_break: list[str]
        | None = Query(default=None, description=get_description_and_values_table_for_line_break_type()),
        ccc: list[str]
        | None = Query(default=None, description=get_description_and_values_table_for_combining_class_category()),
        num_type: list[str]
        | None = Query(default=None, description=get_description_and_values_table_for_numeric_type()),
        join_type: list[str]
        | None = Query(default=None, description=get_description_and_values_table_for_joining_type()),
        flag: list[str] | None = Query(default=None, description=get_description_and_values_table_for_flags()),
        show_props: list[str]
        | None = Query(default=None, description=get_description_and_values_table_for_property_group()),
        per_page: int | None = Query(default=None, ge=1, le=100, description=PER_PAGE_DESCRIPTION),
        page: int | None = Query(default=None, ge=1, description=PAGE_NUMBER_DESCRIPTION),
    ):
        self.parse_all_enum_values(
            category, age, script, bidi_class, decomp_type, line_break, ccc, num_type, join_type, flag, show_props
        )
        self.name = name
        self.per_page = per_page or 10
        self.page = page or 1

    # @snoop
    def parse_all_enum_values(
        self,
        category: list[str] | None,
        age: list[str] | None,
        script: list[str] | None,
        bidi_class: list[str] | None,
        decomp_type: list[str] | None,
        line_break: list[str] | None,
        ccc: list[str] | None,
        num_type: list[str] | None,
        join_type: list[str] | None,
        flag: list[str] | None,
        show_props: list[str] | None,
    ) -> None:
        errors: list[str] = []
        self.categories: list[enum.GeneralCategory] | None = None
        self.age_list: list[enum.UnicodeAge] | None = None
        self.scripts: list[enum.ScriptCode] | None = None
        self.bidi_class_list: list[enum.BidirectionalClass] | None = None
        self.decomp_types: list[enum.DecompositionType] | None = None
        self.line_break_types: list[enum.LineBreakType] | None = None
        self.ccc_list: list[enum.CombiningClassCategory] | None = None
        self.num_types: list[enum.NumericType] | None = None
        self.join_types: list[enum.JoiningType] | None = None
        self.flags: list[enum.CharacterFilterFlags] | None = None
        self.show_props: list[enum.CharPropertyGroup] | None = None

        if category:
            GeneralCategoryMatcher = FilterParameterMatcher[enum.GeneralCategory]("category", enum.GeneralCategory)
            result = GeneralCategoryMatcher.parse_enum_values(category)
            if result.success:
                self.categories = result.value
            else:
                errors.append(result.error or "")

        if age:
            UnicodeAgeMatcher = FilterParameterMatcher[enum.UnicodeAge]("age", enum.UnicodeAge)
            result = UnicodeAgeMatcher.parse_enum_values(age)
            if result.success:
                self.age_list = result.value
            else:
                errors.append(result.error or "")

        if script:
            ScriptCodeMatcher = FilterParameterMatcher[enum.ScriptCode]("script", enum.ScriptCode)
            result = ScriptCodeMatcher.parse_enum_values(script)
            if result.success:
                self.scripts = result.value
            else:
                errors.append(result.error or "")

        if bidi_class:
            BidiClassMatcher = FilterParameterMatcher[enum.BidirectionalClass]("bidi_class", enum.BidirectionalClass)
            result = BidiClassMatcher.parse_enum_values(bidi_class)
            if result.success:
                self.bidi_class_list = result.value
            else:
                errors.append(result.error or "")

        if decomp_type:
            DecompTypeMatcher = FilterParameterMatcher[enum.DecompositionType]("decomp_type", enum.DecompositionType)
            result = DecompTypeMatcher.parse_enum_values(decomp_type)
            if result.success:
                self.decomp_types = result.value
            else:
                errors.append(result.error or "")

        if line_break:
            LineBreakMatcher = FilterParameterMatcher[enum.LineBreakType]("line_break", enum.LineBreakType)
            result = LineBreakMatcher.parse_enum_values(line_break)
            if result.success:
                self.line_break_types = result.value
            else:
                errors.append(result.error or "")

        if ccc:
            CombiningClassMatcher = FilterParameterMatcher[enum.CombiningClassCategory](
                "ccc", enum.CombiningClassCategory
            )
            result = CombiningClassMatcher.parse_enum_values(ccc)
            if result.success:
                self.ccc_list = result.value
            else:
                errors.append(result.error or "")

        if num_type:
            NumericTypeMatcher = FilterParameterMatcher[enum.NumericType]("num_type", enum.NumericType)
            result = NumericTypeMatcher.parse_enum_values(num_type)
            if result.success:
                self.num_types = result.value
            else:
                errors.append(result.error or "")

        if join_type:
            JoiningTypeMatcher = FilterParameterMatcher[enum.JoiningType]("join_type", enum.JoiningType)
            result = JoiningTypeMatcher.parse_enum_values(join_type)
            if result.success:
                self.join_types = result.value
            else:
                errors.append(result.error or "")

        if flag:
            CharFilterFlagMatcher = FilterParameterMatcher[enum.CharacterFilterFlags]("flag", enum.CharacterFilterFlags)
            result = CharFilterFlagMatcher.parse_enum_values(flag)
            if result.success:
                self.flags = result.value
            else:
                errors.append(result.error or "")

        if show_props:
            PropertyGroupMatcher = FilterParameterMatcher[enum.CharPropertyGroup]("show_props", enum.CharPropertyGroup)
            result = PropertyGroupMatcher.parse_enum_values(show_props)
            if result.success:
                self.show_props = result.value
            else:
                errors.append(result.error or "")

        if errors:
            all_errors = f"Invalid values were provided for the following {len(errors)} parameters:\n\n"
            all_errors += "\n\n".join(errors)
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=all_errors)
