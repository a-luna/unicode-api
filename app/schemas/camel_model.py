from humps import camelize
from pydantic.generics import GenericModel
from sqlmodel import SQLModel


def to_camel(string):
    return camelize(string)


class CamelModel(SQLModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class GenericCamelModel(GenericModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
