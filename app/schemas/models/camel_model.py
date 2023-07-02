from pydantic.generics import GenericModel
from sqlmodel import SQLModel

from app.schemas.util import to_lower_camel


class CamelModel(SQLModel):
    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class GenericCamelModel(GenericModel):
    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True
