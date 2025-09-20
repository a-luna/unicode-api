import textwrap
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Annotated, Any, cast

from fastapi import Query

import unicode_api.db.models as db
from unicode_api.api.api_v1.dependencies.filter_param_matcher import (
    CharacterFlagParameterMatcher,
    CharacterPropGroupParameterMatcher,
    DatabaseFilterParameterMatcher,
)
from unicode_api.core.cache import cached_data
from unicode_api.core.util import s
from unicode_api.docs.dependencies.custom_parameters import (
    CHAR_NAME_FILTER_DESCRIPTION,
    CJK_DEFINITION_FILTER_DESCRIPTION,
    PAGE_NUMBER_DESCRIPTION,
    PER_PAGE_DESCRIPTION,
    VERBOSE_DESCRIPTION,
    get_filter_param_description,
)
from unicode_api.models.util import flatten_list2d


@dataclass
class FilterParameters:
    form_inputs: db.UserFilterSettings = field(repr=False)
    no_settings_provided: bool = field(init=False, default=False)
    name: str | None = field(init=False, default=None)
    cjk_definition: str | None = field(init=False, default=None)
    blocks: list[int] | None = field(init=False, default=None)
    categories: list[int] | None = field(init=False, default=None)
    categories_selected: list[int] | None = field(init=False, default=None)
    age_list: list[int] | None = field(init=False, default=None)
    scripts: tuple[list[str], list[int]] | None = field(init=False, default=None)
    script_names: list[str] | None = field(init=False, default=None)
    script_ids: list[int] | None = field(init=False, default=None)
    bidi_class_list: list[int] | None = field(init=False, default=None)
    decomp_types: list[int] | None = field(init=False, default=None)
    line_break_types: list[int] | None = field(init=False, default=None)
    ccc_list: list[int] | None = field(init=False, default=None)
    num_types: list[int] | None = field(init=False, default=None)
    join_types: list[int] | None = field(init=False, default=None)
    flags: list[db.CharacterFilterFlag] | None = field(init=False, default=None)
    show_prop_list: list[db.CharPropertyGroup] | None = field(init=False, default=None)
    parsed_settings: dict[str, Any] = field(init=False, default_factory=dict[str, Any])
    errors: list[str] = field(init=False, default_factory=list[str])

    def __str__(self) -> str:  # pragma: no cover
        return self.__repr__()

    def __post_init__(self):
        self.no_settings_provided = True

        self._parse_name()
        self._parse_cjk_definition()
        self._parse_block()
        self._parse_category()
        self._parse_age()
        self._parse_script()
        self._parse_bidi_class()
        self._parse_decomp_type()
        self._parse_line_break()
        self._parse_ccc()
        self._parse_num_type()
        self._parse_join_type()
        self._parse_flags()
        self._parse_show_props()

    def _parse_name(self):
        if self.form_inputs.name:
            self.name = self.form_inputs.name
            self.no_settings_provided = False

    def _parse_cjk_definition(self):
        if self.form_inputs.cjk_definition:
            self.cjk_definition = self.form_inputs.cjk_definition
            self.no_settings_provided = False

    def _parse_block(self):
        if self.form_inputs.block:
            param_matcher = DatabaseFilterParameterMatcher("Block", "block", db.UnicodeBlock)
            result = param_matcher.parse_filter_params(self.form_inputs.block)
            if result.success and result.value:
                self.blocks = [b.id for b in result.value if b.id]
                self.no_settings_provided = False
            else:
                self.errors.append(result.error)

    def _parse_category(self):
        if self.form_inputs.category:
            param_matcher = DatabaseFilterParameterMatcher("General_Category", "category", db.General_Category)
            result = param_matcher.parse_filter_params(self.form_inputs.category)
            if result.success and result.value:
                self.categories_selected = [c.id for c in result.value if c.id]
                filter_cats = list(set(flatten_list2d([c.category_values for c in result.value])))
                self.categories = sorted(
                    result.value
                    for result in cached_data.get_property_value_ids_by_name("General_Category", filter_cats)
                    if result.value
                )
                self.no_settings_provided = False
            else:
                self.errors.append(result.error)

    def _parse_age(self):
        if self.form_inputs.age:
            param_matcher = DatabaseFilterParameterMatcher("Age", "age", db.Age)
            result = param_matcher.parse_filter_params(self.form_inputs.age)
            if result.success and result.value:
                self.age_list = [a.id for a in result.value if a.id]
                self.no_settings_provided = False
            else:
                self.errors.append(result.error)

    def _parse_script(self):
        if self.form_inputs.script:
            param_matcher = DatabaseFilterParameterMatcher("Script", "script", db.Script)
            result = param_matcher.parse_filter_params(self.form_inputs.script)
            if result.success and result.value:
                self.scripts = ([s.short_name for s in result.value if s.id], [s.id for s in result.value if s.id])
                self.script_names = [s.short_name for s in result.value if s.id]
                self.script_ids = [s.id for s in result.value if s.id]
                self.no_settings_provided = False
            else:
                self.errors.append(result.error)

    def _parse_bidi_class(self):
        if self.form_inputs.bidi_class:
            param_matcher = DatabaseFilterParameterMatcher("Bidi_Class", "bidi_class", db.Bidi_Class)
            result = param_matcher.parse_filter_params(self.form_inputs.bidi_class)
            if result.success and result.value:
                self.bidi_class_list = [bdc.id for bdc in result.value if bdc.id]
                self.no_settings_provided = False
            else:
                self.errors.append(result.error)

    def _parse_decomp_type(self):
        if self.form_inputs.decomp_type:
            param_matcher = DatabaseFilterParameterMatcher("Decomposition_Type", "decomp_type", db.Decomposition_Type)
            result = param_matcher.parse_filter_params(self.form_inputs.decomp_type)
            if result.success and result.value:
                self.decomp_types = [dtype.id for dtype in result.value if dtype.id]
                self.no_settings_provided = False
            else:
                self.errors.append(result.error)

    def _parse_line_break(self):
        if self.form_inputs.line_break:
            param_matcher = DatabaseFilterParameterMatcher("Line_Break", "line_break", db.Line_Break)
            result = param_matcher.parse_filter_params(self.form_inputs.line_break)
            if result.success and result.value:
                self.line_break_types = [lb.id for lb in result.value if lb.id]
                self.no_settings_provided = False
            else:
                self.errors.append(result.error)

    def _parse_ccc(self):
        if self.form_inputs.ccc:
            param_matcher = DatabaseFilterParameterMatcher(
                "Canonical_Combining_Class", "ccc", db.Canonical_Combining_Class
            )
            result = param_matcher.parse_filter_params(self.form_inputs.ccc)
            if result.success and result.value:
                self.ccc_list = [c.id for c in result.value if c.id]
                self.no_settings_provided = False
            else:
                self.errors.append(result.error)

    def _parse_num_type(self):
        if self.form_inputs.num_type:
            param_matcher = DatabaseFilterParameterMatcher("Numeric_Type", "num_type", db.Numeric_Type)
            result = param_matcher.parse_filter_params(self.form_inputs.num_type)
            if result.success and result.value:
                self.num_types = [num_type.id for num_type in result.value if num_type.id]
                self.no_settings_provided = False
            else:
                self.errors.append(result.error)

    def _parse_join_type(self):
        if self.form_inputs.join_type:
            param_matcher = DatabaseFilterParameterMatcher("Joining_Type", "join_type", db.Joining_Type)
            result = param_matcher.parse_filter_params(self.form_inputs.join_type)
            if result.success and result.value:
                self.join_types = [jtype.id for jtype in result.value if jtype.id]
                self.no_settings_provided = False
            else:
                self.errors.append(result.error)

    def _parse_flags(self):
        if self.form_inputs.flag:
            param_matcher = CharacterFlagParameterMatcher("flag")
            result = param_matcher.parse_filter_params(self.form_inputs.flag)
            if result.success and result.value:
                self.flags = result.value
                self.no_settings_provided = False
            else:
                self.errors.append(result.error)

    def _parse_show_props(self):
        if self.form_inputs.show_props:
            param_matcher = CharacterPropGroupParameterMatcher("show_props")
            result = param_matcher.parse_filter_params(self.form_inputs.show_props)
            if result.success and result.value:
                self.show_prop_list = result.value
            else:
                self.errors.append(result.error)

    @property
    def did_parse(self) -> bool:
        return not bool(self.errors)

    @property
    def error_message(self) -> str:
        if self.did_parse:  # pragma: no cover
            return ""
        all_errors = f"Invalid values were provided for the following {len(self.errors)} parameter{s(self.errors)}:\n\n"
        all_errors += "\n\n".join(self.errors)
        return all_errors

    @property
    def parsed(self) -> db.UserFilterSettings:
        get_prop_value = cached_data.get_display_name_for_property_value

        self.parsed_settings = {}
        self._add_to_filter_settings("name", self.name)
        self._add_to_filter_settings("cjk_definition", self.cjk_definition)
        self._add_to_filter_settings("block", self.blocks, lambda x: cached_data.get_unicode_block_by_id(x).long_name)
        self._add_to_filter_settings(
            "category", self.categories_selected, lambda x: get_prop_value("General_Category", x)
        )
        self._add_to_filter_settings("age", self.age_list, lambda x: get_prop_value("Age", x))
        self._add_to_filter_settings(
            "script", self.script_ids if self.scripts else None, lambda x: get_prop_value("Script", x)
        )
        self._add_to_filter_settings("bidi_class", self.bidi_class_list, lambda x: get_prop_value("Bidi_Class", x))
        self._add_to_filter_settings(
            "decomp_type", self.decomp_types, lambda x: get_prop_value("Decomposition_Type", x)
        )
        self._add_to_filter_settings("line_break", self.line_break_types, lambda x: get_prop_value("Line_Break", x))
        self._add_to_filter_settings("ccc", self.ccc_list, lambda x: get_prop_value("Canonical_Combining_Class", x))
        self._add_to_filter_settings("num_type", self.num_types, lambda x: get_prop_value("Numeric_Type", x))
        self._add_to_filter_settings("join_type", self.join_types, lambda x: get_prop_value("Joining_Type", x))
        self._add_to_filter_settings("flag", self.flags, lambda x: x.display_name.replace("_", " "))
        self._add_to_filter_settings(
            "show_props", self.show_prop_list, lambda x: str(x), default=[str(db.CharPropertyGroup.MINIMUM)]
        )

        validated = db.UserFilterSettings.model_validate(self.parsed_settings)
        return validated

    def _add_to_filter_settings(
        self, setting: str, value: Any, transform: Callable[[Any], Any] = lambda x: x, default: Any = None
    ):
        if value:
            match value:
                case list() | tuple():
                    self.parsed_settings[setting] = [transform(v) for v in cast(list[Any] | tuple[Any], value)]
                case _:
                    self.parsed_settings[setting] = transform(value)
        elif default is not None:
            self.parsed_settings[setting] = default


