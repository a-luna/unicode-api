from http import HTTPStatus

from fastapi import HTTPException, Query

from app.core.result import Result
from app.docs.dependencies.custom_parameters import (
    CHAR_NAME_FILTER_DESCRIPTION,
    PAGE_NUMBER_DESCRIPTION,
    PER_PAGE_DESCRIPTION,
    get_description_and_values_table_for_bidi_class,
    get_description_and_values_table_for_combining_class_category,
    get_description_and_values_table_for_decomp_type,
    get_description_and_values_table_for_general_category,
    get_description_and_values_table_for_line_break_type,
    get_description_and_values_table_for_property_group,
    get_description_and_values_table_for_script_code,
    get_description_and_values_table_for_unicode_age,
)
from app.schemas.enums import (
    BidirectionalClass,
    CharPropertyGroup,
    CombiningClassCategory,
    DecompositionType,
    GeneralCategory,
    LineBreakType,
    ScriptCode,
    UnicodeAge,
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
        show_props: list[str]
        | None = Query(default=None, description=get_description_and_values_table_for_property_group()),
        per_page: int | None = Query(default=None, ge=1, le=100, description=PER_PAGE_DESCRIPTION),
        page: int | None = Query(default=None, ge=1, description=PAGE_NUMBER_DESCRIPTION),
    ):
        self.parse_all_enum_values(category, age, script, bidi_class, decomp_type, line_break, ccc, show_props)
        self.name = name
        self.per_page = per_page or 10
        self.page = page or 1

    def parse_all_enum_values(
        self,
        category: list[str] | None,
        age: list[str] | None,
        script: list[str] | None,
        bidi_class: list[str] | None,
        decomp_type: list[str] | None,
        line_break: list[str] | None,
        ccc: list[str] | None,
        show_props: list[str] | None,
    ):
        errors = []
        self.categories = None
        self.age_list = None
        self.scripts = None
        self.bidi_class_list = None
        self.decomp_types = None
        self.line_break_types = None
        self.ccc_list = None
        self.show_props = None

        if category:
            result = parse_enum_values_from_parameter(GeneralCategory, "category", category)
            if result.success:
                self.categories = result.value
            else:
                errors.append(result.error)

        if age:
            result = parse_enum_values_from_parameter(UnicodeAge, "age", age)
            if result.success:
                self.age_list = result.value
            else:
                errors.append(result.error)

        if script:
            result = parse_enum_values_from_parameter(ScriptCode, "script", script)
            if result.success:
                self.scripts = result.value
            else:
                errors.append(result.error)

        if bidi_class:
            result = parse_enum_values_from_parameter(BidirectionalClass, "bidi_class", bidi_class)
            if result.success:
                self.bidi_class_list = result.value
            else:
                errors.append(result.error)

        if decomp_type:
            result = parse_enum_values_from_parameter(DecompositionType, "decomp_type", decomp_type)
            if result.success:
                self.decomp_types = result.value
            else:
                errors.append(result.error)

        if line_break:
            result = parse_enum_values_from_parameter(LineBreakType, "line_break", line_break)
            if result.success:
                self.line_break_types = result.value
            else:
                errors.append(result.error)

        if ccc:
            result = parse_enum_values_from_parameter(CombiningClassCategory, "combining_class", ccc)
            if result.success:
                self.ccc_list = result.value
            else:
                errors.append(result.error)

        if show_props:
            result = parse_enum_values_from_parameter(CharPropertyGroup, "show_props", show_props)
            if result.success:
                self.show_props = result.value
            else:
                errors.append(result.error)

        if errors:
            all_errors = f"Invalid values were provided for the following {len(errors)} parameters:\n\n"
            all_errors += "\n\n".join(errors)
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=all_errors)


def parse_enum_values_from_parameter(enum_class, param_name: str, values: list[str]):
    results = {str_val: enum_class.match_loosely(str_val) for str_val in values}
    invalid_results = [str_val for str_val, did_parse in results.items() if not did_parse]
    if not invalid_results:
        return Result.Ok(list(results.values()))
    else:
        plural = len(invalid_results) > 1
        error = (
            f'{len(invalid_results)} value{"s" if plural else ""} provided for the {param_name!r} parameter '
            f'{"are" if plural else "is"} invalid: {invalid_results}'
        )
        return Result.Fail(error)
