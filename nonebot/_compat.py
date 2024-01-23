from dataclasses import dataclass, is_dataclass
from typing_extensions import Annotated, is_typeddict
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Type,
    TypeVar,
    Callable,
    Optional,
    Protocol,
    Generator,
)

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
    from pydantic_core import CoreSchema
    from pydantic_core import core_schema
    from pydantic import ConfigDict as ConfigDict
    from pydantic._internal._repr import display_as_type
    from pydantic import TypeAdapter, GetCoreSchemaHandler
    from pydantic.fields import FieldInfo as BaseFieldInfo
    from pydantic_core import PydanticUndefined as PydanticUndefined
    from pydantic_core import PydanticUndefinedType as PydanticUndefinedType

    Required = Ellipsis

    class FieldInfo(BaseFieldInfo):
        # make default can be positional argument
        def __init__(self, default: Any = PydanticUndefined, **kwargs: Any) -> None:
            super().__init__(default=default, **kwargs)

        @property
        def extra(self) -> Dict[str, Any]:
            """Extra data that is not part of the standard pydantic fields.

            For compatibility with pydantic v1.
            """
            return {
                k: v
                for k, v in self._attributes_set.items()
                if k not in super().__slots__
            }

    @dataclass
    class ModelField:
        name: str
        annotation: Any
        field_info: FieldInfo

        def _annotation_has_config(self) -> bool:
            try:
                return (
                    issubclass(self.annotation, BaseModel)
                    or is_dataclass(self.annotation)
                    or is_typeddict(self.annotation)
                )
            except TypeError:
                return False

        def get_default(self) -> Any:
            return self.field_info.get_default(call_default_factory=True)

        def validate(self, value: Any, config: Optional[ConfigDict] = None) -> Any:
            type: Any = Annotated[self.annotation, self.field_info]
            return TypeAdapter(
                type, config=None if self._annotation_has_config() else config
            ).validate_python(value)

        def _type_display(self):
            return display_as_type(self.annotation)

        def __hash__(self) -> int:
            return id(self)

    def extract_field_info(field_info: BaseFieldInfo) -> Dict[str, Any]:
        """Get FieldInfo init kwargs from a FieldInfo instance."""

        kwargs = field_info._attributes_set.copy()
        kwargs["annotation"] = field_info.rebuild_annotation()
        return kwargs

    def model_fields(model: Type[BaseModel]) -> List[ModelField]:
        return [
            ModelField(
                name=name,
                annotation=field_info.rebuild_annotation(),
                field_info=FieldInfo(**extract_field_info(field_info)),
            )
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
        """Use pydantic v1 like validator generator in pydantic v2"""

        setattr(
            class_,
            "__get_pydantic_core_schema__",
            classmethod(__get_pydantic_core_schema__),
        )
        return class_

else:  # pragma: pydantic-v1
    from pydantic import parse_obj_as
    from pydantic.fields import Required as Required
    from pydantic import BaseConfig as PydanticConfig
    from pydantic.fields import FieldInfo as BaseFieldInfo
    from pydantic.fields import ModelField as BaseModelField
    from pydantic.fields import Undefined as PydanticUndefined
    from pydantic.schema import get_annotation_from_field_info

    class ConfigDict(PydanticConfig):
        @classmethod
        def get(cls, field: str, default: Any = None) -> Any:
            """Get a config value."""
            return getattr(cls, field, default)

    class FieldInfo(BaseFieldInfo):
        def __init__(self, default: Any = PydanticUndefined, **kwargs: Any):
            # preprocess default value to make it compatible with pydantic v2
            if default is Required:
                default = PydanticUndefined
            super().__init__(self, default, **kwargs)

    class ModelField(BaseModelField):
        # rewrite init method to simplify the logic
        def __init__(self, name: str, annotation: Any, field_info: FieldInfo):
            super().__init__(
                name=name,
                type_=get_annotation_from_field_info(annotation, field_info, name),
                class_validators=None,
                model_config=ConfigDict,
                default=field_info.default,
                default_factory=field_info.default_factory,
                required=(
                    field_info.default is PydanticUndefined
                    and field_info.default_factory is None
                ),
                field_info=field_info,
            )

        def validate(
            self, value: Any, config: Optional[Type[ConfigDict]] = None
        ) -> Any:
            self.set_config(config or ConfigDict)
            v, errs_ = super().validate(value, {}, loc=())
            if errs_:
                raise ValueError(value, self)
            return v

    def extract_field_info(field_info: BaseFieldInfo) -> Dict[str, Any]:
        """Get FieldInfo init kwargs from a FieldInfo instance."""

        kwargs = {"annotation": getattr(field_info, "annotation", Any)}
        kwargs.update(
            (s, getattr(field_info, s)) for s in field_info.__slots__ if s != "extra"
        )
        kwargs.update(field_info.extra)
        return kwargs

    def model_fields(model: Type[BaseModel]) -> List[ModelField]:
        return [
            ModelField(
                name=model_field.name,
                field_info=FieldInfo(
                    **{
                        **extract_field_info(model_field.field_info),
                        "annotation": model_field.annotation,
                    },
                ),
            )
            for model_field in model.__fields__.values()
        ]

    def model_config(model: Type[BaseModel]) -> Any:
        return model.__config__

    def type_validate_python(type_: Type[T], data: Any) -> T:
        return parse_obj_as(type_, data)

    def custom_validation(class_: Type["CVC"]) -> Type["CVC"]:
        return class_
