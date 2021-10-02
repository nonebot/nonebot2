import functools
from string import Formatter
from typing import (TYPE_CHECKING, Any, Set, List, Type, Tuple, Union, Generic,
                    Mapping, TypeVar, Sequence)

if TYPE_CHECKING:
    from . import Message, MessageSegment

TM = TypeVar("TM", bound="Message")


class MessageTemplate(Formatter, Generic[TM]):
    """消息模板格式化实现类"""

    def __init__(self, factory: Type[TM], template: Union[str, TM]) -> None:
        self.template = template
        self.factory = factory

    def format(self, *args: Any, **kwargs: Any) -> TM:
        """
        :说明:

          根据模板和参数生成消息对象
        """
        msg = self.factory()
        if isinstance(self.template, str):
            msg += self.vformat(self.template, args, kwargs)
        elif isinstance(self.template, self.factory):
            for seg in self.template:
                seg: "MessageSegment"
                msg += self.vformat(str(seg), args,
                                    kwargs) if seg.is_text() else seg
        else:
            raise TypeError('template must be a string or instance of Message!')

        return msg

    def vformat(self, format_string: str, args: Sequence[Any],
                kwargs: Mapping[str, Any]) -> TM:
        used_args = set()
        result, _ = self._vformat(format_string, args, kwargs, used_args, 2)
        self.check_unused_args(list(used_args), args, kwargs)
        return result

    def _vformat(
        self,
        format_string: str,
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
        used_args: Set[Union[int, str]],
        recursion_depth: int,
        auto_arg_index: int = 0,
    ) -> Tuple[TM, int]:

        if recursion_depth < 0:
            raise ValueError("Max string recursion exceeded")

        results: List[Any] = []

        for (literal_text, field_name, format_spec,
             conversion) in self.parse(format_string):

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
                            "automatic field numbering")
                    field_name = str(auto_arg_index)
                    auto_arg_index += 1
                elif field_name.isdigit():
                    if auto_arg_index:
                        raise ValueError(
                            "cannot switch from manual field specification to "
                            "automatic field numbering")
                    # disable auto arg incrementing, if it gets
                    # used later on, then an exception will be raised
                    auto_arg_index = False

                # given the field_name, find the object it references
                #  and the argument it came from
                obj, arg_used = self.get_field(field_name, args, kwargs)
                used_args.add(arg_used)

                assert format_spec is not None

                # do any conversion on the resulting object
                obj = self.convert_field(obj, conversion) if conversion else obj

                # expand the format spec, if needed
                format_control, auto_arg_index = self._vformat(
                    format_spec,
                    args,
                    kwargs,
                    used_args,
                    recursion_depth - 1,
                    auto_arg_index,
                )

                # format the object and append to the result
                formatted_text = self.format_field(obj, str(format_control))
                results.append(formatted_text)

        return self.factory(functools.reduce(self._add, results or
                                             [""])), auto_arg_index

    def format_field(self, value: Any, format_spec: str) -> Any:
        return super().format_field(value,
                                    format_spec) if format_spec else value

    def _add(self, a: Any, b: Any) -> Any:
        try:
            return a + b
        except TypeError:
            return a + str(b)
