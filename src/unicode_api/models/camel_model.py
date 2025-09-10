from typing import TypeVar

from pydantic import ConfigDict
from sqlmodel import SQLModel

from unicode_api.models.util import to_lower_camel

T = TypeVar("T")


class CamelModel(SQLModel):
    model_config = ConfigDict(alias_generator=to_lower_camel, populate_by_name=True)  # type: ignore[reportAssignmentType]
