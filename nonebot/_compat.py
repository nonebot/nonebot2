from dataclasses import dataclass
from typing import Any, Dict, Type, TypeVar

from pydantic.fields import FieldInfo
from pydantic import VERSION, BaseModel

T = TypeVar("T")

PYDANTIC_V2 = int(VERSION.split(".", 1)[0]) == 2


if PYDANTIC_V2:
    from pydantic import TypeAdapter
    from pydantic import ConfigDict as BaseConfig

    @dataclass
    class ModelField:
        name: str
        field_info: FieldInfo

    def model_fields(model: Type[BaseModel]) -> Dict[str, ModelField]:
        return {
            name: ModelField(name=name, field_info=field_info)
            for name, field_info in model.model_fields.items()
        }

    def type_validate_python(type_: Type[T], data: Any) -> T:
        return TypeAdapter(type_).validate_python(data)

else:
    from pydantic import parse_obj_as
    from pydantic import BaseConfig as BaseConfig
    from pydantic.fields import ModelField as ModelField

    def model_fields(model: Type[BaseModel]) -> Dict[str, ModelField]:
        return model.__fields__

    def type_validate_python(type_: Type[T], data: Any) -> T:
        return parse_obj_as(type_, data)
