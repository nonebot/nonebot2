from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Union

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
        super().__init__(type=type,
                         data={k: v for k, v in data.items() if v is not None})

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

    @classmethod
    def source(cls, id: int, time: int):
        return cls(type=MessageType.SOURCE, id=id, time=time)

    @classmethod
    def quote(cls, id: int, group_id: int, sender_id: int, target_id: int,
              origin: "MessageChain"):
        return cls(type=MessageType.QUOTE,
                   id=id,
                   groupId=group_id,
                   senderId=sender_id,
                   targetId=target_id,
                   origin=origin.export())

    @classmethod
    def at(cls, target: int):
        return cls(type=MessageType.AT, target=target)

    @classmethod
    def at_all(cls):
        return cls(type=MessageType.AT_ALL)

    @classmethod
    def face(cls, face_id: Optional[int] = None, name: Optional[str] = None):
        return cls(type=MessageType.FACE, faceId=face_id, name=name)

    @classmethod
    def plain(cls, text: str):
        return cls(type=MessageType.PLAIN, text=text)

    @classmethod
    def image(cls,
              image_id: Optional[str] = None,
              url: Optional[str] = None,
              path: Optional[str] = None):
        return cls(type=MessageType.IMAGE, imageId=image_id, url=url, path=path)

    @classmethod
    def flash_image(cls,
                    image_id: Optional[str] = None,
                    url: Optional[str] = None,
                    path: Optional[str] = None):
        return cls(type=MessageType.FLASH_IMAGE,
                   imageId=image_id,
                   url=url,
                   path=path)

    @classmethod
    def voice(cls,
              voice_id: Optional[str] = None,
              url: Optional[str] = None,
              path: Optional[str] = None):
        return cls(type=MessageType.FLASH_IMAGE,
                   imageId=voice_id,
                   url=url,
                   path=path)

    @classmethod
    def xml(cls, xml: str):
        return cls(type=MessageType.XML, xml=xml)

    @classmethod
    def json(cls, json: str):
        return cls(type=MessageType.JSON, json=json)

    @classmethod
    def app(cls, content: str):
        return cls(type=MessageType.APP, content=content)

    @classmethod
    def poke(cls, name: str):
        return cls(type=MessageType.POKE, name=name)


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
        return [
            *map(lambda segment: segment.as_dict(), self.copy())  # type: ignore
        ]

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {[*self.copy()]}>'