class FilterSettings:
    def __init__(
        self,
        name: Annotated[str, Query(description=CHAR_NAME_FILTER_DESCRIPTION)] = "",
        cjk_definition: Annotated[str, Query(description=CJK_DEFINITION_FILTER_DESCRIPTION)] = "",
        block: Annotated[list[str], Query(description=get_filter_param_description("block"))] = None,  # type: ignore[reportArgumentType]
        category: Annotated[list[str], Query(description=get_filter_param_description("category"))] = None,  # type: ignore[reportArgumentType]
        age: Annotated[list[str], Query(description=get_filter_param_description("age"))] = None,  # type: ignore[reportArgumentType]
        script: Annotated[list[str], Query(description=get_filter_param_description("script"))] = None,  # type: ignore[reportArgumentType]
        bidi_class: Annotated[list[str], Query(description=get_filter_param_description("bidi_class"))] = None,  # type: ignore[reportArgumentType]
        decomp_type: Annotated[list[str], Query(description=get_filter_param_description("decomp_type"))] = None,  # type: ignore[reportArgumentType]
        line_break: Annotated[list[str], Query(description=get_filter_param_description("line_break"))] = None,  # type: ignore[reportArgumentType]
        ccc: Annotated[list[str], Query(description=get_filter_param_description("ccc"))] = None,  # type: ignore[reportArgumentType]
        num_type: Annotated[list[str], Query(description=get_filter_param_description("num_type"))] = None,  # type: ignore[reportArgumentType]
        join_type: Annotated[list[str], Query(description=get_filter_param_description("join_type"))] = None,  # type: ignore[reportArgumentType]
        flag: Annotated[list[str], Query(description=get_filter_param_description("flag"))] = None,  # type: ignore[reportArgumentType]
        show_props: Annotated[list[str], Query(description=get_filter_param_description("show_props"))] = None,  # type: ignore[reportArgumentType]
        verbose: Annotated[bool | None, Query(description=VERBOSE_DESCRIPTION)] = None,
        per_page: Annotated[int | None, Query(ge=1, le=100, description=PER_PAGE_DESCRIPTION)] = None,
        page: Annotated[int | None, Query(ge=1, description=PAGE_NUMBER_DESCRIPTION)] = None,
    ):
        form_inputs = db.UserFilterSettings(
            name=name,
            cjk_definition=cjk_definition,
            block=block,
            category=category,
            age=age,
            script=script,
            bidi_class=bidi_class,
            decomp_type=decomp_type,
            line_break=line_break,
            ccc=ccc,
            num_type=num_type,
            join_type=join_type,
            flag=flag,
            show_props=show_props,
        )
        self.params = FilterParameters(form_inputs)
        self.verbose = verbose or False
        self.per_page = per_page or 10
        self.page = page or 1

    def __repr__(self) -> str:
        s = f"""
        FilterSettings(
            no_settings_provided={self.no_settings_provided},
            did_parse={self.did_parse},
            parsed={self.params},
            verbose={self.verbose},
            per_page={self.per_page},
            page={self.page},
            error_message={self.error_message},
        )
        """
        return textwrap.dedent(s)

    @property
    def no_settings_provided(self) -> bool:
        return self.params.no_settings_provided

    @property
    def did_parse(self) -> bool:
        return self.params.did_parse

    @property
    def error_message(self) -> str | None:
        return self.params.error_message if not self.did_parse else None

    @property
    def parsed(self) -> db.UserFilterSettings:
        return self.params.parsed

    @property
    def show_props(self) -> list[db.CharPropertyGroup]:
        return self.params.show_prop_list or []
