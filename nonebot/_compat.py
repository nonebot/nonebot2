from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Type,
    TypeVar,
    Callable,
    Protocol,
    Generator,
)

from pydantic.fields import FieldInfo
from pydantic import VERSION, BaseModel

T = TypeVar("T")

PYDANTIC_V2 = int(VERSION.split(".", 1)[0]) == 2

if TYPE_CHECKING:

    class ModelBeforeValidator(Protocol):
        def __call__(self, cls: Any, __value: Any) -> Any:
            ...

    class CustomValidationClass(Protocol):
        @classmethod
        def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
            ...

    CVC = TypeVar("CVC", bound=CustomValidationClass)


if PYDANTIC_V2:  # pragma: pydantic-v2
    from pydantic import ConfigDict as BaseConfig
    from pydantic_core import CoreSchema, core_schema
    from pydantic import TypeAdapter, GetCoreSchemaHandler

    @dataclass
    class ModelField:
        name: str
        field_info: FieldInfo

        @property
        def annotation(self) -> Any:
            return self.field_info.annotation

    def model_fields(model: Type[BaseModel]) -> List[ModelField]:
        return [
            ModelField(name=name, field_info=field_info)
            for name, field_info in model.model_fields.items()
        ]

    def model_config(model: Type[BaseModel]) -> Any:
        return model.model_config

    def type_validate_python(type_: Type[T], data: Any) -> T:
        return TypeAdapter(type_).validate_python(data)

    def __get_pydantic_core_schema__(
        cls: Type["CustomValidationClass"],
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        validators = list(cls.__get_validators__())
        if len(validators) == 1:
            return core_schema.no_info_plain_validator_function(validators[0])
        return core_schema.chain_schema(
            [core_schema.no_info_plain_validator_function(func) for func in validators]
        )

    def custom_validation(class_: Type["CVC"]) -> Type["CVC"]:
        setattr(
            class_,
            "__get_pydantic_core_schema__",
            classmethod(__get_pydantic_core_schema__),
        )
        return class_

else:  # pragma: pydantic-v1
    from pydantic import parse_obj_as
    from pydantic import BaseConfig as PydanticConfig
    from pydantic.fields import ModelField as ModelField

    class BaseConfig(PydanticConfig):
        @classmethod
        def get(cls, field: str, default: Any = None) -> Any:
            return getattr(cls, field, default)

    def model_fields(model: Type[BaseModel]) -> List[ModelField]:
        return list(model.__fields__.values())

    def model_config(model: Type[BaseModel]) -> Any:
        return model.__config__

    def type_validate_python(type_: Type[T], data: Any) -> T:
        return parse_obj_as(type_, data)

    def custom_validation(class_: Type["CVC"]) -> Type["CVC"]:
        return class_
