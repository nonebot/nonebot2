from _string import formatter_field_name_split  # type: ignore
from collections.abc import Mapping, Sequence
import functools
from string import Formatter
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Optional,
    TypeVar,
    Union,
    cast,
    overload,
)
from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from .message import Message, MessageSegment

    def formatter_field_name_split(
        field_name: str,
    ) -> tuple[str, list[tuple[bool, str]]]: ...


TM = TypeVar("TM", bound="Message")
TF = TypeVar("TF", str, "Message")

FormatSpecFunc: TypeAlias = Callable[[Any], str]
FormatSpecFunc_T = TypeVar("FormatSpecFunc_T", bound=FormatSpecFunc)


class MessageTemplate(Formatter, Generic[TF]):
    """消息模板格式化实现类。

    参数:
        template: 模板
        factory: 消息类型工厂，默认为 `str`
        private_getattr: 是否允许在模板中访问私有属性，默认为 `False`
    """

    @overload
    def __init__(
        self: "MessageTemplate[str]",
        template: str,
        factory: type[str] = str,
        private_getattr: bool = False,
    ) -> None: ...

    @overload
    def __init__(
        self: "MessageTemplate[TM]",
        template: Union[str, TM],
        factory: type[TM],
        private_getattr: bool = False,
    ) -> None: ...

    def __init__(
        self,
        template: Union[str, TM],
        factory: Union[type[str], type[TM]] = str,
        private_getattr: bool = False,
    ) -> None:
        self.template: TF = template  # type: ignore
        self.factory: type[TF] = factory  # type: ignore
        self.format_specs: dict[str, FormatSpecFunc] = {}
        self.private_getattr = private_getattr

    def __repr__(self) -> str:
        return f"MessageTemplate({self.template!r}, factory={self.factory!r})"

    def add_format_spec(
        self, spec: FormatSpecFunc_T, name: Optional[str] = None
    ) -> FormatSpecFunc_T:
        name = name or spec.__name__
        if name in self.format_specs:
            raise ValueError(f"Format spec {name} already exists!")
        self.format_specs[name] = spec
        return spec

    def format(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, *args, **kwargs
    ) -> TF:
        """根据传入参数和模板生成消息对象"""
        return self._format(args, kwargs)

    def format_map(self, mapping: Mapping[str, Any]) -> TF:
        """根据传入字典和模板生成消息对象, 在传入字段名不是有效标识符时有用"""
        return self._format([], mapping)

    def _format(self, args: Sequence[Any], kwargs: Mapping[str, Any]) -> TF:
        full_message = self.factory()
        used_args, arg_index = set(), 0

        if isinstance(self.template, str):
            msg, arg_index = self._vformat(
                self.template, args, kwargs, used_args, arg_index
            )
            full_message += msg
        elif isinstance(self.template, self.factory):
            template = cast("Message[MessageSegment]", self.template)
            for seg in template:
                if not seg.is_text():
                    full_message += seg
                else:
                    msg, arg_index = self._vformat(
                        str(seg), args, kwargs, used_args, arg_index
                    )
                    full_message += msg
        else:
            raise TypeError("template must be a string or instance of Message!")

        self.check_unused_args(used_args, args, kwargs)
        return cast(TF, full_message)

    def vformat(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        format_string: str,
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
    ) -> TF:
        raise NotImplementedError("`vformat` has merged into `_format`")

    def _vformat(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        format_string: str,
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
        used_args: set[Union[int, str]],
        auto_arg_index: int = 0,
    ) -> tuple[TF, int]:
        results: list[Any] = [self.factory()]

        for literal_text, field_name, format_spec, conversion in self.parse(
            format_string
        ):
            # output the literal text
            if literal_text:
                results.append(literal_text)

            # if there's a field, output it
            if field_name is not None:
                # this is some markup, find the object and do
                #  the formatting

                # handle arg indexing when empty field_names are given.
                if field_name == "":
                    if auto_arg_index is False:
                        raise ValueError(
                            "cannot switch from manual field specification to "
                            "automatic field numbering"
                        )
                    field_name = str(auto_arg_index)
                    auto_arg_index += 1
                elif field_name.isdigit():
                    if auto_arg_index:
                        raise ValueError(
                            "cannot switch from manual field specification to "
                            "automatic field numbering"
                        )
                    # disable auto arg incrementing, if it gets
                    # used later on, then an exception will be raised
                    auto_arg_index = False

                # given the field_name, find the object it references
                #  and the argument it came from
                obj, arg_used = self.get_field(field_name, args, kwargs)
                used_args.add(arg_used)

                # do any conversion on the resulting object
                obj = self.convert_field(obj, conversion) if conversion else obj

                # format the object and append to the result
                formatted_text = (
                    self.format_field(obj, format_spec) if format_spec else obj
                )
                results.append(formatted_text)

        return functools.reduce(self._add, results), auto_arg_index

    def get_field(
        self, field_name: str, args: Sequence[Any], kwargs: Mapping[str, Any]
    ) -> tuple[Any, Union[int, str]]:
        first, rest = formatter_field_name_split(field_name)
        obj = self.get_value(first, args, kwargs)

        for is_attr, value in rest:
            if not self.private_getattr and value.startswith("_"):
                raise ValueError("Cannot access private attribute")
            obj = getattr(obj, value) if is_attr else obj[value]

        return obj, first

    def format_field(self, value: Any, format_spec: str) -> Any:
        formatter: Optional[FormatSpecFunc] = self.format_specs.get(format_spec)
        if formatter is None and not issubclass(self.factory, str):
            segment_class: type["MessageSegment"] = self.factory.get_segment_class()
            method = getattr(segment_class, format_spec, None)
            if callable(method) and not cast(str, method.__name__).startswith("_"):
                formatter = getattr(segment_class, format_spec)
        return (
            super().format_field(value, format_spec)
            if formatter is None
            else formatter(value)
        )

    def _add(self, a: Any, b: Any) -> Any:
        try:
            return a + b
        except TypeError:
            return a + str(b)
