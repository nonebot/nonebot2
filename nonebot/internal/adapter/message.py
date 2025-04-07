import abc
from collections.abc import Iterable
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import (  # noqa: UP035
    Any,
    Generic,
    Optional,
    SupportsIndex,
    Type,
    TypeVar,
    Union,
    overload,
)
from typing_extensions import Self

from nonebot.compat import custom_validation, type_validate_python

from .template import MessageTemplate

TMS = TypeVar("TMS", bound="MessageSegment")
TM = TypeVar("TM", bound="Message")


@custom_validation
@dataclass
class MessageSegment(abc.ABC, Generic[TM]):
    """消息段基类"""

    type: str
    """消息段类型"""
    data: dict[str, Any] = field(default_factory=dict)
    """消息段数据"""

    @classmethod
    @abc.abstractmethod
    def get_message_class(cls) -> Type[TM]:  # noqa: UP006
        """获取消息数组类型"""
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self) -> str:
        """该消息段所代表的 str，在命令匹配部分使用"""
        raise NotImplementedError

    def __len__(self) -> int:
        return len(str(self))

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self
    ) -> bool:
        return not self == other

    def __add__(self, other: Union[str, Self, Iterable[Self]]) -> TM:
        return self.get_message_class()(self) + other

    def __radd__(self, other: Union[str, Self, Iterable[Self]]) -> TM:
        return self.get_message_class()(other) + self

    @classmethod
    def __get_validators__(cls):
        yield cls._validate

    @classmethod
    def _validate(cls, value) -> Self:
        if isinstance(value, cls):
            return value
        if isinstance(value, MessageSegment):
            raise ValueError(f"Type {type(value)} can not be converted to {cls}")
        if not isinstance(value, dict):
            raise ValueError(f"Expected dict for MessageSegment, got {type(value)}")
        if "type" not in value:
            raise ValueError(
                f"Expected dict with 'type' for MessageSegment, got {value}"
            )
        return cls(type=value["type"], data=value.get("data", {}))

    def get(self, key: str, default: Any = None):
        return asdict(self).get(key, default)

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()

    def items(self):
        return asdict(self).items()

    def join(self, iterable: Iterable[Union[Self, TM]]) -> TM:
        return self.get_message_class()(self).join(iterable)

    def copy(self) -> Self:
        return deepcopy(self)

    @abc.abstractmethod
    def is_text(self) -> bool:
        """当前消息段是否为纯文本"""
        raise NotImplementedError


