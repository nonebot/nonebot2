---
sidebar_position: 2
description: 消息段
---

# 通用消息段

通用消息段是对各适配器中的消息段的抽象总结。其可用于 Alconna 命令的参数定义，也可用于消息的构建和解析。

```python
from nonebot_plugin_alconna import Alconna, Args, Image, on_alconna

meme = on_alconna(Alconna("make_meme", Args["name", str]["img", Image]))

@meme.handle()
async def _(img: Image):
    ...
```

## 模型定义

> **注意**: 本节的内容经过简化。实际情况以源码为准。

```python
class Segment:
    """基类标注"""
    @property
    def type(self) -> str: ...
    @property
    def data(self) -> [str, Any]: ...
    @property
    def children(self) -> list["Segment"]: ...

class Text(Segment):
    """Text对象, 表示一类文本元素"""
    text: str
    styles: dict[tuple[int, int], list[str]]

    def cover(self, text: str): ...
    def mark(self, start: Optional[int] = None, end: Optional[int] = None, *styles: str): ...

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
    id: Optional[str]
    url: Optional[str]
    path: Optional[Union[str, Path]]
    raw: Optional[Union[bytes, BytesIO]]
    mimetype: Optional[str]
    name: str

    to_url: ClassVar[Optional[MediaToUrl]]

class Image(Media):
    """Image对象, 表示一类图片元素"""
    width: Optional[int]
    height: Optional[int]

class Audio(Media):
    """Audio对象, 表示一类音频元素"""
    duration: Optional[float]

class Voice(Media):
    """Voice对象, 表示一类语音元素"""
    duration: Optional[float]

class Video(Media):
    """Video对象, 表示一类视频元素"""
    thumbnail: Optional[Image]
    duration: Optional[float]

class File(Media):
    """File对象, 表示一类文件元素"""

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

class Reference(Segment):
    """Reference对象，表示一类引用消息。转发消息 (Forward) 也属于此类"""
    id: Optional[str]
    nodes: Sequence[Union[RefNode, CustomNode]]

class Button(Segment):
    """Button对象，表示一类按钮消息"""
    flag: Literal["action", "link", "input", "enter"]
    """
    - 点击 action 类型的按钮时会触发一个关于 按钮回调 事件，该事件的 button 资源会包含上述 id
    - 点击 link 类型的按钮时会打开一个链接或者小程序，该链接的地址为 `url`
    - 点击 input 类型的按钮时会在用户的输入框中填充 `text`
    - 点击 enter 类型的按钮时会直接发送 `text`
    """
    label: Union[str, Text]
    """按钮上的文字"""
    clicked_label: Optional[str]
    """点击后按钮上的文字"""
    id: Optional[str]
    url: Optional[str]
    text: Optional[str]
    style: Optional[str]
    """
    仅建议使用下列值：primary, secondary, success, warning, danger, info, link, grey, blue

    此处规定 `grey` 与 `secondary` 等同, `blue` 与 `primary` 等同
    """
    permission: Union[Literal["admin", "all"], list[At]] = "all"
    """
    - admin: 仅管理者可操作
    - all: 所有人可操作
    - list[At]: 指定用户/身份组可操作
    """

class Keyboard(Segment):
    """Keyboard对象，表示一行按钮元素"""
    id: Optional[str]
    """此处一般用来表示模板id，特殊情况下可能表示例如 bot_appid 等"""
    buttons: Optional[list[Button]]
    row: Optional[int]
    """当消息中只写有一个 Keyboard 时可根据此参数约定按钮组的列数"""

class Other(Segment):
    """其他 Segment"""
    origin: MessageSegment

class I18n(Segment):
    """特殊的 Segment，用于 i18n 消息"""
    item_or_scope: Union[LangItem, str]
    type_: Optional[str] = None

    def tp(self) -> UniMessageTemplate: ...
```

:::tip

或许你注意到了 `Segment` 上有一个 `children` 属性。

这是因为在 [`Satori`](https://satori.js.org/zh-CN/) 协议的规定下，一类元素可以用其子元素来代表一类兼容性消息
（例如，qq 的商场表情在某些平台上可以用图片代替）。

为此，本插件提供了 `select` 方法来表达 "命令中获取子元素" 的方法：

```python
from nonebot_plugin_alconna import Args, Image, Alconna, select
from nonebot_plugin_alconna.builtins.uniseg.market_face import MarketFace

# 表示这个指令需要的图片会在目标元素下进行搜索，将所有符合 Image 的元素选出来并将第一个作为结果
alc1 = Alconna("make_meme", Args["name", str]["img", select(Image).first])  # 也可以使用 select(Image).nth(0)

# 表示这个指令需要的图片要么直接是 Image 要么是在 MarketFace 元素内的 Image
alc2 = Alconna("make_meme", Args["name", str]["img", [Image, select(Image).from_(MarketFace)]])
```

也可以参考通用消息的 [`嵌套提取`](./message.mdx#嵌套提取)

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
