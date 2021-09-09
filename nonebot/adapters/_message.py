import abc
from copy import deepcopy
from dataclasses import dataclass, field, asdict
from typing import (Any, List, Dict, Type, Union, TypeVar, Mapping, Generic,
                    Iterable)

from ._formatter import MessageFormatter

T = TypeVar("T")
TMS = TypeVar("TMS", covariant=True)
TM = TypeVar("TM", bound="Message")


@dataclass
class MessageSegment(Mapping, abc.ABC, Generic[TM]):
    """消息段基类"""
    type: str
    """
    - 类型: ``str``
    - 说明: 消息段类型
    """
    data: Dict[str, Any] = field(default_factory=lambda: {})
    """
    - 类型: ``Dict[str, Union[str, list]]``
    - 说明: 消息段数据
    """

    @classmethod
    @abc.abstractmethod
    def get_message_class(cls) -> Type[TM]:
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self) -> str:
        """该消息段所代表的 str，在命令匹配部分使用"""
        raise NotImplementedError

    def __len__(self) -> int:
        return len(str(self))

    def __ne__(self: T, other: T) -> bool:
        return not self == other

    def __add__(self, other: Union[str, Mapping, Iterable[Mapping]]) -> TM:
        return self.get_message_class()(self) + other  # type: ignore

    def __radd__(self, other: Union[str, Mapping, Iterable[Mapping]]) -> TM:
        return self.get_message_class()(other) + self  # type: ignore

    def __getitem__(self, key: str):
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any):
        return setattr(self, key, value)

    def __iter__(self):
        yield from asdict(self).keys()

    def __contains__(self, key: Any) -> bool:
        return key in asdict(self).keys()

    def get(self, key: str, default: Any = None):
        return getattr(self, key, default)

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()

    def items(self):
        return asdict(self).items()

    def copy(self: T) -> T:
        return deepcopy(self)

    @abc.abstractmethod
    def is_text(self) -> bool:
        raise NotImplementedError


class Message(List[TMS], abc.ABC):
    """消息数组"""

    def __init__(self: TM,
                 message: Union[str, None, Mapping, Iterable[Mapping], TMS, TM,
                                Any] = None,
                 *args,
                 **kwargs):
        """
        :参数:

          * ``message: Union[str, list, dict, MessageSegment, Message, Any]``: 消息内容
        """
        super().__init__(*args, **kwargs)
        if message is None:
            return
        elif isinstance(message, Message):
            self.extend(message)
        elif isinstance(message, MessageSegment):
            self.append(message)
        else:
            self.extend(self._construct(message))

    @classmethod
    def template(cls: Type[TM], format_string: str) -> MessageFormatter[TM]:
        """
        :说明:

          根据创建消息模板, 用法和 ``str.format`` 大致相同, 但是可以输出消息对象

        :示例:

        .. code-block:: python

            >>> Message.template("{} {}").format("hello", "world")
            Message(MessageSegment(type='text', data={'text': 'hello world'}))
            >>> Message.template("{} {}").format(MessageSegment.image("file///..."), "world")
            Message(MessageSegment(type='image', data={'file': 'file///...'}), MessageSegment(type='text', data={'text': 'world'}))

        :参数:

          * ``format_string: str``: 格式化字符串

        :返回:

          - ``MessageFormatter[TM]``: 消息格式化器
        """
        return MessageFormatter(cls, format_string)

    @classmethod
    @abc.abstractmethod
    def get_segment_class(cls) -> Type[TMS]:
        raise NotImplementedError

    def __str__(self):
        return "".join(str(seg) for seg in self)

    @classmethod
    def __get_validators__(cls):
        yield cls._validate

    @classmethod
    def _validate(cls, value):
        return cls(value)

    @staticmethod
    @abc.abstractmethod
    def _construct(
            msg: Union[str, Mapping, Iterable[Mapping], Any]) -> Iterable[TMS]:
        raise NotImplementedError

    def __add__(self: TM, other: Union[str, Mapping, Iterable[Mapping]]) -> TM:
        result = self.copy()
        result += other
        return result

    def __radd__(self: TM, other: Union[str, Mapping, Iterable[Mapping]]) -> TM:
        result = self.__class__(other)  # type: ignore
        return result + self

    def __iadd__(self: TM, other: Union[str, Mapping, Iterable[Mapping]]) -> TM:
        if isinstance(other, MessageSegment):
            self.append(other)
        elif isinstance(other, Message):
            self.extend(other)
        else:
            self.extend(self._construct(other))
        return self

    def append(self: TM, obj: Union[str, TMS]) -> TM:
        """
        :说明:

          添加一个消息段到消息数组末尾

        :参数:

          * ``obj: Union[str, MessageSegment]``: 要添加的消息段
        """
        if isinstance(obj, MessageSegment):
            super(Message, self).append(obj)
        elif isinstance(obj, str):
            self.extend(self._construct(obj))
        else:
            raise ValueError(f"Unexpected type: {type(obj)} {obj}")
        return self

    def extend(self: TM, obj: Union[TM, Iterable[TMS]]) -> TM:
        """
        :说明:

          拼接一个消息数组或多个消息段到消息数组末尾

        :参数:

          * ``obj: Union[Message, Iterable[MessageSegment]]``: 要添加的消息数组
        """
        for segment in obj:
            self.append(segment)
        return self

    def copy(self: TM) -> TM:
        return deepcopy(self)

    def extract_plain_text(self: "Message[MessageSegment]") -> str:
        """
        :说明:

          提取消息内纯文本消息
        """

        return "".join(str(seg) for seg in self if seg.is_text())
