from typing import Union, Optional
from typing_extensions import Literal

from pydantic import BaseModel, validator, parse_obj_as
from pydantic.fields import ModelField

from nonebot.adapters import Event as BaseEvent
from nonebot.utils import escape_tag

from .message import Message
from .model import MessageModel, PrivateMessageModel, GroupMessageModel, ConversationType, TextMessage


class Event(BaseEvent):
    """
    钉钉 协议 Event 适配。继承属性参考 `BaseEvent <./#class-baseevent>`_ 。
    """
    message: Message = None

    def __init__(self, **data):
        super().__init__(**data)
        # 其实目前钉钉机器人只能接收到 text 类型的消息
        message: Union[TextMessage] = getattr(self, self.msgtype, None)
        self.message = parse_obj_as(Message, message)

    def get_type(self) -> Literal["message"]:
        """
        - 类型: ``str``
        - 说明: 事件类型
        """
        return "message"

    def get_event_name(self) -> str:
        detail_type = self.conversationType.name
        return self.get_type() + "." + detail_type

    def get_event_description(self) -> str:
        return (f'Message[{self.msgtype}] {self.msgId} from {self.senderId} "' +
                "".join(
                    map(
                        lambda x: escape_tag(str(x))
                        if x.is_text() else f"<le>{escape_tag(str(x))}</le>",
                        self.message,
                    )) + '"')

    def get_user_id(self) -> str:
        return self.senderId

    def get_session_id(self) -> str:
        """
        - 类型: ``str``
        - 说明: 消息 ID
        """
        return self.msgId

    def get_message(self) -> "Message":
        """
        - 类型: ``Message``
        - 说明: 消息内容
        """
        return self.message

    def get_plaintext(self) -> str:
        """
        - 类型: ``str``
        - 说明: 纯文本消息内容
        """
        return self.message.extract_plain_text().strip() if self.message else ""


class MessageEvent(MessageModel, Event):
    pass


class PrivateMessageEvent(PrivateMessageModel, Event):

    def is_tome(self) -> bool:
        return True


class GroupMessageEvent(GroupMessageModel, Event):

    def is_tome(self) -> bool:
        return self.isInAtList
