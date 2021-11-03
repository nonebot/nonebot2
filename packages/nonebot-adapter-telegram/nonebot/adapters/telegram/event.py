from typing import Any, Optional

from pydantic import Field

from nonebot.adapters import Event as BaseEvent
from nonebot.typing import overrides
from nonebot.utils import DataclassEncoder

from .message import Message
from .model import *


class Event(BaseEvent):
    class Config:
        extra = "allow"
        json_encoders = {Message: DataclassEncoder}

    @classmethod
    def _parse_event(cls, obj: dict) -> "Event":
        post_type: str = list(obj.keys())[1]
        map = {
            "message": MessageEvent,
            "edited_message": EditedMessageEvent,
            "channel_post": MessageEvent,
            "edited_channel_post": EditedMessageEvent,
            "inline_query": InlineQueryEvent,
            "chosen_inline_result": ChosenInlineResult,
            "callback_query": CallbackQueryEvent,
            "shipping_query": ShippingQueryEvent,
            "pre_checkout_query": PreCheckoutQueryEvent,
            "poll": PollEvent,
            "poll_answer": PollAnswerEvent,
            "chat_member": ChatMemberUpdatedEvent,
            "my_chat_member": ChatMemberUpdatedEvent,
        }
        return map[post_type].parse_event(obj[post_type])

    @classmethod
    def parse_event(cls, obj: dict) -> "Event":
        if cls.__subclasses__():
            return cls._parse_event(obj)
        else:
            return cls.parse_obj(obj)

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return str(self.dict(by_alias=True, exclude_none=True))

    @overrides(BaseEvent)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no user!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no session!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False


class MessageEvent(Event):
    message_id: int
    date: int
    chat: Chat
    forward_from: Optional[User]
    forward_from_chat: Optional[Chat]
    forward_from_message_id: Optional[int]
    forward_signature: Optional[str]
    forward_sender_name: Optional[str]
    via_bot: Optional[User]
    media_group_id: Optional[str]
    author_signature: Optional[str]
    reply_to_message: Optional["MessageEvent"] = None
    message: Optional[Message] = None

    @classmethod
    def _parse_event(cls, obj: dict) -> "Event":
        if "pinned_message" in obj:
            return PinnedMessageEvent.parse_event(obj)
        else:
            message_type = obj["chat"]["type"]
            map = {
                "private": PrivateMessageEvent,
                "group": GroupMessageEvent,
                "supergroup": GroupMessageEvent,
                "channel": ChannelPostEvent,
            }
            return map[message_type].parse_event(obj)

    def __init__(self, **data: Any) -> None:
        reply_to_message = data.pop("reply_to_message", None)
        super().__init__(**data)
        self.message = Message(data)
        if reply_to_message:
            self.reply_to_message = MessageEvent.parse_event(reply_to_message)

    @overrides(Event)
    def get_type(self) -> str:
        return "message"

    @overrides(Event)
    def get_event_name(self) -> str:
        return "message"

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.message.extract_plain_text()

    @overrides(Event)
    def get_session_id(self) -> str:
        return str(self.chat.id)


class PrivateMessageEvent(MessageEvent):
    from_: Optional[User] = Field(default=None, alias="from")

    @overrides(Event)
    def is_tome(self) -> bool:
        return True

    @overrides(MessageEvent)
    def get_event_name(self) -> str:
        return "message.private"

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f"private_{self.chat.id}"

    @overrides(MessageEvent)
    def is_tome(self) -> bool:
        return True


class GroupMessageEvent(MessageEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]

    @overrides(MessageEvent)
    def get_event_name(self) -> str:
        return "message.group"

    @overrides(MessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f"group_{self.from_.id}"


class ChannelPostEvent(MessageEvent):
    sender_chat: Optional[Chat]

    def get_event_name(self) -> str:
        return "message.channel_post"

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return str(self.chat.id)


class EditedMessageEvent(Event):
    message_id: int
    date: int
    chat: Chat
    via_bot: Optional[User]
    edit_date: int
    media_group_id: Optional[str]
    author_signature: Optional[str]
    reply_to_message: Optional["MessageEvent"]
    message: Optional[Message] = None

    @classmethod
    def _parse_event(cls, obj: dict):
        message_type = obj["chat"]["type"]
        map = {
            "private": PrivateEditedMessageEvent,
            "group": GroupEditedMessageEvent,
            "supergroup": GroupEditedMessageEvent,
            "channel": ChannelPostEvent,
        }
        return map[message_type].parse_event(obj)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.message = Message(data)

    @overrides(Event)
    def get_type(self) -> str:
        return "edit_message"

    @overrides(Event)
    def get_event_name(self) -> str:
        return "edit_message"


class PrivateEditedMessageEvent(EditedMessageEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]

    @overrides(EditedMessageEvent)
    def get_event_name(self) -> str:
        return "edited_message.private"

    @overrides(EditedMessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)


class GroupEditedMessageEvent(EditedMessageEvent):
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]

    @overrides(EditedMessageEvent)
    def get_event_name(self) -> str:
        return f"edited_message.group"

    @overrides(EditedMessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)


class EditedChannelPostEvent(EditedMessageEvent):
    sender_chat: Optional[Chat]

    @overrides(EditedMessageEvent)
    def get_event_name(self) -> str:
        return "edited_message.channel_post"

    @overrides(EditedMessageEvent)
    def get_user_id(self) -> str:
        return str(self.from_.id)


class NoticeEvent(Event):
    sender_chat: Optional[Chat]

    @overrides(Event)
    def get_type(self) -> str:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice"


class PinnedMessageEvent(NoticeEvent):
    message_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]
    chat: Chat
    date: int
    pinned_message: Optional[MessageEvent]

    @overrides(Event)
    def get_event_name(self) -> str:
        return "notice.pinned_message"


class NewChatMemberEvent(NoticeEvent):
    pass


class InlineQueryEvent(Event):
    id: str
    from_: User = Field(alias="from")
    query: str
    offset: str
    chat_type: Optional[str]
    Location: Optional[Location]


class ChosenInlineResultEvent(Event):
    result_id: str
    from_: User = Field(alias="from")
    Location: Optional[Location]
    inline_message_id: Optional[str]
    query: str


class CallbackQueryEvent(Event):
    id: str
    from_: Optional[User] = Field(default=None, alias="from")
    message: Optional[Message_]
    inline_message_id: Optional[str]
    chat_instance: Optional[str]
    data: Optional[str]
    game_short_name: Optional[str]


class ShippingQueryEvent(Event):
    id: str
    from_: User = Field(alias="from")
    invoice_payload: str
    shipping_address: ShippingAddress


class PreCheckoutQueryEvent(Event):
    id: str
    from_: User = Field(alias="from")
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str]
    order_info: Optional[OrderInfo]


class PollEvent(Event):
    id: str
    question: str
    options: List[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: Optional[int]
    explanation: Optional[str]
    explanation_entities: Optional[List[MessageEntity]]
    open_period: Optional[int]
    close_date: Optional[int]


class PollAnswerEvent(Event):
    poll_id: str
    user: User
    option_ids: List[int]


class ChatMemberUpdatedEvent(Event):
    chat: Chat
    from_: User = Field(alias="from")
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink]
