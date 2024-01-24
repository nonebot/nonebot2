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


__all__ = (
    "Required",
    "PydanticUndefined",
    "PydanticUndefinedType",
    "ConfigDict",
    "FieldInfo",
    "ModelField",
    "extract_field_info",
    "model_fields",
    "model_config",
    "type_validate_python",
    "custom_validation",
)


if PYDANTIC_V2:  # pragma: pydantic-v2
    from pydantic_core import CoreSchema, core_schema
    from pydantic._internal._repr import display_as_type
    from pydantic import TypeAdapter, GetCoreSchemaHandler
    from pydantic.fields import FieldInfo as BaseFieldInfo

    Required = Ellipsis
    """Alias of Ellipsis for compatibility with pydantic v1"""

    # Export undefined type
    from pydantic_core import PydanticUndefined as PydanticUndefined
    from pydantic_core import PydanticUndefinedType as PydanticUndefinedType

    # isort: split

    # Export model config dict
    from pydantic import ConfigDict as ConfigDict

    class FieldInfo(BaseFieldInfo):
        """FieldInfo class with extra property for compatibility with pydantic v1"""

        # make default can be positional argument
        def __init__(self, default: Any = PydanticUndefined, **kwargs: Any) -> None:
            super().__init__(default=default, **kwargs)

        @property
        def extra(self) -> Dict[str, Any]:
            """Extra data that is not part of the standard pydantic fields.

            For compatibility with pydantic v1.
            """
            # extract extra data from attributes set except used slots
            return {
                k: v
                for k, v in self._attributes_set.items()
                if k not in super().__slots__
            }

    @dataclass
    class ModelField:
        """ModelField class for compatibility with pydantic v1"""

        name: str
        """The name of the field."""
        annotation: Any
        """The annotation of the field."""
        field_info: FieldInfo
        """The FieldInfo of the field."""

        def _annotation_has_config(self) -> bool:
            """Check if the annotation has config.

            TypeAdapter raise error when annotation has config
            and given config is not None.
            """
            try:
                return (
                    issubclass(self.annotation, BaseModel)
                    or is_dataclass(self.annotation)
                    or is_typeddict(self.annotation)
                )
            except TypeError:
                return False

        def get_default(self) -> Any:
            """Get the default value of the field."""
            return self.field_info.get_default(call_default_factory=True)

        def validate(self, value: Any, config: Optional[ConfigDict] = None) -> Any:
            """Validate the value pass to the field."""
            type: Any = Annotated[self.annotation, self.field_info]
            return TypeAdapter(
                type, config=None if self._annotation_has_config() else config
            ).validate_python(value)

        def _type_display(self):
            """Get the display of the type of the field."""
            return display_as_type(self.annotation)

        def __hash__(self) -> int:
            # Each ModelField is unique for our purposes,
            # to allow store them in a set.
            return id(self)

    def extract_field_info(field_info: BaseFieldInfo) -> Dict[str, Any]:
        """Get FieldInfo init kwargs from a FieldInfo instance."""

        kwargs = field_info._attributes_set.copy()
        kwargs["annotation"] = field_info.rebuild_annotation()
        return kwargs

    def model_fields(model: Type[BaseModel]) -> List[ModelField]:
        """Get field list of a model."""

        return [
            ModelField(
                name=name,
                annotation=field_info.rebuild_annotation(),
                field_info=FieldInfo(**extract_field_info(field_info)),
            )
            for name, field_info in model.model_fields.items()
        ]

    def model_config(model: Type[BaseModel]) -> Any:
        """Get config of a model."""
        return model.model_config

    def type_validate_python(type_: Type[T], data: Any) -> T:
        """Validate data with given type."""
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
    from pydantic import BaseConfig as PydanticConfig
    from pydantic.fields import FieldInfo as BaseFieldInfo
    from pydantic.fields import ModelField as BaseModelField
    from pydantic.schema import get_annotation_from_field_info

    # isort: split

    from pydantic.fields import Required as Required

    # isort: split

    from pydantic.fields import Undefined as PydanticUndefined
    from pydantic.fields import UndefinedType as PydanticUndefinedType

    class ConfigDict(PydanticConfig):
        """Config class that allow get value with default value."""

        @classmethod
        def get(cls, field: str, default: Any = None) -> Any:
            """Get a config value."""
            return getattr(cls, field, default)

    class FieldInfo(BaseFieldInfo):
        def __init__(self, default: Any = PydanticUndefined, **kwargs: Any):
            # preprocess default value to make it compatible with pydantic v2
            # when default is Required, set it to PydanticUndefined
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
            """Validate the value pass to the field.

            Set config before validate to ensure validate correctly.
            """

            if self.model_config is not config:
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
        """Get field list of a model."""

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
        """Get config of a model."""
        return model.__config__

    def type_validate_python(type_: Type[T], data: Any) -> T:
        """Validate data with given type."""
        return parse_obj_as(type_, data)

    def custom_validation(class_: Type["CVC"]) -> Type["CVC"]:
        """Do nothing in pydantic v1"""
        return class_
