from typing import Union, Mapping, Iterable
from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment):

    def __str__(self) -> str:
        raise NotImplementedError

    def __add__(self, other) -> "Message":
        return Message(self) + other

    def __radd__(self, other) -> "Message":
        return Message(other) + self

    def is_text(self) -> bool:
        raise NotImplementedError


class Message(BaseMessage):

    @staticmethod
    def _construct(
        msg: Union[str, Mapping,
                   Iterable[Mapping]]) -> Iterable[MessageSegment]:
        raise NotImplementedError
