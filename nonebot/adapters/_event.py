import abc

from pydantic import BaseModel

from ._message import Message
from nonebot.utils import DataclassEncoder


class Event(abc.ABC, BaseModel):
    """Event 基类。提供获取关键信息的方法，其余信息可直接获取。"""

    class Config:
        extra = "allow"
        json_encoders = {Message: DataclassEncoder}

    @abc.abstractmethod
    def get_type(self) -> str:
        """
        :说明:

          获取事件类型的方法，类型通常为 NoneBot 内置的四种类型。

        :返回:

          * ``Literal["message", "notice", "request", "meta_event"]``
          * 其他自定义 ``str``
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_event_name(self) -> str:
        """
        :说明:

          获取事件名称的方法。

        :返回:

          * ``str``
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_event_description(self) -> str:
        """
        :说明:

          获取事件描述的方法，通常为事件具体内容。

        :返回:

          * ``str``
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return f"[{self.get_event_name()}]: {self.get_event_description()}"

    def get_log_string(self) -> str:
        """
        :说明:

          获取事件日志信息的方法，通常你不需要修改这个方法，只有当希望 NoneBot 隐藏该事件日志时，可以抛出 ``NoLogException`` 异常。

        :返回:

          * ``str``

        :异常:

          - ``NoLogException``
        """
        return f"[{self.get_event_name()}]: {self.get_event_description()}"

    @abc.abstractmethod
    def get_user_id(self) -> str:
        """
        :说明:

          获取事件主体 id 的方法，通常是用户 id 。

        :返回:

          * ``str``
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_session_id(self) -> str:
        """
        :说明:

          获取会话 id 的方法，用于判断当前事件属于哪一个会话，通常是用户 id、群组 id 组合。

        :返回:

          * ``str``
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_message(self) -> "Message":
        """
        :说明:

          获取事件消息内容的方法。

        :返回:

          * ``Message``
        """
        raise NotImplementedError

    def get_plaintext(self) -> str:
        """
        :说明:

          获取消息纯文本的方法，通常不需要修改，默认通过 ``get_message().extract_plain_text`` 获取。

        :返回:

          * ``str``
        """
        return self.get_message().extract_plain_text()

    @abc.abstractmethod
    def is_tome(self) -> bool:
        """
        :说明:

          获取事件是否与机器人有关的方法。

        :返回:

          * ``bool``
        """
        raise NotImplementedError
