---
sidebar_position: 2
description: 消息段
---

# 通用消息段

## 模型定义

```python
class Segment:
    """基类标注"""
    children: List["Segment"]

class Text(Segment):
    """Text对象, 表示一类文本元素"""
    text: str
    styles: Dict[Tuple[int, int], List[str]]

class At(Segment):
    """At对象, 表示一类提醒某用户的元素"""
    flag: Literal["user", "role", "channel"]
    target: str
    display: Optional[str]

class AtAll(Segment):
    """AtAll对象, 表示一类提醒所有人的元素"""
    here: bool

class Emoji(Segment):
    """Emoji对象, 表示一类表情元素"""
    id: str
    name: Optional[str]

class Media(Segment):
    url: Optional[str]
    id: Optional[str]
    path: Optional[Union[str, Path]]
    raw: Optional[Union[bytes, BytesIO]]
    mimetype: Optional[str]
    name: str

    to_url: ClassVar[Optional[MediaToUrl]]

class Image(Media):
    """Image对象, 表示一类图片元素"""

class Audio(Media):
    """Audio对象, 表示一类音频元素"""
    duration: Optional[int]

class Voice(Media):
    """Voice对象, 表示一类语音元素"""
    duration: Optional[int]

class Video(Media):
    """Video对象, 表示一类视频元素"""

class File(Segment):
    """File对象, 表示一类文件元素"""
    id: str
    name: Optional[str]

class Reply(Segment):
    """Reply对象，表示一类回复消息"""
    id: str
    """此处不一定是消息ID，可能是其他ID，如消息序号等"""
    msg: Optional[Union[Message, str]]
    origin: Optional[Any]

class Reference(Segment):
    """Reference对象，表示一类引用消息。转发消息 (Forward) 也属于此类"""
    id: Optional[str]
    """此处不一定是消息ID，可能是其他ID，如消息序号等"""
    children: List[Union[RefNode, CustomNode]]

class Hyper(Segment):
    """Hyper对象，表示一类超级消息。如卡片消息、ark消息、小程序等"""
    format: Literal["xml", "json"]
    raw: Optional[str]
    content: Optional[Union[dict, list]]

class Other(Segment):
    """其他 Segment"""
    origin: MessageSegment

```

:::tip

或许你注意到了 `Segment` 上有一个 `children` 属性。

这是因为在 [`Satori`](https://satori.js.org/zh-CN/) 协议的规定下，一类元素可以用其子元素来代表一类兼容性消息
（例如，qq 的商场表情在某些平台上可以用图片代替）。

为此，本插件提供了两种方式来表达 "获取子元素" 的方法：

```python
from nonebot_plugin_alconna.builtins.uniseg.chronocat import MarketFace
from nonebot_plugin_alconna import Args, Image, Alconna, select, select_first

# 表示这个指令需要的图片要么直接是 Image 要么是在 MarketFace 元素内的 Image
alc1 = Alconna("make_meme", Args["img", [Image, Image.from_(MarketFace)]])

# 表示这个指令需要的图片会在目标元素下进行搜索，将所有符合 Image 的元素选出来并将第一个作为结果
alc2 = Alconna("make_meme", Args["img", select(Image, index=0)])  # 也可以使用 select_first(Image)
```

:::

## 自定义消息段

`uniseg` 提供了部分方法来允许用户自定义 Segment 的序列化和反序列化：

```python
from dataclasses import dataclass

from nonebot.adapters import Bot
from nonebot.adapters import MessageSegment as BaseMessageSegment
from nonebot.adapters.satori import Custom, Message, MessageSegment

from nonebot_plugin_alconna.uniseg.builder import MessageBuilder
from nonebot_plugin_alconna.uniseg.exporter import MessageExporter
from nonebot_plugin_alconna.uniseg import Segment, custom_handler, custom_register


@dataclass
class MarketFace(Segment):
    tabId: str
    faceId: str
    key: str


@custom_register(MarketFace, "chronocat:marketface")
def mfbuild(builder: MessageBuilder, seg: BaseMessageSegment):
    if not isinstance(seg, Custom):
        raise ValueError("MarketFace can only be built from Satori Message")
    return MarketFace(**seg.data)(*builder.generate(seg.children))


@custom_handler(MarketFace)
async def mfexport(exporter: MessageExporter, seg: MarketFace, bot: Bot, fallback: bool):
    if exporter.get_message_type() is Message:
        return MessageSegment("chronocat:marketface", seg.data)(await exporter.export(seg.children, bot, fallback))

```

具体而言，你可以使用 `custom_register` 来增加一个从 MessageSegment 到 Segment 的处理方法；使用 `custom_handler` 来增加一个从 Segment 到 MessageSegment 的处理方法。
