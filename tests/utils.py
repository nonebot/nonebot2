from typing import Type, Union, Mapping, Iterable, Optional

from pydantic import Extra, create_model

from nonebot.adapters import Event, Message, MessageSegment


def escape_text(s: str, *, escape_comma: bool = True) -> str:
    s = s.replace("&", "&amp;").replace("[", "&#91;").replace("]", "&#93;")
    if escape_comma:
        s = s.replace(",", "&#44;")
    return s


class FakeMessageSegment(MessageSegment["FakeMessage"]):
    @classmethod
    def get_message_class(cls):
        return FakeMessage

    def __str__(self) -> str:
        return self.data["text"] if self.type == "text" else f"[fake:{self.type}]"

    @classmethod
    def text(cls, text: str):
        return cls("text", {"text": text})

    @staticmethod
    def image(url: str):
        return FakeMessageSegment("image", {"url": url})

    @staticmethod
    def nested(content: "FakeMessage"):
        return FakeMessageSegment("node", {"content": content})

    def is_text(self) -> bool:
        return self.type == "text"


class FakeMessage(Message[FakeMessageSegment]):
    @classmethod
    def get_segment_class(cls):
        return FakeMessageSegment

    @staticmethod
    def _construct(msg: Union[str, Iterable[Mapping]]):
        if isinstance(msg, str):
            yield FakeMessageSegment.text(msg)
        else:
            for seg in msg:
                yield FakeMessageSegment(**seg)
        return

    def __add__(
        self, other: Union[str, FakeMessageSegment, Iterable[FakeMessageSegment]]
    ):
        other = escape_text(other) if isinstance(other, str) else other
        return super().__add__(other)


def make_fake_event(
    _base: Optional[Type[Event]] = None,
    _type: str = "message",
    _name: str = "test",
    _description: str = "test",
    _user_id: Optional[str] = "test",
    _session_id: Optional[str] = "test",
    _message: Optional[Message] = None,
    _to_me: bool = True,
    **fields,
) -> Type[Event]:
    Base = _base or Event

    class FakeEvent(Base, extra=Extra.forbid):
        def get_type(self) -> str:
            return _type

        def get_event_name(self) -> str:
            return _name

        def get_event_description(self) -> str:
            return _description

        def get_user_id(self) -> str:
            if _user_id is not None:
                return _user_id
            raise NotImplementedError

        def get_session_id(self) -> str:
            if _session_id is not None:
                return _session_id
            raise NotImplementedError

        def get_message(self) -> "Message":
            if _message is not None:
                return _message
            raise NotImplementedError

        def is_tome(self) -> bool:
            return _to_me

    return create_model("FakeEvent", __base__=FakeEvent, **fields)
