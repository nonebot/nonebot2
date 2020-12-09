import inspect
from typing_extensions import Literal
from typing import Type, List, Optional

from pydantic import BaseModel
from pygtrie import StringTrie
from nonebot.adapters import Event
from nonebot.utils import escape_tag
from nonebot.typing import overrides
from nonebot.exception import NoLogException

from .message import Message

# class Event(BaseEvent):
#     """
#     CQHTTP 协议 Event 适配。继承属性参考 `BaseEvent <./#class-baseevent>`_ 。
#     """

#     def __init__(self, raw_event: dict):
#         if "message" in raw_event:
#             raw_event["message"] = Message(raw_event["message"])

#         super().__init__(raw_event)

#     @property
#     @overrides(BaseEvent)
#     def id(self) -> Optional[int]:
#         """
#         - 类型: ``Optional[int]``
#         - 说明: 事件/消息 ID
#         """
#         return self._raw_event.get("message_id") or self._raw_event.get("flag")

#     @property
#     @overrides(BaseEvent)
#     def name(self) -> str:
#         """
#         - 类型: ``str``
#         - 说明: 事件名称，由类型与 ``.`` 组合而成
#         """
#         n = self.type + "." + self.detail_type
#         if self.sub_type:
#             n += "." + self.sub_type
#         return n

#     @property
#     @overrides(BaseEvent)
#     def self_id(self) -> str:
#         """
#         - 类型: ``str``
#         - 说明: 机器人自身 ID
#         """
#         return str(self._raw_event["self_id"])

#     @property
#     @overrides(BaseEvent)
#     def time(self) -> int:
#         """
#         - 类型: ``int``
#         - 说明: 事件发生时间
#         """
#         return self._raw_event["time"]

#     @property
#     @overrides(BaseEvent)
#     def type(self) -> str:
#         """
#         - 类型: ``str``
#         - 说明: 事件类型
#         """
#         return self._raw_event["post_type"]

#     @type.setter
#     @overrides(BaseEvent)
#     def type(self, value) -> None:
#         self._raw_event["post_type"] = value

#     @property
#     @overrides(BaseEvent)
#     def detail_type(self) -> str:
#         """
#         - 类型: ``str``
#         - 说明: 事件详细类型
#         """
#         return self._raw_event[f"{self.type}_type"]

#     @detail_type.setter
#     @overrides(BaseEvent)
#     def detail_type(self, value) -> None:
#         self._raw_event[f"{self.type}_type"] = value

#     @property
#     @overrides(BaseEvent)
#     def sub_type(self) -> Optional[str]:
#         """
#         - 类型: ``Optional[str]``
#         - 说明: 事件子类型
#         """
#         return self._raw_event.get("sub_type")

#     @sub_type.setter
#     @overrides(BaseEvent)
#     def sub_type(self, value) -> None:
#         self._raw_event["sub_type"] = value

#     @property
#     @overrides(BaseEvent)
#     def user_id(self) -> Optional[int]:
#         """
#         - 类型: ``Optional[int]``
#         - 说明: 事件主体 ID
#         """
#         return self._raw_event.get("user_id")

#     @user_id.setter
#     @overrides(BaseEvent)
#     def user_id(self, value) -> None:
#         self._raw_event["user_id"] = value

#     @property
#     @overrides(BaseEvent)
#     def group_id(self) -> Optional[int]:
#         """
#         - 类型: ``Optional[int]``
#         - 说明: 事件主体群 ID
#         """
#         return self._raw_event.get("group_id")

#     @group_id.setter
#     @overrides(BaseEvent)
#     def group_id(self, value) -> None:
#         self._raw_event["group_id"] = value

#     @property
#     @overrides(BaseEvent)
#     def to_me(self) -> Optional[bool]:
#         """
#         - 类型: ``Optional[bool]``
#         - 说明: 消息是否与机器人相关
#         """
#         return self._raw_event.get("to_me")

#     @to_me.setter
#     @overrides(BaseEvent)
#     def to_me(self, value) -> None:
#         self._raw_event["to_me"] = value

#     @property
#     @overrides(BaseEvent)
#     def message(self) -> Optional["Message"]:
#         """
#         - 类型: ``Optional[Message]``
#         - 说明: 消息内容
#         """
#         return self._raw_event.get("message")

#     @message.setter
#     @overrides(BaseEvent)
#     def message(self, value) -> None:
#         self._raw_event["message"] = value

