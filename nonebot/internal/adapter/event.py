import abc
from typing import Any, TypeVar

from pydantic import BaseModel

from nonebot.compat import PYDANTIC_V2, ConfigDict
from nonebot.utils import DataclassEncoder

from .message import Message

E = TypeVar("E", bound="Event")


class Event(abc.ABC, BaseModel):
    """Event 基类。提供获取关键信息的方法，其余信息可直接获取。"""

    if PYDANTIC_V2:  # pragma: pydantic-v2
        model_config = ConfigDict(extra="allow")
    else:  # pragma: pydantic-v1

        class Config(ConfigDict):
            extra = "allow"  # type: ignore
            json_encoders = {Message: DataclassEncoder}  # noqa: RUF012

    if not PYDANTIC_V2:  # pragma: pydantic-v1

        @classmethod
        def validate(cls: type["E"], value: Any) -> "E":
            if isinstance(value, Event) and not isinstance(value, cls):
                raise TypeError(f"{value} is incompatible with Event type {cls}")
            return super().validate(value)

    @abc.abstractmethod
    def get_type(self) -> str:
        """获取事件类型的方法，类型通常为 NoneBot 内置的四种类型。"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_event_name(self) -> str:
        """获取事件名称的方法。"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_event_description(self) -> str:
        """获取事件描述的方法，通常为事件具体内容。"""
        raise NotImplementedError

    def __str__(self) -> str:
        return f"[{self.get_event_name()}]: {self.get_event_description()}"

    def get_log_string(self) -> str:
        """获取事件日志信息的方法。

        通常你不需要修改这个方法，只有当希望 NoneBot 隐藏该事件日志时，
        可以抛出 `NoLogException` 异常。

        异常:
            NoLogException: 希望 NoneBot 隐藏该事件日志
        """
        return f"[{self.get_event_name()}]: {self.get_event_description()}"

    @abc.abstractmethod
    def get_user_id(self) -> str:
        """获取事件主体 id 的方法，通常是用户 id 。"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_session_id(self) -> str:
        """获取会话 id 的方法，用于判断当前事件属于哪一个会话，
        通常是用户 id、群组 id 组合。
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_message(self) -> "Message":
        """获取事件消息内容的方法。"""
        raise NotImplementedError

    def get_plaintext(self) -> str:
        """获取消息纯文本的方法。

        通常不需要修改，默认通过 `get_message().extract_plain_text` 获取。
        """
        return self.get_message().extract_plain_text()

    @abc.abstractmethod
    def is_tome(self) -> bool:
        """获取事件是否与机器人有关的方法。"""
        raise NotImplementedError
