---
sidebar_position: 1
description: 编写适配器对接新的平台
---

# 编写适配器

在编写适配器之前，我们需要先了解[适配器的功能与组成](../advanced/adapter#适配器功能与组成)，适配器通常由`Adapter`、`Bot`、`Event`和`Message`四个部分组成，在编写适配器时，我们需要继承 NoneBot 中的基类，并根据实际平台来编写每个部分功能。

## 组织结构

NoneBot 适配器项目通常以`nonebot-adapter-{adapter-name}`作为项目名，并以**命名空间包**的形式编写，即在`nonebot/adapters/{adapter-name}`目录中编写实际代码，例如：

```tree
📦 nonebot-adapter-{adapter-name}
├── 📂 nonebot
│   ├── 📂 adapters
│   │   ├── 📂 {adapter-name}
│   │   │   ├── 📜 __init__.py
│   │   │   ├── 📜 adapter.py
│   │   │   ├── 📜 bot.py
│   │   │   └── 📜 config.py
│   │   │   ├── 📜 event.py
│   │   │   ├── 📜 message.py
├── 📜 pyproject.toml
└── 📜 README.md
```

:::tip 提示

本段所述的项目结构仅作推荐，不做强制要求，保证实际可用性即可。

:::

## 组成部分

:::tip 提示

本章节的代码中提到的`Adapter`、`Bot`、`Event`和`Message`等，均为下文由我们适配器所编写的类，而非`NoneBot`中的基类。

:::

### Log

适配器在处理时通常需要打印日志，但使用 NoneBot 的默认`logger`的话，不方便区分适配器和其它的日志。

因此我们要使用 NoneBot 提供的方法，自定义一个`log`用于专门打印适配器的日志：

```python {3} title=log.py
from nonebot.utils import logger_wrapper

log = logger_wrapper("your_adapter_name")
```

这个`log`会在默认`logger`中添加适配器名称前缀，它接收两个参数，第一个是日志等级，第二个是日志内容，具体用法如下：

```python
from .log import log

log("DEBUG", "A DEBUG log.")
log("INFO", "A INFO log.")

try:
    ...
except Exception:
    log("EXCEPTION", "something error.")
```

### Config

通常适配器需要一些配置项，例如平台连接密钥等，参考[插件配置](../appendices/config#%E6%8F%92%E4%BB%B6%E9%85%8D%E7%BD%AE)，定义用于适配器的配置模型，例如：

```python title=config.py
from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    xxx_id: str
    xxx_token: str
```

配置项的读取将在下方[Adapter](#adapter)中介绍。

### Adapter

Adapter 负责转换事件和调用接口，正确创建 Bot 对象并注册到 NoneBot 中。

我们需要继承基类`Adapter`，并实现相关方法：

```python {8,11,14,18} title=adapter.py
from typing import Any
from nonebot.typing import overrides
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.drivers import Driver

from .config import Config

class Adapter(BaseAdapter):

    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        # 读取适配器所需的配置项
        self.adapter_config: Config = Config(**self.config.dict())

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        """适配器名称"""
        return "your_adapter_name"

```

#### 与平台交互

NoneBot 提供了多种[Driver](../advanced/driver)来帮助适配器进行网络通信，主要分为客户端和服务端两种类型，具体包括以下几种：

- HTTP 服务端（WebHook）
- WebSocket 服务端
- HTTP 客户端
- WebSocket 客户端

我们需要**根据平台文档和特性**选择合适的`Driver`，并编写相关函数用于初始化适配器，与平台建立连接和进行交互：

```python {8,10} title=adapter.py
from nonebot.drivers import ForwardDriver

class Adapter(BaseAdapter):
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.platform_config: Config = Config(**self.config.dict())
        self.setup()

    def setup(self) -> None:
        if not isinstance(self.driver, ForwardDriver):
            # 判断用户配置的Driver类型是否符合适配器要求
            # 不符合时应抛出异常，这里以 ForwardDriver 为例
            raise RuntimeError(
                f"Current driver {self.config.driver} doesn't support forward connections!"
                f"{self.get_name()} Adapter need a ForwardDriver to work."
            )
        # 如果需要在 NoneBot 启动和关闭时进行某些操作，则需要添加以下代码
        self.driver.on_startup(self.startup)
        self.driver.on_shutdown(self.shutdown)


    async def startup(self) -> None:
        """定义启动时的操作，例如和平台建立连接"""
        ...

    async def shutdown(self) -> None:
        """定义关闭时的操作，例如停止任务、断开连接"""
        ...
```

#### `Bot`连接

在与平台建立连接时，我们需要将[Bot](#bot)实例化，并调用`Adapter`的`bot_connect`方法告知 NoneBot 建立了`Bot`连接;

在与平台断开连接或出现某些异常，需要移除`Bot`时，我们要调用`bot_disconnect`方法告知 NoneBot 断开了`Bot`连接：

```python {7,8,11} title=adapter.py
from .bot import Bot

class Adapter(BaseAdapter):

    def _handle_connect(self):
        bot_id = ...  # 通过配置或者平台API等方式，获取到 Bot 的 ID
        bot = Bot(self, self_id=bot_id)  # 实例化 Bot
        self.bot_connect(bot)  # 建立 Bot 连接

    def _handle_disconnect(self):
        self.bot_disconnect(bot)  # 断开 Bot 连接
```

#### 处理`Event`事件

在接收到来自平台的事件数据后，我们需要将其转为适配器的[Event](#event)，并调用`Bot`的`handle_event`方法来让`Bot`对事件进行处理：

```python title=adapter.py
import asyncio
from pydantic
from .bot import Bot
from .event import Event

class Adapter(BaseAdapter):

    @classmethod
    def payload_to_event(cls, payload: Dict[str, Any]) -> Event:
        """转换平台 payload 为具体 Event"""

        # Event 继承自 pydantic.BaseModel，可以使用 parse_obj 等方法
        # 以下是一个供参考的处理：
        # 编写一个以事件类型作为键，事件 Model 作为值的事件类型字典
        event_classes: Dict[str, Type[Event]]
        event_type = payload.get("event_type", None)
        event_class = event_classes.get(event_type, None)
        # 做一层异常处理，以应对平台事件数据的变更
        try:
            if not event_class:
                # 未知的事件类型，需要给出日志提示并转为基础 Event
                log(
                    "WARNING",
                    f"Unknown payload type: {event_type}, detail: {str(payload)}",
                )
                return Event.parse_obj(payload)
            return event_class.parse_obj(payload)
        except Exception as e:
            # 无法正常解析为具体 Event 时，需要给出日志提示
            log(
                "WARNING",
                f"Parse event error: {str(payload)}",
            )
            # 也可以尝试转为基础 Event 进行处理
            # return Event.parse_obj(payload)


    async def _forward(self, bot: Bot):

        payload: Dict[str, Any]  # 接收到的事件数据
        event = self.payload_to_event(payload)
        # 让 bot 对事件进行处理
        asyncio.create_task(bot.handle_event(event))

```

#### 调用平台API

我们需要实现`Adapter`的`_call_api`方法，使适配器能够调用平台提供的API。

具体为将请求构造为 NoneBot 提供的`Request`对象，调用`adapter`的`request`方法来发送请求。

```python {8,19} title=adapter.py
from typing import Dict, Callable

from nonebot.drivers import Request

class Adapter(BaseAdapter):

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        log("DEBUG", f"Calling API <y>{api}</y>")  # 给予日志提示
        request = Request(
            method="GET",  # 请求方法
            url=api,  # 接口地址
            headers=...,  # 请求头，通常需要包含鉴权信息
            params=data,  # 自行处理数据的传输形式
            # json=data,
            # data=data,
        )
        # 发送请求，返回结果
        return await self.adapter.request(request)


        # 或者预先编写一系列API处理函数，例如：
        API_HANDLERS: Dict[str, Callable]
        if (api_handler := API_HANDLERS.get(api)) is None:
            # 没有该API处理函数时抛出异常
            raise RuntimeError(f"Api {api} Not Available")
        # 在这些处理函数中，应一样通过 adapter.request 方法发送请求
        return await api_handler(self, bot, **data)
```

`调用平台API`实现方式具体可以参考以下适配器：

- [OneBot](https://github.com/nonebot/adapter-onebot/blob/master/nonebot/adapters/onebot/v11/adapter.py#L126-L182)
- [QQGuild](https://github.com/nonebot/adapter-qqguild/blob/master/nonebot/adapters/qqguild/adapter.py#L353-L359)

#### 示例参考

以下提供部分网络通信方式示例，仅供参考：

<details>
<summary>Websocket 客户端</summary>

`Websocket 客户端`需要一个支持 WebSocket 的`ForwardDriver`类型的驱动器，例如`aiohttp`和`websockets`

```python title=adapter.py
import asyncio
import json
from typing import Optional, Dict, Any

from nonebot.typing import overrides
from nonebot.exception import WebSocketClosed
from nonebot.drivers import Driver, ForwardDriver, Request

from nonebot.adapters import Adapter as BaseAdapter

from .bot import Bot
from .config import Config
from .event import Event
from .log import log


class Adapter(BaseAdapter):
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.adapter_config: Config = Config(**self.config.dict())

        # 用于存储 ws 任务
        self.task: Optional[asyncio.Task] = None

        self.setup()

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return "your_adapter_name"

    def setup(self) -> None:
        # 检查 Driver 类型是否符合要求
        if not isinstance(self.driver, ForwardDriver):
            raise RuntimeError(
                f"Current driver {self.config.driver} doesn't support forward connections!"
                "your_platform_name Adapter need a ForwardDriver to work."
            )
        self.driver.on_startup(self.startup)
        self.driver.on_shutdown(self.shutdown)

    async def startup(self):
        # 初始化 Bot
        bot_id = self.adapter_config.bot_id
        bot_token = self.adapter_config.bot_token
        bot = Bot(self, self_id=bot_id, token=bot_token)
        self.bot_connect(bot)

        # 建立 ws 任务
        self.task = asyncio.create_task(self._forward_ws(bot))

    async def shutdown(self):
        if self.task is not None and not self.task.done():
            self.task.cancel()

    async def _forward_ws(self, bot: Bot):
        request = Request(
            method="GET",
            url="your_platform_websocket_url",
            headers={"token": bot.token},
        )
        while True:
            try:
                async with self.websocket(request) as ws:
                    try:
                        # 一些鉴权和心跳操作等，请自行编写
                        ...

                        payload = await ws.receive()  # 接收事件数据
                        payload = json.loads(payload)
                        event = self.payload_to_event(payload)
                        asyncio.create_task(bot.handle_event(event))

                    except WebSocketClosed as e:
                        log(
                            "ERROR",
                            "<r><bg #f8bbd0>WebSocket Closed</bg #f8bbd0></r>",
                            e,
                        )
                    except Exception as e:
                        log(
                            "ERROR",
                            "<r><bg #f8bbd0>Error while process data from "
                            "websocket platform_websocket_url. "
                            "Trying to reconnect...</bg #f8bbd0></r>",
                            e,
                        )
                    finally:
                        self.bot_disconnect(bot)  # 断开Bot链接
            except Exception as e:
                # 尝试重连
                log(
                    "ERROR",
                    "<r><bg #f8bbd0>Error while setup websocket to "
                    "platform_websocket_url. Trying to reconnect...</bg #f8bbd0></r>",
                    e,
                )
                await asyncio.sleep(3)  # 重连间隔

    @classmethod
    def payload_to_event(cls, payload: Dict[str, Any]) -> Event:
        ...

```

</details>

<details>
<summary>HTTP WebHook</summary>

`HTTP WebHook`需要一个`ReverseDriver`类型的驱动器，例如`fastapi`

```python title=adapter.py
import json
import asyncio
from typing import Dict, Any, cast
from nonebot.typing import overrides
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    ReverseDriver,
    HTTPServerSetup,
)

from nonebot.adapters import Adapter as BaseAdapter

from .bot import Bot
from .config import Config
from .event import Event
from .log import log


class Adapter(BaseAdapter):
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.adapter_config: Config = Config(**self.config.dict())
        self.setup()

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return "your_platform_name"

    def setup(self):
        if not isinstance(self.driver, ReverseDriver):
            raise RuntimeError(
                f"Current driver {self.config.driver} doesn't support connections!"
                f"{self.get_name()} Adapter need a ReverseDriver and ReverseDriver to work."
            )
        webhook_url = self.adapter_config.webhook_url

        # 构造一个 HTTP 路由配置
        http_setup = HTTPServerSetup(
            URL(webhook_url),  # 路由地址
            "POST",  # 接受的方法
            "WEBHOOK name",  # 路由名称
            self._handle_http,  # 处理函数
        )
        self.setup_http_server(http_setup)

    async def _handle_http(self, request: Request) -> Response:
        # 定义 HTTP 处理函数，该函数必须只有一个 Request 类型的参数

        # 在此处对接收到到的请求进行处理
        payload = json.loads(request.content)  # 请求内容
        bot_id = payload.get("bot_id", None)  # 从内容中获取bot_id
        if bot_id:
            if (bot := self.bots.get(bot_id, None)) is None:
                # 如果该bot尚未建立连接，则实例化bot并连接
                bot = Bot(self, bot_id)
                self.bot_connect(bot)
            bot = cast(Bot, bot)  # for type checking
            event = self.payload_to_event(payload)
            asyncio.create_task(bot.handle_event(event))
        else:
            log("WARNING", "Missing bot_id in request")

        # 如果平台要求我们收到事件后做出响应，可以返回 Response
        return Response(
            status_code=200,  # 状态码
            headers={"something": "something"},  # 响应头
            content="xxx",  # 响应内容
        )

    @classmethod
    def payload_to_event(cls, payload: Dict[str, Any]) -> Event:
        ...
```

</details>

更多通信交互方式可以参考以下适配器：

- [OneBot](https://github.com/nonebot/adapter-onebot/blob/master/nonebot/adapters/onebot/v11/adapter.py) - `WebSocket 客户端`、`WebSocket 服务端`、`HTTP WEBHOOK`、`HTTP POST`
- [QQGuild](https://github.com/nonebot/adapter-qqguild/blob/master/nonebot/adapters/qqguild/adapter.py) - `WebSocket 服务端`
- [Telegram](https://github.com/nonebot/adapter-telegram/blob/beta/nonebot/adapters/telegram/adapter.py) - `HTTP WEBHOOK`

### Bot

`Bot`负责存储平台机器人相关信息，并提供回复事件的方法。

我们需要继承基类`Bot`，并实现相关方法：

```python {20,25,34} title=bot.py
from typing import TYPE_CHECKING, Any, Union

from nonebot.typing import overrides
from nonebot.message import handle_event

from nonebot.adapters import Bot as BaseBot
from .event import Event
from .message import Message, MessageSegment

if TYPE_CHECKING:
    from .adapter import Adapter


class Bot(BaseBot):
    """
    your_adapter_name 协议 Bot 适配。
    """

    @overrides(BaseBot)
    def __init__(self, adapter: Adapter, self_id: str, **kwargs: Any):
        super().__init__(adapter, self_id)
        self.adapter: Adapter = adapter
        # 一些有关 Bot 的信息也可以在此定义和存储

    async def handle_event(self, event: Event):
        # 根据需要，对事件进行某些预处理，例如：
        # 检查事件是否和机器人有关操作，去除事件消息收尾的@bot
        # 检查事件是否有回复消息，调用平台API获取原始消息的消息内容
        ...
        # 调用 handle_event 让 NoneBot 对事件进行处理
        await handle_event(self, event)

    @overrides(BaseBot)
    async def send(
        self,
        event: Event,
        message: Union[str, Message, MessageSegment],
        **kwargs: Any,
    ) -> Any:
        # 根据平台实现 Bot 回复事件的方法

        # 将消息处理为平台所需的格式后，调用发送消息接口进行发送，例如：
        data = message_to_platform_data(message)
        await self.send_message(
            data=data,
            ...
        )
```

### Event

`Event`负责定义事件内容，以及事件主体对象。

我们需要继承基类`Event`，实现一个适配器的基础`Event`，并实现相关方法：

```python {6,9,14,19,24,29,34} title="event.py"
from nonebot.typing import overrides
from nonebot.utils import escape_tag

from nonebot.adapters import Event as BaseEvent

class Event(BaseEvent):

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        # 返回事件的名称，用于日志打印
        return "event name"

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        # 返回事件的描述，用于日志打印
        return escape_tag(repr(self.dict()))

    @overrides(BaseEvent)
    def get_message(self):
        # 获取事件消息的方法，根据事件具体实现，如果事件非消息类型事件，则抛出异常
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        # 获取用户ID的方法，根据事件具体实现，如果事件没有用户ID，则抛出异常
        raise ValueError("Event has no context!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        # 获取事件会话ID的方法，根据事件具体实现，如果事件没有相关ID，则抛出异常
        raise ValueError("Event has no context!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        # 判断事件是否和机器人有关
        return False
```

然后根据平台所给的事件，编写具体的`Event`，并且注意要实现`get_type`方法，返回事件对应的类型，具体请参考[事件类型](../advanced/adapter#事件类型)，消息类型事件还应重写`get_user_id`方法，例如：

```python {5,14,18,27,35} title=event.py
class HeartbeatEvent(Event):
    """心跳时间，通常为元事件"""

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return "meta_event"

class MessageEvent(Event):
    """消息事件"""
    message_id: str
    user_id: str

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return "message"

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        return self.user_id

class JoinRoomEvent(Event):
    """加入房间事件，通常为通知事件"""
    user_id: str
    room_id: str

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return "notice"

class ApplyAddFriendEvent(Event):
    """申请添加好友事件，通常为请求事件"""
    user_id: str

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return "request"
```

### Message

`Message`负责正确序列化消息，以便机器人插件处理。

我们需要继承`MessageSegment`和`Message`两个类，并实现相关方法：

```python {9,12,17,22,27,30,36} title="message.py"
from typing import Type, Iterable

from nonebot.typing import overrides
from nonebot.utils import escape_tag

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment

class MessageSegment(BaseMessageSegment["Message"]):
    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        # 返回适配器的Message类型本身
        return Message

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        # 返回该消息段的纯文本表现形式，在命令匹配部分使用
        return "text of MessageSegment"

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        # 判断该消息段是否为纯文本
        return self.type == "text"


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> Type[MessageSegment]:
        # 返回适配器的MessageSegment类型本身
        return MessageSegment

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: str) -> Iterable[MessageSegment]:
        # 实现相关方法，从字符串中构造消息数组
        ...
```

然后根据平台具体的消息类型，来实现各种`MessageSegment`消息段，具体可以参考以下适配器：

- [OneBot](https://github.com/nonebot/adapter-onebot/blob/master/nonebot/adapters/onebot/v11/message.py#L77-L261)
- [QQGuild](https://github.com/nonebot/adapter-qqguild/blob/master/nonebot/adapters/qqguild/message.py#L22-L150)

## 后续工作

在完成适配器代码的编写后，如果想要将适配器发布到 NoneBot 商店，我们需要将适配器发布到 PyPI中，前往[商店](https://nonebot.dev/store)页面，切换到适配器页签，点击 **发布适配器** 按钮，填写适配器相关信息并提交。

另外建议编写适配器文档或者一些插件开发示例，以便其他开发者使用我们的适配器。
