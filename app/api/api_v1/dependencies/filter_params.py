from http import HTTPStatus

from fastapi import HTTPException, Query

from app.docs.dependencies.custom_parameters import (
    CHAR_NAME_FILTER_DESCRIPTION,
    PAGE_NUMBER_DESCRIPTION,
    PER_PAGE_DESCRIPTION,
    get_description_and_values_table_for_property_group,
    get_description_and_values_table_for_unicode_age,
    get_filter_setting_description_general_category,
    get_filter_setting_description_script_code,
)
from app.schemas.enums import CharPropertyGroup, GeneralCategory, ScriptCode, UnicodeAge


class FilterParameters:
    def __init__(
        self,
        name: str | None = Query(default=None, description=CHAR_NAME_FILTER_DESCRIPTION),
        category: list[str] | None = Query(default=None, description=get_filter_setting_description_general_category()),
        age: list[str] | None = Query(default=None, description=get_description_and_values_table_for_unicode_age()),
        script: list[str] | None = Query(default=None, description=get_filter_setting_description_script_code()),
        show_props: list[str]
        | None = Query(default=None, description=get_description_and_values_table_for_property_group()),
        per_page: int | None = Query(default=None, ge=1, le=100, description=PER_PAGE_DESCRIPTION),
        page: int | None = Query(default=None, ge=1, description=PAGE_NUMBER_DESCRIPTION),
    ):
        self.name = name
        self.categories = parse_enum_values_from_parameter(GeneralCategory, "category", category) if category else None
        self.age_list = parse_enum_values_from_parameter(UnicodeAge, "age", age) if age else None
        self.scripts = parse_enum_values_from_parameter(ScriptCode, "script", script) if script else None
        self.show_props = (
            parse_enum_values_from_parameter(CharPropertyGroup, "show_props", show_props) if show_props else None
        )
        self.per_page = per_page or 10
        self.page = page or 1


def parse_enum_values_from_parameter(enum_class, param_name: str, values: list[str]):
    results = {str_val: enum_class.match_loosely(str_val) for str_val in values}
    invalid_results = [str_val for str_val, did_parse in results.items() if not did_parse]
    if invalid_results:
        needs_plural = len(invalid_results) > 1
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail=(
                f'{len(invalid_results)} value{"s" if needs_plural else ""} provided for the {param_name!r} '
                f'parameter {"are" if needs_plural else "is"} invalid: {invalid_results}'
            ),
        )
    return list(results.values())
