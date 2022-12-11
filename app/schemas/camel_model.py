from humps import camelize
from pydantic import BaseModel
from pydantic.generics import GenericModel


def to_camel(string):
    return camelize(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class GenericCamelModel(GenericModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
