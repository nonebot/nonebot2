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
    def get_user_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(Event)
    def get_session_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(Event)
    def is_tome(self) -> bool:
        return False


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
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(CQHTTPEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)

    @overrides(CQHTTPEvent)
    def is_tome(self) -> bool:
        return self.to_me


class PrivateMessageEvent(MessageEvent):
    __event__ = "message.private"
    message_type: Literal["private"]

    @overrides(CQHTTPEvent)
    def get_event_description(self) -> str:
        return (f'Message {self.message_id} from {self.user_id} "' + "".join(
            map(
                lambda x: escape_tag(str(x))
                if x.is_text() else f"<le>{escape_tag(str(x))}</le>",
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
                    if x.is_text() else f"<le>{escape_tag(str(x))}</le>",
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

    @overrides(CQHTTPEvent)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id


class GroupDecreaseNoticeEvent(NoticeEvent):
    __event__ = "notice.group_decrease"
    notice_type: Literal["group_decrease"]
    sub_type: str
    user_id: int
    group_id: int
    operator_id: int

    @overrides(CQHTTPEvent)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id


class GroupIncreaseNoticeEvent(NoticeEvent):
    __event__ = "notice.group_increase"
    notice_type: Literal["group_increase"]
    sub_type: str
    user_id: int
    group_id: int
    operator_id: int

    @overrides(CQHTTPEvent)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id


class GroupBanNoticeEvent(NoticeEvent):
    __event__ = "notice.group_ban"
    notice_type: Literal["group_ban"]
    sub_type: str
    user_id: int
    group_id: int
    operator_id: int
    duration: int

    @overrides(CQHTTPEvent)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id


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

    @overrides(CQHTTPEvent)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id


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

    @overrides(CQHTTPEvent)
    def is_tome(self) -> bool:
        return self.target_id == self.self_id


class LuckyKingNotifyEvent(NotifyEvent):
    __event__ = "notice.notify.lucky_king"
    sub_type: Literal["lucky_king"]
    target_id: int

    @overrides(CQHTTPEvent)
    def is_tome(self) -> bool:
        return self.target_id == self.self_id


class HonorNotifyEvent(NotifyEvent):
    __event__ = "notice.notify.honor"
    sub_type: Literal["honor"]
    honor_type: str

    @overrides(CQHTTPEvent)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id


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
