from enum import Enum
from typing import Any, Dict, List, Union, Iterable

from pydantic import validate_arguments

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment
from nonebot.typing import overrides


class MessageType(str, Enum):
    SOURCE = 'Source'
    QUOTE = 'Quote'
    AT = 'At'
    AT_ALL = 'AtAll'
    FACE = 'Face'
    PLAIN = 'Plain'
    IMAGE = 'Image'
    FLASH_IMAGE = 'FlashImage'
    VOICE = 'Voice'
    XML = 'Xml'
    JSON = 'Json'
    APP = 'App'
    POKE = 'Poke'


class MessageSegment(BaseMessageSegment):
    type: MessageType
    data: Dict[str, Any]

    @overrides(BaseMessageSegment)
    @validate_arguments
    def __init__(self, type: MessageType, **data):
        super().__init__(type=type, data=data)

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        if self.is_text():
            return self.data.get('text', '')
        return '[mirai:%s]' % ','.join([
            self.type.value,
            *map(
                lambda s: '%s=%r' % s,
                self.data.items(),
            ),
        ])

    @overrides(BaseMessageSegment)
    def __add__(self, other) -> "MessageChain":
        return MessageChain(self) + other

    @overrides(BaseMessageSegment)
    def __radd__(self, other) -> "MessageChain":
        return MessageChain(other) + self

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == MessageType.PLAIN

    def as_dict(self) -> Dict[str, Any]:
        return {'type': self.type.value, **self.data}


class MessageChain(BaseMessage):

    @overrides(BaseMessage)
    def __init__(self, message: Union[List[Dict[str, Any]], MessageSegment],
                 **kwargs):
        super().__init__(**kwargs)
        if isinstance(message, MessageSegment):
            self.append(message)
        elif isinstance(message, Iterable):
            self.extend(self._construct(message))
        else:
            raise ValueError(
                f'Type {type(message).__name__} is not supported in mirai adapter.'
            )

    @overrides(BaseMessage)
    def _construct(
        self, message: Iterable[Union[Dict[str, Any], MessageSegment]]
    ) -> List[MessageSegment]:
        if isinstance(message, str):
            raise ValueError(
                "String operation is not supported in mirai adapter")
        return [
            *map(
                lambda segment: segment if isinstance(segment, MessageSegment)
                else MessageSegment(**segment), message)
        ]

    def export(self) -> List[Dict[str, Any]]:
        chain: List[Dict[str, Any]] = []
        for segment in self.copy():
            segment: MessageSegment
            chain.append({'type': segment.type.value, **segment.data})
        return chain

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {[*self.copy()]}>'
