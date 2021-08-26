import functools
import operator
from string import Formatter
from typing import (Any, Generic, List, Mapping, Protocol, Sequence, Set, Tuple,
                    Type, TypeVar, Union, TYPE_CHECKING)

if TYPE_CHECKING:
    from nonebot.adapters import Message


class AddAble(Protocol):

    def __add__(self, __s: Any) -> "AddAble":
        ...

    def __str__(self) -> str:
        ...


AddAble_T = TypeVar("AddAble_T", bound=AddAble)
MessageResult_T = TypeVar("MessageResult_T", bound="Message", covariant=True)


class MessageFormatter(Formatter, Generic[MessageResult_T]):

    def __init__(self, factory: Type[MessageResult_T], template: str) -> None:
        super().__init__()
        self.template = template
        self.factory = factory

    def format(self, *args: AddAble, **kwargs: AddAble) -> MessageResult_T:
        msg: AddAble = super().format(self.template, *args, **kwargs)
        return msg if isinstance(msg, self.factory) else self.factory(
            msg)  # type: ignore

    def vformat(self, format_string: str, args: Sequence[AddAble],
                kwargs: Mapping[str, AddAble]):
        result, arg_index, used_args = self._vformat(format_string, args,
                                                     kwargs, set(), 2)
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
    ) -> Tuple[AddAble, int, Set[Union[int, str]]]:

        if recursion_depth < 0:
            raise ValueError("Max string recursion exceeded")

        results: List[AddAble] = []

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
                format_control, auto_arg_index, formatted_args = self._vformat(
                    format_spec,
                    args,
                    kwargs,
                    used_args.copy(),
                    recursion_depth - 1,
                    auto_arg_index,
                )
                used_args |= formatted_args

                # format the object and append to the result
                formatted_text = self.format_field(obj, str(format_control))
                results.append(formatted_text)

        return functools.reduce(operator.add, results or
                                [""]), auto_arg_index, used_args

    def format_field(self, value: AddAble_T,
                     format_spec: str) -> Union[AddAble_T, str]:
        return super().format_field(value,
                                    format_spec) if format_spec else value
