from enum import Enum
from typing import Any, List, Dict, Type, Iterable, Optional, Union

from pydantic import validate_arguments

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment
from nonebot.typing import overrides


class MessageType(str, Enum):
    """消息类型枚举类"""
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


class MessageSegment(BaseMessageSegment["MessageChain"]):
    """
    Mirai-API-HTTP 协议 MessageSegment 适配。具体方法参考 `mirai-api-http 消息类型`_

    .. _mirai-api-http 消息类型:
        https://github.com/project-mirai/mirai-api-http/blob/master/docs/MessageType.md
    """

    type: MessageType
    data: Dict[str, Any]

    @classmethod
    def get_message_class(cls) -> Type["MessageChain"]:
        return MessageChain

    @validate_arguments
    @overrides(BaseMessageSegment)
    def __init__(self, type: MessageType, **data: Any):
        super().__init__(type=type,
                         data={k: v for k, v in data.items() if v is not None})

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        return self.data['text'] if self.is_text() else repr(self)

    def __repr__(self) -> str:
        return '[mirai:%s]' % ','.join([
            self.type.value,
            *map(
                lambda s: '%s=%r' % s,
                self.data.items(),
            ),
        ])

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == MessageType.PLAIN

    def as_dict(self) -> Dict[str, Any]:
        """导出可以被正常json序列化的结构体"""
        return {'type': self.type.value, **self.data}

    @classmethod
    def source(cls, id: int, time: int):
        return cls(type=MessageType.SOURCE, id=id, time=time)

    @classmethod
    def quote(cls, id: int, group_id: int, sender_id: int, target_id: int,
              origin: "MessageChain"):
        """
        :说明:

          生成回复引用消息段

        :参数:

          * ``id: int``: 被引用回复的原消息的message_id
          * ``group_id: int``: 被引用回复的原消息所接收的群号，当为好友消息时为0
          * ``sender_id: int``: 被引用回复的原消息的发送者的QQ号
          * ``target_id: int``: 被引用回复的原消息的接收者者的QQ号（或群号）
          * ``origin: MessageChain``: 被引用回复的原消息的消息链对象
        """
        return cls(type=MessageType.QUOTE,
                   id=id,
                   groupId=group_id,
                   senderId=sender_id,
                   targetId=target_id,
                   origin=origin.export())

    @classmethod
    def at(cls, target: int):
        """
        :说明:

          @某个人

        :参数:

          * ``target: int``: 群员QQ号
        """
        return cls(type=MessageType.AT, target=target)

    @classmethod
    def at_all(cls):
        """
        :说明:

          @全体成员
        """
        return cls(type=MessageType.AT_ALL)

    @classmethod
    def face(cls, face_id: Optional[int] = None, name: Optional[str] = None):
        """
        :说明:

          发送QQ表情

        :参数:

          * ``face_id: Optional[int]``: QQ表情编号，可选，优先高于name
          * ``name: Optional[str]``: QQ表情拼音，可选
        """
        return cls(type=MessageType.FACE, faceId=face_id, name=name)

    @classmethod
    def plain(cls, text: str):
        """
        :说明:

          纯文本消息

        :参数:

          * ``text: str``: 文字消息
        """
        return cls(type=MessageType.PLAIN, text=text)

    @classmethod
    def image(cls,
              image_id: Optional[str] = None,
              url: Optional[str] = None,
              path: Optional[str] = None):
        """
        :说明:

          图片消息

        :参数:

          * ``image_id: Optional[str]``: 图片的image_id，群图片与好友图片格式不同。不为空时将忽略url属性
          * ``url: Optional[str]``: 图片的URL，发送时可作网络图片的链接
          * ``path: Optional[str]``: 图片的路径，发送本地图片
        """
        return cls(type=MessageType.IMAGE, imageId=image_id, url=url, path=path)

    @classmethod
    def flash_image(cls,
                    image_id: Optional[str] = None,
                    url: Optional[str] = None,
                    path: Optional[str] = None):
        """
        :说明:

          闪照消息

        :参数:

          同 ``image``
        """
        return cls(type=MessageType.FLASH_IMAGE,
                   imageId=image_id,
                   url=url,
                   path=path)

    @classmethod
    def voice(cls,
              voice_id: Optional[str] = None,
              url: Optional[str] = None,
              path: Optional[str] = None):
        """
        :说明:

          语音消息

        :参数:

          * ``voice_id: Optional[str]``: 语音的voice_id，不为空时将忽略url属性
          * ``url: Optional[str]``: 语音的URL，发送时可作网络语音的链接
          * ``path: Optional[str]``: 语音的路径，发送本地语音
        """
        return cls(type=MessageType.FLASH_IMAGE,
                   imageId=voice_id,
                   url=url,
                   path=path)

    @classmethod
    def xml(cls, xml: str):
        """
        :说明:

          XML消息

        :参数:

          * ``xml: str``: XML文本
        """
        return cls(type=MessageType.XML, xml=xml)

    @classmethod
    def json(cls, json: str):
        """
        :说明:

          Json消息

        :参数:

          * ``json: str``: Json文本
        """
        return cls(type=MessageType.JSON, json=json)

    @classmethod
    def app(cls, content: str):
        """
        :说明:

          应用程序消息

        :参数:

          * ``content: str``: 内容
        """
        return cls(type=MessageType.APP, content=content)

    @classmethod
    def poke(cls, name: str):
        """
        :说明:

          戳一戳消息

        :参数:

          * ``name: str``: 戳一戳的类型

            * ``Poke``: 戳一戳
            * ``ShowLove``: 比心
            * ``Like``: 点赞
            * ``Heartbroken``: 心碎
            * ``SixSixSix``: 666
            * ``FangDaZhao``: 放大招

        """
        return cls(type=MessageType.POKE, name=name)


class MessageChain(BaseMessage[MessageSegment]):
    """
    Mirai 协议 Message 适配

    由于Mirai协议的Message实现较为特殊, 故使用MessageChain命名
    """

    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @overrides(BaseMessage)
    def __init__(self, message: Union[List[Dict[str,
                                                Any]], Iterable[MessageSegment],
                                      MessageSegment, str], **kwargs):
        super().__init__(**kwargs)
        if isinstance(message, MessageSegment):
            self.append(message)
        elif isinstance(message, str):
            self.append(MessageSegment.plain(text=message))
        elif isinstance(message, Iterable):
            self.extend(self._construct(message))
        else:
            raise ValueError(
                f'Type {type(message).__name__} is not supported in mirai adapter.'
            )

    @overrides(BaseMessage)
    def _construct(
        self, message: Union[List[Dict[str, Any]], Iterable[MessageSegment]]
    ) -> List[MessageSegment]:
        if isinstance(message, str):
            raise ValueError(
                "String operation is not supported in mirai adapter")
        return [
            *map(
                lambda x: x
                if isinstance(x, MessageSegment) else MessageSegment(**x),
                message)
        ]

    def export(self) -> List[Dict[str, Any]]:
        """导出为可以被正常json序列化的数组"""
        return [
            *map(lambda segment: segment.as_dict(), self.copy())  # type: ignore
        ]

    def extract_first(self, *type: MessageType) -> Optional[MessageSegment]:
        """
        :说明:

          弹出该消息链的第一个消息

        :参数:

          * `*type: MessageType`: 指定的消息类型, 当指定后如类型不匹配不弹出
        """
        if not len(self):
            return None
        first: MessageSegment = self[0]
        if (not type) or (first.type in type):
            return self.pop(0)
        return None

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {[*self.copy()]}>'