#     @property
#     @overrides(BaseEvent)
#     def reply(self) -> Optional[dict]:
#         """
#         - 类型: ``Optional[dict]``
#         - 说明: 回复消息详情
#         """
#         return self._raw_event.get("reply")

#     @reply.setter
#     @overrides(BaseEvent)
#     def reply(self, value) -> None:
#         self._raw_event["reply"] = value

#     @property
#     @overrides(BaseEvent)
#     def raw_message(self) -> Optional[str]:
#         """
#         - 类型: ``Optional[str]``
#         - 说明: 原始消息
#         """
#         return self._raw_event.get("raw_message")

#     @raw_message.setter
#     @overrides(BaseEvent)
#     def raw_message(self, value) -> None:
#         self._raw_event["raw_message"] = value

#     @property
#     @overrides(BaseEvent)
#     def plain_text(self) -> Optional[str]:
#         """
#         - 类型: ``Optional[str]``
#         - 说明: 纯文本消息内容
#         """
#         return self.message and self.message.extract_plain_text()

#     @property
#     @overrides(BaseEvent)
#     def sender(self) -> Optional[dict]:
#         """
#         - 类型: ``Optional[dict]``
#         - 说明: 消息发送者信息
#         """
#         return self._raw_event.get("sender")

#     @sender.setter
#     @overrides(BaseEvent)
#     def sender(self, value) -> None:
#         self._raw_event["sender"] = value


class CQHTTPEvent(Event):
    __event__ = ""
    time: int
    self_id: int
    post_type: Literal["message", "notice", "request", "meta_event"]

    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return self.post_type

    @overrides(Event)
    def get_event_name(self) -> str:
        return self.post_type

    @overrides(Event)
    def get_event_description(self) -> str:
        return str(self.dict())

    @overrides(Event)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(Event)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(Event)
    def get_session_id(self) -> str:
        raise ValueError("Event has no message!")


# Models
class Sender(BaseModel):
    user_id: Optional[int] = None
    nickname: Optional[str] = None
    sex: Optional[str] = None
    age: Optional[int] = None
    card: Optional[str] = None
    area: Optional[str] = None
    level: Optional[str] = None
    role: Optional[str] = None
    title: Optional[str] = None

    class Config:
        extra = "allow"


class Reply(BaseModel):
    time: int
    message_type: str
    message_id: int
    real_id: int
    sender: Sender
    message: Message

    class Config:
        extra = "allow"


class Anonymous(BaseModel):
    id: int
    name: str
    flag: str

    class Config:
        extra = "allow"


class File(BaseModel):
    id: str
    name: str
    size: int
    busid: int

    class Config:
        extra = "allow"


class Status(BaseModel):
    online: bool
    good: bool

    class Config:
        extra = "allow"


