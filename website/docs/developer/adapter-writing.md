---
sidebar_position: 1
description: 编写适配器对接新的平台
---

# 编写适配器

在编写适配器之前，您需要了解[适配器的功能与组成](../advanced/adapter#适配器功能与组成)，适配器通常由`Adapter`、`Bot`、`Event`和`Message`四个部分组成，在编写适配器时，您需要继承 NoneBot 中的基类，并根据您的平台来编写每个部分功能。

## 组织结构

适配器项目通常要以**命名空间包**的形式编写，即在`nonebot/adapters/{adapter-name}`目录中编写实际代码，例如：

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
│   │   │   ├── 📜 utils.py
├── 📜 pyproject.toml
└── 📜 README.md
```

当然这并非强制要求，不过我们仍建议您按照这种规范。

:::tip 提示

本章节的代码中提到的`Adapter`、`Bot`、`Event`和`Message`等，均为下文由您适配器所编写的类，而非`NoneBot`中的基类。

:::

## Adapter

继承基类`Adapter`，并实现相关方法：

```python {8,11,15,20} title=adapter.py
from typing import Any
from nonebot.typing import overrides
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.drivers import Driver

from .bot import Bot

class Adapter(BaseAdapter):

    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return "your_adapter_name"

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        # 实际调用 api 的逻辑实现函数，实现该方法以调用 api。
        ...
```

### 日志

使用 NoneBot 提供的方法，自定义一个`log`用于专门打印适配器的日志：

```python title="utils.py"
from nonebot.utils import logger_wrapper

log = logger_wrapper("your_adapter_name")
```

使用方法：

```python {1,6,8} title=adapter.py
from .utils import log

class Adapter(BaseAdapter):
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        log("DEBUG", "adapter init...")
        super().__init__(driver, **kwargs)
        log("INFO", "adapter init!")
```

### 配置

通常适配器需要一些配置项，例如平台连接密钥等，可以参考[插件配置](../appendices/config#%E6%8F%92%E4%BB%B6%E9%85%8D%E7%BD%AE)，定义用于适配器的配置模型，例如：

```python title=config.py
from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
	xxx_id: str
    xxx_token: str
```

然后在`Adapter`的初始化中读取配置项：

```python {1,7} title=adapter.py
from .config import Config

class Adapter(BaseAdapter):
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.platform_config: Config = Config(**self.config.dict())
```

:::tip 提示

注意，不能使用`config`来命名配置，它已被基类`Adapter`所使用，建议使用`平台名_config`或者其他变量名，例如上方例子使用的`platform_config`

:::

### 与平台交互

NoneBot 提供了多种[Driver](../advanced/driver)来帮助适配器进行网络通信，主要包括客户端和服务端两种类型，具体包括以下几种：

- HTTP 服务端（WebHook）
- WebSocket 服务端
- HTTP 客户端
- WebSocket 客户端

您需要**根据平台文档和特性**选择合适的`Driver`，并编写相关函数用于初始化适配器，与平台建立连接和进行交互：

```python {8,10} title="adapter.py"
from nonebot.drivers import ForwardDriver

class Adapter(BaseAdapter):
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.platform_config: Config = Config(**self.config.dict())
        self.setup()

    def setup(self) -> None:
        if not isinstance(self.driver, ForwardDriver):
            # 判断用户配置的Driver类型是否符合您的适配器要求，不符合时应抛出异常
            raise RuntimeError(
                f"Current driver {self.config.driver} doesn't support forward connections!"
                f"{self.get_name()} Adapter need a ForwardDriver to work."
            )
        # 如果适配器需要在nonebot启动和关闭时进行某些操作，则需要添加以下代码
        self.driver.on_startup(self.startup)
        self.driver.on_shutdown(self.shutdown)


    async def startup(self) -> None:
        """定义启动时的操作，例如和平台建立连接"""
        ...

    async def shutdown(self) -> None:
        """定义关闭时的操作，例如停止任务、断开连接"""
        ...
```

### `Bot`连接

在您与平台建立连接时，您需要将[Bot](#bot)实例化，并调用`adapter`的`bot_connect`方法来告知 NoneBot 建立了`Bot`连接，并在断开连接时调用`bot_disconnect`，例如：

```python {7,8,11} title="adapter.py"
from .bot import Bot

class Adapter(BaseAdapter):

    def _handle_connect(self):
        bot_id = ...  # 通过配置或者平台API等方式，获取到Bot的ID
        bot = Bot(self, self_id=bot_id)  # 实例化Bot
        self.bot_connect(bot)  # 建立Bot连接

	def _handle_disconnect(self):
        self.bot_disconnect(bot)  # 断开Bot连接
```

### 处理`Event`事件

在接收到来自平台的事件数据后，您需要将其转为适配器的[Event](#event)，并调用`Bot`的`handle_event`方法来让`Bot`对事件进行处理，例如：

```python {7,26-27} title="adapter.py"
import asyncio
from .event import Event

class Adapter(BaseAdapter):

    @classmethod
    def payload_to_event(cls, payload: Dict[str, Any]) -> Event:
        # 自行编写方法，将payload转为对应的具体Event
        # Event继承自pydantic.BaseModel，意味着您可以使用parse_obj等方法
        # 以下是一个简单示例：
        event_classes: Dict[str, Type[Event]]  # 编写一个事件类型字典
        event_type = payload.get("event_type", None)
        event_class = event_classes.get(event_type, None)
        if not event_class:
            log(
                "WARNING",
                f"Unknown payload type: {event_type}, detail: {str(payload)}",
            )
            # 未知的事件类型，转为基础的Event
            return Event.parse_obj(payload)
       	return event_class.parse_obj(payload)

    async def _forward(self, bot: Bot):
        payload: Dict[str, Any]  # 接收到的事件数据

        event = self.payload_to_event(payload)
        asyncio.create_task(bot.handle_event(event))
```

### 调用平台API

实现`Adapter`的`_call_api`方法，使适配器能够调用平台提供的API，例如：

```python {6,16} title="adapter.py"
from nonebot.drivers import Request

class Adapter(BaseAdapter):

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        log("DEBUG", f"Calling API <y>{api}</y>")
        request = Request(
            method="GET",  # 请求方法自行处理
            url=api,  # 接口地址
            headers=...,  # 请求头，通常需要包含鉴权信息
            params=data,  # 自行处理数据的传输形式
            # json=data,
            # data=data,
        )
        return await self.adapter.request(request)  # 发送请求，返回结果


        # 或者您可以编写一系列API处理函数，例如：
        if (api_handler := API_HANDLERS.get(api)) is None:
            # 没有该API处理函数时抛出异常
            raise ValueError("Api Not Available")
        return await api_handler(self, bot, **data)
```

`调用平台API`实现方式具体可以参考以下适配器：

- [OneBot](https://github.com/nonebot/adapter-onebot/blob/master/nonebot/adapters/onebot/v11/adapter.py#L126-L182)
- [QQGuild](https://github.com/nonebot/adapter-qqguild/blob/master/nonebot/adapters/qqguild/adapter.py#L353-L359)

### 示例参考

以下提供部分网络通信方式示例，仅供参考：

<details>
<summary>Websocket 客户端</summary>

`Websocket 客户端`需要一个`ForwardDriver`类型的驱动器，例如`httpx`和`websockets`

```python title="adapter.py"
import asyncio
from typing import Optional

class Adapter(BaseAdapter):
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.platform_config: Config = Config(**self.config.dict())
        self.task: Optional[asyncio.Task] = None
        self.setup()

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return "your_adapter_name"

    def setup(self) -> None:
        if not isinstance(self.driver, ForwardDriver):
            raise RuntimeError(
                f"Current driver {self.config.driver} doesn't support forward connections!"
                "your_platform_name Adapter need a ForwardDriver to work."
            )
        self.driver.on_startup(self.startup)
        self.driver.on_shutdown(self.shutdown)

    async def startup(self):
        bot_id = self.platform_config.bot_id
        bot_token = self.platform_config.bot_token
        bot = Bot(self, self_id=bot_id, token=bot_token)
        self.bot_connect(bot)
        self.task = asyncio.create_task(self._forward_ws(bot))

    async def shutdown(self):
        if self.task is not None and not self.task.done():
            self.task.cancel()

	async def _forward_ws(self, bot: Bot):
        request = Request(
        	method="GET",
            url="your_platform_websocket_url",
            headers={"token": bot.token}
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
                            "<r><bg #f8bbd0>Error while process data from websocket "
                            f"{escape_tag(str(ws_url))}. Trying to reconnect...</bg #f8bbd0></r>",
                            e,
                        )
                    finally:
                        self.bot_disconnect(bot)  # 断开Bot链接
			except Exception as e:
                log(
                    "ERROR",
                    "<r><bg #f8bbd0>Error while setup websocket to your_platform_websocket_url. Trying to reconnect...</bg #f8bbd0></r>",
                    e,
                )
                await asyncio.sleep(3)  # 重连间隔

```

</details>

<details>
<summary>HTTP WebHook</summary>

`HTTP WebHook`需要一个`ReverseDriver`类型的驱动器，例如`fastapi`

```python title=adapter.py
import json
from typing import cast
from nonebot.drivers import (
    URL,
    Request,
    Response,
    ReverseDriver,
    HTTPServerSetup
)

class Adapter(BaseAdapter):
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.platform_config: Config = Config(**self.config.dict())
        self.setup()

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return "your_platform_name"

    def setup(self):
        # ReverseDriver用于接收回调事件，ForwardDriver用于调用API
        if not isinstance(self.driver, ReverseDriver):
            raise RuntimeError(
                f"Current driver {self.config.driver} doesn't support connections!"
                f"{self.get_name()} Adapter need a ReverseDriver and ReverseDriver to work."
            )
        webhook_url = self.platform_config.webhook_url
        http_setup = HTTPServerSetup(
            URL(webhook_url),  # 路由地址
            "POST",  # 接受的方法
            "WEBHOOK name",  # 路由名称
            self._handle_http,  # 处理函数
        )
        self.setup_http_server(http_setup)

    async def _handle_http(self, request: Request) -> Response:
        # 在此处对接收到到的请求进行处理，最终返回响应
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

        return Response(
        	status_code=200,  # 状态码
            headers={"something": "something"}  # 响应头
            content="xxx"  # 响应内容
            request=Request(...)  # 请求
        )
```

</details>

更多通信交互方式可以参考以下适配器：

- [OneBot](https://github.com/nonebot/adapter-onebot/blob/master/nonebot/adapters/onebot/v11/adapter.py) - `WebSocket 客户端`、`WebSocket 服务端`、`HTTP WEBHOOK`、`HTTP POST`
- [QQGuild](https://github.com/nonebot/adapter-qqguild/blob/master/nonebot/adapters/qqguild/adapter.py) - `WebSocket 服务端`
- [Telegram](https://github.com/nonebot/adapter-telegram/blob/beta/nonebot/adapters/telegram/adapter.py) - `HTTP WEBHOOK`

## Bot

继承基类`Bot`，并实现相关方法：

```python {15,21,26,34} title="bot.py"
from typing import TYPE_CHECKING, Any, Union

from nonebot.typing import overrides
from nonebot.message import handle_event
from nonebot.internal.adapter.adapter import Adapter

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


    async def handle_event(self, event: Event):
        # 根据需要对收到的事件先进行预处理，然后调用handle_event让nonebot对事件进行处理
        if isinstance(event, MessageEvent):
            _check_at_me(self, event)  # 检查事件是否和机器人有关操作
            _check_reply(self, event)  # 检查事件是否有回复消息
        await handle_event(self, event)

    @overrides(BaseBot)
    async def send(
        self,
        event: Event,
        message: Union[str, Message, MessageSegment],
        **kwargs: Any,
    ) -> Any:
        # 根据您的平台实现Bot发送消息的方法
        # 对消息进行一些处理后，调用发送消息接口进行发送
        ...
```

## Event

继承基类`Event`实现一个适配器的`Event`，并实现相关方法：

```python {6,9,14,18,23,28,33} title="event.py"
from nonebot.typing import overrides
from nonebot.utils import escape_tag

from nonebot.adapters import Event as BaseEvent

class Event(BaseEvent):

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        # 返回事件的名称
        return "event name"

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
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

然后根据您的平台所给的事件，来编写具体的`Event`，并且注意要实现`get_type`方法，返回事件对应的类型，具体请参考[事件类型](../advanced/adapter#事件类型)：

```python {5,14,27,35} title="event.py"
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

## Message

需要继承`MessageSegment`和`Message`两个类，并实现相关方法：

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

然后根据您的平台具体的消息类型，来实现各种`MessageSegment`消息段，具体可以参考以下适配器：

- [OneBot](https://github.com/nonebot/adapter-onebot/blob/master/nonebot/adapters/onebot/v11/message.py#LL76-L254)
- [QQGuild](https://github.com/nonebot/adapter-qqguild/blob/master/nonebot/adapters/qqguild/message.py#L22-L150)