@custom_validation
class Message(list[TMS], abc.ABC):
    """消息序列

    参数:
        message: 消息内容
    """

    def __init__(
        self,
        message: Union[str, None, Iterable[TMS], TMS] = None,
    ):
        super().__init__()
        if message is None:
            return
        elif isinstance(message, str):
            self.extend(self._construct(message))
        elif isinstance(message, MessageSegment):
            self.append(message)
        elif isinstance(message, Iterable):
            self.extend(message)
        else:
            self.extend(self._construct(message))  # pragma: no cover

    @classmethod
    def template(cls, format_string: Union[str, TM]) -> MessageTemplate[Self]:
        """创建消息模板。

        用法和 `str.format` 大致相同，支持以 `Message` 对象作为消息模板并输出消息对象。
        并且提供了拓展的格式化控制符，
        可以通过该消息类型的 `MessageSegment` 工厂方法创建消息。

        参数:
            format_string: 格式化模板

        返回:
            消息格式化器
        """
        return MessageTemplate(format_string, cls)

    @classmethod
    @abc.abstractmethod
    def get_segment_class(cls) -> type[TMS]:
        """获取消息段类型"""
        raise NotImplementedError

    def __str__(self) -> str:
        return "".join(str(seg) for seg in self)

    @classmethod
    def __get_validators__(cls):
        yield cls._validate

    @classmethod
    def _validate(cls, value) -> Self:
        if isinstance(value, cls):
            return value
        elif isinstance(value, Message):
            raise ValueError(f"Type {type(value)} can not be converted to {cls}")
        elif isinstance(value, str):
            pass
        elif isinstance(value, dict):
            value = type_validate_python(cls.get_segment_class(), value)
        elif isinstance(value, Iterable):
            value = [type_validate_python(cls.get_segment_class(), v) for v in value]
        else:
            raise ValueError(
                f"Expected str, dict or iterable for Message, got {type(value)}"
            )
        return cls(value)

    @staticmethod
    @abc.abstractmethod
    def _construct(msg: str) -> Iterable[TMS]:
        """构造消息数组"""
        raise NotImplementedError

    def __add__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Union[str, TMS, Iterable[TMS]]
    ) -> Self:
        result = self.copy()
        result += other
        return result

    def __radd__(self, other: Union[str, TMS, Iterable[TMS]]) -> Self:
        result = self.__class__(other)
        return result + self

    def __iadd__(self, other: Union[str, TMS, Iterable[TMS]]) -> Self:
        if isinstance(other, str):
            self.extend(self._construct(other))
        elif isinstance(other, MessageSegment):
            self.append(other)
        elif isinstance(other, Iterable):
            self.extend(other)
        else:
            raise TypeError(f"Unsupported type {type(other)!r}")
        return self

    @overload
    def __getitem__(self, args: str) -> Self:
        """获取仅包含指定消息段类型的消息

        参数:
            args: 消息段类型

        返回:
            所有类型为 `args` 的消息段
        """

    @overload
    def __getitem__(self, args: tuple[str, int]) -> TMS:
        """索引指定类型的消息段

        参数:
            args: 消息段类型和索引

        返回:
            类型为 `args[0]` 的消息段第 `args[1]` 个
        """

    @overload
    def __getitem__(self, args: tuple[str, slice]) -> Self:
        """切片指定类型的消息段

        参数:
            args: 消息段类型和切片

        返回:
            类型为 `args[0]` 的消息段切片 `args[1]`
        """

    @overload
    def __getitem__(self, args: int) -> TMS:
        """索引消息段

        参数:
            args: 索引

        返回:
            第 `args` 个消息段
        """

    @overload
    def __getitem__(self, args: slice) -> Self:
        """切片消息段

        参数:
            args: 切片

        返回:
            消息切片 `args`
        """

    def __getitem__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        args: Union[
            str,
            tuple[str, int],
            tuple[str, slice],
            int,
            slice,
        ],
    ) -> Union[TMS, Self]:
        arg1, arg2 = args if isinstance(args, tuple) else (args, None)
        if isinstance(arg1, int) and arg2 is None:
            return super().__getitem__(arg1)
        elif isinstance(arg1, slice) and arg2 is None:
            return self.__class__(super().__getitem__(arg1))
        elif isinstance(arg1, str) and arg2 is None:
            return self.__class__(seg for seg in self if seg.type == arg1)
        elif isinstance(arg1, str) and isinstance(arg2, int):
            return [seg for seg in self if seg.type == arg1][arg2]
        elif isinstance(arg1, str) and isinstance(arg2, slice):
            return self.__class__([seg for seg in self if seg.type == arg1][arg2])
        else:
            raise ValueError("Incorrect arguments to slice")  # pragma: no cover

    def __contains__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, value: Union[TMS, str]
    ) -> bool:
        """检查消息段是否存在

        参数:
            value: 消息段或消息段类型
        返回:
            消息内是否存在给定消息段或给定类型的消息段
        """
        if isinstance(value, str):
            return next((seg for seg in self if seg.type == value), None) is not None
        return super().__contains__(value)

    def has(self, value: Union[TMS, str]) -> bool:
        """与 {ref}``__contains__` <nonebot.adapters.Message.__contains__>` 相同"""
        return value in self

    def index(self, value: Union[TMS, str], *args: SupportsIndex) -> int:
        """索引消息段

        参数:
            value: 消息段或者消息段类型
            arg: start 与 end

        返回:
            索引 index

        异常:
            ValueError: 消息段不存在
        """
        if isinstance(value, str):
            first_segment = next((seg for seg in self if seg.type == value), None)
            if first_segment is None:
                raise ValueError(f"Segment with type {value!r} is not in message")
            return super().index(first_segment, *args)
        return super().index(value, *args)

    def get(self, type_: str, count: Optional[int] = None) -> Self:
        """获取指定类型的消息段

        参数:
            type_: 消息段类型
            count: 获取个数

        返回:
            构建的新消息
        """
        if count is None:
            return self[type_]

        iterator, filtered = (
            (seg for seg in self if seg.type == type_),
            self.__class__(),
        )
        for _ in range(count):
            seg = next(iterator, None)
            if seg is None:
                break
            filtered.append(seg)
        return filtered

    def count(self, value: Union[TMS, str]) -> int:
        """计算指定消息段的个数

        参数:
            value: 消息段或消息段类型

        返回:
            个数
        """
        return len(self[value]) if isinstance(value, str) else super().count(value)

    def only(self, value: Union[TMS, str]) -> bool:
        """检查消息中是否仅包含指定消息段

        参数:
            value: 指定消息段或消息段类型

        返回:
            是否仅包含指定消息段
        """
        if isinstance(value, str):
            return all(seg.type == value for seg in self)
        return all(seg == value for seg in self)

    def append(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, obj: Union[str, TMS]
    ) -> Self:
        """添加一个消息段到消息数组末尾。

        参数:
            obj: 要添加的消息段
        """
        if isinstance(obj, MessageSegment):
            super().append(obj)
        elif isinstance(obj, str):
            self.extend(self._construct(obj))
        else:
            raise ValueError(f"Unexpected type: {type(obj)} {obj}")  # pragma: no cover
        return self

    def extend(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, obj: Union[Self, Iterable[TMS]]
    ) -> Self:
        """拼接一个消息数组或多个消息段到消息数组末尾。

        参数:
            obj: 要添加的消息数组
        """
        for segment in obj:
            self.append(segment)
        return self

    def join(self, iterable: Iterable[Union[TMS, Self]]) -> Self:
        """将多个消息连接并将自身作为分割

        参数:
            iterable: 要连接的消息

        返回:
            连接后的消息
        """
        ret = self.__class__()
        for index, msg in enumerate(iterable):
            if index != 0:
                ret.extend(self)
            if isinstance(msg, MessageSegment):
                ret.append(msg.copy())
            else:
                ret.extend(msg.copy())
        return ret

    def copy(self) -> Self:
        """深拷贝消息"""
        return deepcopy(self)

    def include(self, *types: str) -> Self:
        """过滤消息

        参数:
            types: 包含的消息段类型

        返回:
            新构造的消息
        """
        return self.__class__(seg for seg in self if seg.type in types)

    def exclude(self, *types: str) -> Self:
        """过滤消息

        参数:
            types: 不包含的消息段类型

        返回:
            新构造的消息
        """
        return self.__class__(seg for seg in self if seg.type not in types)

    def extract_plain_text(self) -> str:
        """提取消息内纯文本消息"""

        return "".join(str(seg) for seg in self if seg.is_text())
