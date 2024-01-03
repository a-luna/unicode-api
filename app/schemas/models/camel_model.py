from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from sqlmodel import SQLModel

from app.schemas.util import to_lower_camel

T = TypeVar("T")


class CamelModel(SQLModel):
    model_config = ConfigDict(alias_generator=to_lower_camel, populate_by_name=True)


class GenericCamelModel(BaseModel, Generic[T]):
    model_config = ConfigDict(alias_generator=to_lower_camel, populate_by_name=True)
