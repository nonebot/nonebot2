import inspect
from typing import Any, Dict, Type, Union, Callable, Optional, ForwardRef

from pydantic import BaseConfig
from pydantic.class_validators import Validator
from pydantic.typing import evaluate_forwardref
from pydantic.schema import get_annotation_from_field_info
from pydantic.fields import Required, FieldInfo, ModelField, UndefinedType

from .models import Param, Depends, Dependent, ParamTypes, SimpleParam


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        ) for param in signature.parameters.values()
    ]
    typed_signature = inspect.Signature(typed_params)
    return typed_signature


def get_typed_annotation(param: inspect.Parameter, globalns: Dict[str,
                                                                  Any]) -> Any:
    annotation = param.annotation
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        annotation = evaluate_forwardref(annotation, globalns, globalns)
    return annotation


def get_param_sub_dependent(*, param: inspect.Parameter) -> Dependent:
    depends: Depends = param.default
    if depends.dependency:
        dependency = depends.dependency
    else:
        dependency = param.annotation
    return get_sub_dependant(
        depends=depends,
        dependency=dependency,
        name=param.name,
    )


def get_parameterless_sub_dependant(*, depends: Depends) -> Dependent:
    assert callable(
        depends.dependency
    ), "A parameter-less dependency must have a callable dependency"
    return get_sub_dependant(depends=depends, dependency=depends.dependency)


def get_sub_dependant(
    *,
    depends: Depends,
    dependency: Callable[..., Any],
    name: Optional[str] = None,
) -> Dependent:
    sub_dependant = get_dependent(
        func=dependency,
        name=name,
        use_cache=depends.use_cache,
    )
    return sub_dependant


def get_dependent(*,
                  func: Callable[..., Any],
                  name: Optional[str] = None,
                  use_cache: bool = True) -> Dependent:
    signature = get_typed_signature(func)
    params = signature.parameters
    dependent = Dependent(func=func, name=name, use_cache=use_cache)
    for param_name, param in params.items():
        if isinstance(param.default, Depends):
            sub_dependent = get_param_sub_dependent(param=param)
            dependent.dependencies.append(sub_dependent)
            continue
        param_field = get_param_field(param=param,
                                      param_name=param_name,
                                      default_field_info=SimpleParam)

    return dependent


def get_param_field(*,
                    param: inspect.Parameter,
                    param_name: str,
                    default_field_info: Type[Param] = Param,
                    force_type: Optional[ParamTypes] = None,
                    ignore_default: bool = False) -> ModelField:
    default_value = Required
    if param.default != param.empty and not ignore_default:
        default_value = param.default
    if isinstance(default_value, FieldInfo):
        field_info = default_value
        default_value = field_info.default
        if (isinstance(field_info, Param) and
                getattr(field_info, "in_", None) is None):
            field_info.in_ = default_field_info.in_
        if force_type:
            field_info.in_ = force_type  # type: ignore
    else:
        field_info = default_field_info(default_value)
    required: bool = default_value == Required
    annotation: Any = Any
    if param.annotation != param.empty:
        annotation = param.annotation
    annotation = get_annotation_from_field_info(annotation, field_info,
                                                param_name)
    if not field_info.alias and getattr(field_info, "convert_underscores",
                                        None):
        alias = param.name.replace("_", "-")
    else:
        alias = field_info.alias or param.name
    field = create_field(
        name=param.name,
        type_=annotation,
        default=None if required else default_value,
        alias=alias,
        required=required,
        field_info=field_info,
    )
    # field.required = required

    return field


def create_field(name: str,
                 type_: Type[Any],
                 class_validators: Optional[Dict[str, Validator]] = None,
                 default: Optional[Any] = None,
                 required: Union[bool, UndefinedType] = False,
                 model_config: Type[BaseConfig] = BaseConfig,
                 field_info: Optional[FieldInfo] = None,
                 alias: Optional[str] = None) -> ModelField:
    class_validators = class_validators or {}
    field_info = field_info or FieldInfo(None)
    return ModelField(name=name,
                      type_=type_,
                      class_validators=class_validators,
                      model_config=model_config,
                      default=default,
                      required=required,
                      alias=alias,
                      field_info=field_info)
