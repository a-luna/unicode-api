from typing import Annotated

from fastapi import HTTPException, Query, status

from app.api.api_v1.dependencies.filter_param_matcher import filter_param_matcher
from app.core.cache import cached_data
from app.docs.dependencies.custom_parameters import (
    CHAR_NAME_FILTER_DESCRIPTION,
    CJK_DEFINITION_FILTER_DESCRIPTION,
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


class FilterParameters:
    def __init__(
        self,
        name: Annotated[str | None, Query(description=CHAR_NAME_FILTER_DESCRIPTION)] = None,
        cjk_definition: Annotated[str | None, Query(description=CJK_DEFINITION_FILTER_DESCRIPTION)] = None,
        block: Annotated[list[str], Query(description=get_filter_param_description("block"))] = None,
        category: Annotated[list[str], Query(description=get_filter_param_description("category"))] = None,
        age: Annotated[list[str], Query(description=get_filter_param_description("age"))] = None,
        script: Annotated[list[str], Query(description=get_filter_param_description("script"))] = None,
        bidi_class: Annotated[list[str], Query(description=get_filter_param_description("bidi_class"))] = None,
        decomp_type: Annotated[list[str], Query(description=get_filter_param_description("decomp_type"))] = None,
        line_break: Annotated[list[str], Query(description=get_filter_param_description("line_break"))] = None,
        ccc: Annotated[list[str], Query(description=get_filter_param_description("ccc"))] = None,
        num_type: Annotated[list[str], Query(description=get_filter_param_description("num_type"))] = None,
        join_type: Annotated[list[str], Query(description=get_filter_param_description("join_type"))] = None,
        flag: Annotated[list[str], Query(description=get_filter_param_description("flag"))] = None,
        show_props: Annotated[list[str], Query(description=get_filter_param_description("show_props"))] = None,
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
        self.cjk_definition = cjk_definition
        self.per_page = per_page or 10
        self.page = page or 1

    @property
    def settings(self) -> dict[str, str]:  # noqa: C901
        filter_settings = {}
        if self.name:
            filter_settings["name"] = self.name

        if self.cjk_definition:
            filter_settings["cjk_definition"] = self.cjk_definition

        if self.blocks:
            block_names = [cached_data.get_unicode_block_by_id(block_id).name for block_id in self.blocks]
            filter_settings["block"] = ", ".join(block_names)

        if self.categories:
            categories = [str(cat) for cat in self.categories]
            filter_settings["category"] = ", ".join(categories)

        if self.age_list:
            filter_settings["version"] = ", ".join(self.age_list)

        if self.scripts:
            scripts = [str(script) for script in self.scripts]
            filter_settings["script"] = ", ".join(scripts)

        if self.bidi_class_list:
            bidi_class_list = [str(bidi_class) for bidi_class in self.bidi_class_list]
            filter_settings["bidi_class"] = ", ".join(bidi_class_list)

        if self.decomp_types:
            decomp_types = [str(decomp) for decomp in self.decomp_types]
            filter_settings["decomp_type"] = ", ".join(decomp_types)

        if self.line_break_types:
            line_break_types = [str(lb) for lb in self.line_break_types]
            filter_settings["line_break"] = ", ".join(line_break_types)

        if self.ccc_list:
            ccc_list = [str(ccc) for ccc in self.ccc_list]
            filter_settings["ccc"] = ", ".join(ccc_list)

        if self.num_types:
            num_types = [str(num_type) for num_type in self.num_types]
            filter_settings["num_type"] = ", ".join(num_types)

        if self.join_types:
            join_types = [str(join_type) for join_type in self.join_types]
            filter_settings["join_type"] = ", ".join(join_types)

        if self.flags:
            flags = [flag.display_name.replace("_", " ") for flag in self.flags]
            filter_settings["flag"] = ", ".join(flags)

        if self.show_props:
            prop_groups = [str(prop) for prop in self.show_props]
            filter_settings["property_groups"] = ", ".join(prop_groups)

        return filter_settings

    def parse_all_enum_values(  # noqa: C901
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
            result = filter_param_matcher[UnicodeBlockName].parse_enum_values(block)
            if result.success:
                self.blocks = result.value
            else:
                errors.append(result.error or "")

        if category:
            result = filter_param_matcher[GeneralCategory].parse_enum_values(category)
            if result.success:
                self.categories = result.value
            else:
                errors.append(result.error or "")

        if age:
            result = filter_param_matcher[UnicodeAge].parse_enum_values(age)
            if result.success:
                self.age_list = result.value
            else:
                errors.append(result.error or "")

        if script:
            result = filter_param_matcher[ScriptCode].parse_enum_values(script)
            if result.success:
                self.scripts = result.value
            else:
                errors.append(result.error or "")

        if bidi_class:
            result = filter_param_matcher[BidirectionalClass].parse_enum_values(bidi_class)
            if result.success:
                self.bidi_class_list = result.value
            else:
                errors.append(result.error or "")

        if decomp_type:
            result = filter_param_matcher[DecompositionType].parse_enum_values(decomp_type)
            if result.success:
                self.decomp_types = result.value
            else:
                errors.append(result.error or "")

        if line_break:
            result = filter_param_matcher[LineBreakType].parse_enum_values(line_break)
            if result.success:
                self.line_break_types = result.value
            else:
                errors.append(result.error or "")

        if ccc:
            result = filter_param_matcher[CombiningClassCategory].parse_enum_values(ccc)
            if result.success:
                self.ccc_list = result.value
            else:
                errors.append(result.error or "")

        if num_type:
            result = filter_param_matcher[NumericType].parse_enum_values(num_type)
            if result.success:
                self.num_types = result.value
            else:
                errors.append(result.error or "")

        if join_type:
            result = filter_param_matcher[JoiningType].parse_enum_values(join_type)
            if result.success:
                self.join_types = result.value
            else:
                errors.append(result.error or "")

        if flag:
            result = filter_param_matcher[CharacterFilterFlags].parse_enum_values(flag)
            if result.success:
                self.flags = result.value
            else:
                errors.append(result.error or "")

        if show_props:
            result = filter_param_matcher[CharPropertyGroup].parse_enum_values(show_props)
            if result.success:
                self.show_props = result.value
            else:
                errors.append(result.error or "")

        if errors:
            all_errors = f"Invalid values were provided for the following {len(errors)} parameters:\n\n"
            all_errors += "\n\n".join(errors)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=all_errors)
