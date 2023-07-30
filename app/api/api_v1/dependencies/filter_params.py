from http import HTTPStatus
from typing import Annotated, Generic, Type, TypeVar

from fastapi import HTTPException, Query

from app.core.result import Result
from app.data.cache import cached_data
from app.docs.dependencies.custom_parameters import (
    CHAR_NAME_FILTER_DESCRIPTION,
    PAGE_NUMBER_DESCRIPTION,
    PER_PAGE_DESCRIPTION,
    VERBOSE_DESCRIPTION,
    get_filter_param_description,
)
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
        name: Annotated[str | None, Query(description=CHAR_NAME_FILTER_DESCRIPTION)] = None,
        block: Annotated[list[str] | None, Query(description=get_filter_param_description("block"))] = None,
        category: Annotated[list[str] | None, Query(description=get_filter_param_description("category"))] = None,
        age: Annotated[list[str] | None, Query(description=get_filter_param_description("age"))] = None,
        script: Annotated[list[str] | None, Query(description=get_filter_param_description("script"))] = None,
        bidi_class: Annotated[list[str] | None, Query(description=get_filter_param_description("bidi_class"))] = None,
        decomp_type: Annotated[list[str] | None, Query(description=get_filter_param_description("decomp_type"))] = None,
        line_break: Annotated[list[str] | None, Query(description=get_filter_param_description("line_break"))] = None,
        ccc: Annotated[list[str] | None, Query(description=get_filter_param_description("ccc"))] = None,
        num_type: Annotated[list[str] | None, Query(description=get_filter_param_description("num_type"))] = None,
        join_type: Annotated[list[str] | None, Query(description=get_filter_param_description("join_type"))] = None,
        flag: Annotated[list[str] | None, Query(description=get_filter_param_description("flag"))] = None,
        show_props: Annotated[list[str] | None, Query(description=get_filter_param_description("show_props"))] = None,
        verbose: Annotated[bool | None, Query(description=VERBOSE_DESCRIPTION)] = None,
        per_page: Annotated[int | None, Query(ge=1, le=100, description=PER_PAGE_DESCRIPTION)] = None,
        page: Annotated[int | None, Query(ge=1, description=PAGE_NUMBER_DESCRIPTION)] = None,
    ):
        self.parse_all_enum_values(
            block,
            category,
            age,
            script,
            bidi_class,
            decomp_type,
            line_break,
            ccc,
            num_type,
            join_type,
            flag,
            show_props,
        )
        self.verbose = verbose or False
        self.name = name
        self.per_page = per_page or 10
        self.page = page or 1

    @property
    def settings(self) -> list[str]:
        filter_settings = []
        if self.blocks:
            block_names = [cached_data.get_unicode_block_by_id(block_id).name for block_id in self.blocks]
            filter_settings.append(f"block: {', '.join(block_names)}")

        if self.categories:
            categories = [str(cat) for cat in self.categories]
            filter_settings.append(f"category: {', '.join(categories)}")

        if self.age_list:
            filter_settings.append(f"version: {', '.join(self.age_list)}")

        if self.scripts:
            scripts = [str(script) for script in self.scripts]
            filter_settings.append(f"script: {', '.join(scripts)}")

        if self.bidi_class_list:
            bidi_class_list = [str(bidi_class) for bidi_class in self.bidi_class_list]
            filter_settings.append(f"bidi_class: {', '.join(bidi_class_list)}")

        if self.decomp_types:
            decomp_types = [str(decomp) for decomp in self.decomp_types]
            filter_settings.append(f"decomp_type: {', '.join(decomp_types)}")

        if self.line_break_types:
            line_break_types = [str(lb) for lb in self.line_break_types]
            filter_settings.append(f"line_break: {', '.join(line_break_types)}")

        if self.ccc_list:
            ccc_list = [str(ccc) for ccc in self.ccc_list]
            filter_settings.append(f"ccc: {', '.join(ccc_list)}")

        if self.num_types:
            num_types = [str(num_type) for num_type in self.num_types]
            filter_settings.append(f"num_type: {', '.join(num_types)}")

        if self.join_types:
            join_types = [str(join_type) for join_type in self.join_types]
            filter_settings.append(f"join_type: {', '.join(join_types)}")

        if self.flags:
            flags = [flag.display_name.replace("_", " ") for flag in self.flags]
            filter_settings.append(f"flag: {', '.join(flags)}")

        return filter_settings

    def parse_all_enum_values(
        self,
        block: list[str] | None,
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
        self.blocks: list[int] | None = None
        self.categories: list[GeneralCategory] | None = None
        self.age_list: list[str] | None = None
        self.scripts: list[ScriptCode] | None = None
        self.bidi_class_list: list[BidirectionalClass] | None = None
        self.decomp_types: list[DecompositionType] | None = None
        self.line_break_types: list[LineBreakType] | None = None
        self.ccc_list: list[CombiningClassCategory] | None = None
        self.num_types: list[NumericType] | None = None
        self.join_types: list[JoiningType] | None = None
        self.flags: list[CharacterFilterFlags] | None = None
        self.show_props: list[CharPropertyGroup] | None = None

        if block:
            UnicodeBlockNameMatcher = FilterParameterMatcher[UnicodeBlockName]("block", UnicodeBlockName)
            result = UnicodeBlockNameMatcher.parse_enum_values(block)
            if result.success:
                self.blocks = result.value
            else:
                errors.append(result.error or "")

        if category:
            GeneralCategoryMatcher = FilterParameterMatcher[GeneralCategory]("category", GeneralCategory)
            result = GeneralCategoryMatcher.parse_enum_values(category)
            if result.success:
                self.categories = result.value
            else:
                errors.append(result.error or "")

        if age:
            UnicodeAgeMatcher = FilterParameterMatcher[UnicodeAge]("age", UnicodeAge)
            result = UnicodeAgeMatcher.parse_enum_values(age)
            if result.success:
                self.age_list = result.value
            else:
                errors.append(result.error or "")

        if script:
            ScriptCodeMatcher = FilterParameterMatcher[ScriptCode]("script", ScriptCode)
            result = ScriptCodeMatcher.parse_enum_values(script)
            if result.success:
                self.scripts = result.value
            else:
                errors.append(result.error or "")

        if bidi_class:
            BidiClassMatcher = FilterParameterMatcher[BidirectionalClass]("bidi_class", BidirectionalClass)
            result = BidiClassMatcher.parse_enum_values(bidi_class)
            if result.success:
                self.bidi_class_list = result.value
            else:
                errors.append(result.error or "")

        if decomp_type:
            DecompTypeMatcher = FilterParameterMatcher[DecompositionType]("decomp_type", DecompositionType)
            result = DecompTypeMatcher.parse_enum_values(decomp_type)
            if result.success:
                self.decomp_types = result.value
            else:
                errors.append(result.error or "")

        if line_break:
            LineBreakMatcher = FilterParameterMatcher[LineBreakType]("line_break", LineBreakType)
            result = LineBreakMatcher.parse_enum_values(line_break)
            if result.success:
                self.line_break_types = result.value
            else:
                errors.append(result.error or "")

        if ccc:
            CombiningClassMatcher = FilterParameterMatcher[CombiningClassCategory]("ccc", CombiningClassCategory)
            result = CombiningClassMatcher.parse_enum_values(ccc)
            if result.success:
                self.ccc_list = result.value
            else:
                errors.append(result.error or "")

        if num_type:
            NumericTypeMatcher = FilterParameterMatcher[NumericType]("num_type", NumericType)
            result = NumericTypeMatcher.parse_enum_values(num_type)
            if result.success:
                self.num_types = result.value
            else:
                errors.append(result.error or "")

        if join_type:
            JoiningTypeMatcher = FilterParameterMatcher[JoiningType]("join_type", JoiningType)
            result = JoiningTypeMatcher.parse_enum_values(join_type)
            if result.success:
                self.join_types = result.value
            else:
                errors.append(result.error or "")

        if flag:
            CharFilterFlagMatcher = FilterParameterMatcher[CharacterFilterFlags]("flag", CharacterFilterFlags)
            result = CharFilterFlagMatcher.parse_enum_values(flag)
            if result.success:
                self.flags = result.value
            else:
                errors.append(result.error or "")

        if show_props:
            PropertyGroupMatcher = FilterParameterMatcher[CharPropertyGroup]("show_props", CharPropertyGroup)
            result = PropertyGroupMatcher.parse_enum_values(show_props)
            if result.success:
                self.show_props = result.value
            else:
                errors.append(result.error or "")

        if errors:
            all_errors = f"Invalid values were provided for the following {len(errors)} parameters:\n\n"
            all_errors += "\n\n".join(errors)
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=all_errors)