# Message Events
class MessageEvent(CQHTTPEvent):
    __event__ = "message"
    post_type: Literal["message"]
    sub_type: str
    user_id: int
    message_type: str
    message_id: int
    message: Message
    raw_message: str
    font: int
    sender: Sender
    to_me: bool = False
    reply: Optional[Reply] = None

    @overrides(CQHTTPEvent)
    def get_event_name(self) -> str:
        sub_type = getattr(self, "sub_type", None)
        return f"{self.post_type}.{self.message_type}" + (f".{sub_type}"
                                                          if sub_type else "")

    @overrides(CQHTTPEvent)
    def get_message(self) -> Message:
        return self.message

    @overrides(CQHTTPEvent)
    def get_plaintext(self) -> str:
        return self.message.extract_plain_text()

    @overrides(CQHTTPEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class PrivateMessageEvent(MessageEvent):
    __event__ = "message.private"
    message_type: Literal["private"]

    @overrides(CQHTTPEvent)
    def get_event_description(self) -> str:
        return (f'Message {self.message_id} from {self.user_id} "' + "".join(
            map(
                lambda x: escape_tag(str(x))
                if x.type == "text" else f"<le>{escape_tag(str(x))}</le>",
                self.message)) + '"')


class GroupMessageEvent(MessageEvent):
    __event__ = "message.group"
    message_type: Literal["group"]
    group_id: int
    anonymous: Anonymous

    @overrides(CQHTTPEvent)
    def get_event_description(self) -> str:
        return (
            f'Message {self.message_id} from {self.user_id}@[群:{self.group_id}] "'
            + "".join(
                map(
                    lambda x: escape_tag(str(x))
                    if x.type == "text" else f"<le>{escape_tag(str(x))}</le>",
                    self.message)) + '"')


# Notice Events
class NoticeEvent(CQHTTPEvent):
    __event__ = "notice"
    post_type: Literal["notice"]
    notice_type: str

    @overrides(CQHTTPEvent)
    def get_event_name(self) -> str:
        sub_type = getattr(self, "sub_type", None)
        return f"{self.post_type}.{self.notice_type}" + (f".{sub_type}"
                                                         if sub_type else "")


class GroupUploadNoticeEvent(NoticeEvent):
    __event__ = "notice.group_upload"
    notice_type: Literal["group_upload"]
    user_id: int
    group_id: int
    file: File


class GroupAdminNoticeEvent(NoticeEvent):
    __event__ = "notice.group_admin"
    notice_type: Literal["group_admin"]
    sub_type: str
    user_id: int
    group_id: int


class GroupDecreaseNoticeEvent(NoticeEvent):
    __event__ = "notice.group_decrease"
    notice_type: Literal["group_decrease"]
    sub_type: str
    user_id: int
    group_id: int
    operator_id: int


class GroupIncreaseNoticeEvent(NoticeEvent):
    __event__ = "notice.group_increase"
    notice_type: Literal["group_increase"]
    sub_type: str
    user_id: int
    group_id: int
    operator_id: int


class GroupBanNoticeEvent(NoticeEvent):
    __event__ = "notice.group_ban"
    notice_type: Literal["group_ban"]
    sub_type: str
    user_id: int
    group_id: int
    operator_id: int
    duration: int


class FriendAddNoticeEvent(NoticeEvent):
    __event__ = "notice.friend_add"
    notice_type: Literal["friend_add"]
    user_id: int


class GroupRecallNoticeEvent(NoticeEvent):
    __event__ = "notice.group_recall"
    notice_type: Literal["group_recall"]
    user_id: int
    group_id: int
    operator_id: int
    message_id: int


class FriendRecallNoticeEvent(NoticeEvent):
    __event__ = "notice.friend_recall"
    notice_type: Literal["friend_recall"]
    user_id: int
    message_id: int


class NotifyEvent(NoticeEvent):
    __event__ = "notice.notify"
    notice_type: Literal["notify"]
    sub_type: str
    user_id: int
    group_id: int


class PokeNotifyEvent(NotifyEvent):
    __event__ = "notice.notify.poke"
    sub_type: Literal["poke"]
    target_id: int


class LuckyKingNotifyEvent(NotifyEvent):
    __event__ = "notice.notify.lucky_king"
    sub_type: Literal["lucky_king"]
    target_id: int


class HonorNotifyEvent(NotifyEvent):
    __event__ = "notice.notify.honor"
    sub_type: Literal["honor"]
    honor_type: str


# Request Events
class RequestEvent(CQHTTPEvent):
    __event__ = "request"
    post_type: Literal["request"]
    request_type: str

    @overrides(CQHTTPEvent)
    def get_event_name(self) -> str:
        sub_type = getattr(self, "sub_type", None)
        return f"{self.post_type}.{self.request_type}" + (f".{sub_type}"
                                                          if sub_type else "")


class FriendRequestEvent(RequestEvent):
    __event__ = "request.friend"
    request_type: Literal["friend"]
    user_id: int
    comment: str
    flag: str


class GroupRequestEvent(RequestEvent):
    __event__ = "request.group"
    request_type: Literal["group"]
    sub_type: str
    group_id: int
    user_id: int
    comment: str
    flag: str


# Meta Events
class MetaEvent(CQHTTPEvent):
    __event__ = "meta_event"
    post_type: Literal["meta_event"]
    meta_event_type: str

    @overrides(CQHTTPEvent)
    def get_event_name(self) -> str:
        sub_type = getattr(self, "sub_type", None)
        return f"{self.post_type}.{self.meta_event_type}" + (f".{sub_type}" if
                                                             sub_type else "")

    @overrides(CQHTTPEvent)
    def get_log_string(self) -> str:
        raise NoLogException


class LifecycleMetaEvent(MetaEvent):
    __event__ = "meta_event.lifecycle"
    meta_event_type: Literal["lifecycle"]
    sub_type: str


class HeartbeatMetaEvent(MetaEvent):
    __event__ = "meta_event.heartbeat"
    meta_event_type: Literal["heartbeat"]
    status: Status
    interval: int


_t = StringTrie(separator=".")

model = None
for model in globals().values():
    if not inspect.isclass(model) or not issubclass(model, CQHTTPEvent):
        continue
    _t["." + model.__event__] = model


def get_event_model(event_name) -> List[Type[CQHTTPEvent]]:
    return [model.value for model in _t.prefixes("." + event_name)][::-1]
