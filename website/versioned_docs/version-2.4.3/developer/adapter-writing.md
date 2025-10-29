---
sidebar_position: 1
description: 编写适配器对接新的平台
---

# 编写适配器

在编写适配器之前，我们需要先了解[适配器的功能与组成](../advanced/adapter#适配器功能与组成)，适配器通常由 `Adapter`、`Bot`、`Event` 和 `Message` 四个部分组成，在编写适配器时，我们需要继承 NoneBot 中的基类，并根据实际平台来编写每个部分功能。

## 组织结构

NoneBot 适配器项目通常以 `nonebot-adapter-{adapter-name}` 作为项目名，并以**命名空间包**的形式编写，即在 `nonebot/adapters/{adapter-name}` 目录中编写实际代码，例如：

```tree
📦 nonebot-adapter-{adapter-name}
├── 📂 nonebot
│   ├── 📂 adapters
│   │   ├── 📂 {adapter-name}
│   │   │   ├── 📜 __init__.py
│   │   │   ├── 📜 adapter.py
│   │   │   ├── 📜 bot.py
│   │   │   ├── 📜 config.py
│   │   │   ├── 📜 event.py
│   │   │   └── 📜 message.py
├── 📜 pyproject.toml
└── 📜 README.md
```

:::tip 提示

上述的项目结构仅作推荐，不做强制要求，保证实际可用性即可。

:::

### 使用 NB-CLI 创建项目

我们可以使用脚手架快速创建项目：

```shell
nb adapter create
```

按照指引，输入适配器名称以及存储位置，即可创建一个带有基本结构的适配器项目。

## 组成部分

:::tip 提示

本章节的代码中提到的 `Adapter`、`Bot`、`Event` 和 `Message` 等，均为下文中适配器所编写的类，而非 NoneBot 中的基类。

:::

### Log

适配器在处理时通常需要打印日志，但直接使用 NoneBot 的默认 `logger` 不方便区分适配器输出和其它日志。因此我们可以使用 NoneBot 提供的 `logger_wrapper` 方法，自定义一个 `log` 函数用于快捷打印适配器日志：

```python {3} title=log.py
from nonebot.utils import logger_wrapper

log = logger_wrapper("your_adapter_name")
```

这个 `log` 函数会在默认 `logger` 中添加适配器名称前缀，它接收三个参数：日志等级、日志内容以及可选的异常，具体用法如下：

```python
from .log import log

log("DEBUG", "A DEBUG log.")
log("INFO", "A INFO log.")

try:
    ...
except Exception as e:
    log("ERROR", "something error.", e)
```

### Config

通常适配器需要一些配置项，例如平台连接密钥等。适配器的配置方法与[插件配置](../appendices/config#%E6%8F%92%E4%BB%B6%E9%85%8D%E7%BD%AE)类似，例如：

```python title=config.py
from pydantic import BaseModel

class Config(BaseModel):
    xxx_id: str
    xxx_token: str
```

配置项的读取将在下方 [Adapter](#adapter) 中介绍。

### Adapter

Adapter 负责转换事件、调用接口，以及正确创建 Bot 对象并注册到 NoneBot 中。在编写平台相关内容之前，我们需要继承基类，并实现适配器的基本信息：

```python {9,11,14,18} title=adapter.py
from typing import Any
from typing_extensions import override

from nonebot.drivers import Driver
from nonebot import get_plugin_config
from nonebot.adapters import Adapter as BaseAdapter

from .config import Config

class Adapter(BaseAdapter):
    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        # 读取适配器所需的配置项
        self.adapter_config: Config = get_plugin_config(Config)

    @classmethod
    @override
    def get_name(cls) -> str:
        """适配器名称"""
        return "your_adapter_name"
```

#### 与平台交互

NoneBot 提供了多种 [Driver](../advanced/driver) 来帮助适配器进行网络通信，主要分为客户端和服务端两种类型。我们需要**根据平台文档和特性**选择合适的通信方式，并编写相关方法用于初始化适配器，与平台建立连接和进行交互：

##### 客户端通信方式

```python {12,23,24} title=adapter.py
import asyncio
from typing_extensions import override

from nonebot import get_plugin_config
from nonebot.exception import WebSocketClosed
from nonebot.drivers import Request, WebSocketClientMixin

class Adapter(BaseAdapter):
    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.adapter_config: Config = get_plugin_config(Config)
        self.task: Optional[asyncio.Task] = None  # 存储 ws 任务
        self.setup()

    def setup(self) -> None:
        if not isinstance(self.driver, WebSocketClientMixin):
            # 判断用户配置的Driver类型是否符合适配器要求，不符合时应抛出异常
            raise RuntimeError(
                f"Current driver {self.config.driver} doesn't support websocket client connections!"
                f"{self.get_name()} Adapter need a WebSocket Client Driver to work."
            )
        # 在 NoneBot 启动和关闭时进行相关操作
        self.driver.on_startup(self.startup)
        self.driver.on_shutdown(self.shutdown)

    async def startup(self) -> None:
        """定义启动时的操作，例如和平台建立连接"""
        self.task = asyncio.create_task(self._forward_ws())  # 建立 ws 连接

    async def _forward_ws(self):
        request = Request(
            method="GET",
            url="your_platform_websocket_url",
            headers={"token": "..."},  # 鉴权请求头
        )
        while True:
            try:
                async with self.websocket(request) as ws:
                    try:
                        # 处理 websocket
                        ...
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
                        # 这里要断开 Bot 连接
            except Exception as e:
                # 尝试重连
                log(
                    "ERROR",
                    "<r><bg #f8bbd0>Error while setup websocket to "
                    "platform_websocket_url. Trying to reconnect...</bg #f8bbd0></r>",
                    e,
                )
                await asyncio.sleep(3)  # 重连间隔

    async def shutdown(self) -> None:
        """定义关闭时的操作，例如停止任务、断开连接"""

        # 断开 ws 连接
        if self.task is not None and not self.task.done():
            self.task.cancel()
```

##### 服务端通信方式

```python {30,38} title=adapter.py
from nonebot import get_plugin_config
from nonebot.drivers import (
    Request,
    ASGIMixin,
    WebSocket,
    HTTPServerSetup,
    WebSocketServerSetup
)

class Adapter(BaseAdapter):
    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.adapter_config: Config = get_plugin_config(Config)
        self.setup()

    def setup(self) -> None:
        if not isinstance(self.driver, ASGIMixin):
            raise RuntimeError(
                f"Current driver {self.config.driver} doesn't support asgi server!"
                f"{self.get_name()} Adapter need a asgi server driver to work."
            )
        # 建立服务端路由
        # HTTP Webhook 路由
        http_setup = HTTPServerSetup(
            URL("your_webhook_url"),  # 路由地址
            "POST",  # 接收的方法
            "WEBHOOK name",  # 路由名称
            self._handle_http,  # 处理函数
        )
        self.setup_http_server(http_setup)

        # 反向 Websocket 路由
        ws_setup = WebSocketServerSetup(
            URL("your_websocket_url"),  # 路由地址
            "WebSocket name",  # 路由名称
            self._handle_ws,  # 处理函数
        )
        self.setup_websocket_server(ws_setup)


    async def _handle_http(self, request: Request) -> Response:
        """HTTP 路由处理函数，只有一个类型为 Request 的参数，且返回值类型为 Response"""
        ...
        return Response(
            status_code=200,  # 状态码
            headers={"something": "something"},  # 响应头
            content="xxx",  # 响应内容
        )

    async def _handle_ws(self, websocket: WebSocket) -> Any:
        """WebSocket 路由处理函数，只有一个类型为 WebSocket 的参数"""
        ...
```

更多通信交互方式可以参考以下适配器：

- [OneBot](https://github.com/nonebot/adapter-onebot/blob/master/nonebot/adapters/onebot/v11/adapter.py) - `WebSocket 客户端`、`WebSocket 服务端`、`HTTP WEBHOOK`、`HTTP POST`
- [QQ](https://github.com/nonebot/adapter-qq/blob/master/nonebot/adapters/qq/adapter.py) - `WebSocket 服务端`、`HTTP WEBHOOK`
- [Telegram](https://github.com/nonebot/adapter-telegram/blob/beta/nonebot/adapters/telegram/adapter.py) - `HTTP WEBHOOK`

#### 建立 Bot 连接

在与平台建立连接后，我们需要将 [Bot](#bot) 实例化，并调用适配器提供的的 `bot_connect` 方法告知 NoneBot 建立了 Bot 连接。在与平台断开连接或出现某些异常进行重连时，我们需要调用 `bot_disconnect` 方法告知 NoneBot 断开了 Bot 连接。

```python {7,8,11} title=adapter.py
from .bot import Bot

class Adapter(BaseAdapter):

    def _handle_connect(self):
        bot_id = ...  # 通过配置或者平台 API 等方式，获取到 Bot 的 ID
        bot = Bot(self, self_id=bot_id)  # 实例化 Bot
        self.bot_connect(bot)  # 建立 Bot 连接

    def _handle_disconnect(self):
        self.bot_disconnect(bot)  # 断开 Bot 连接
```

#### 转换 Event 事件

在接收到来自平台的事件数据后，我们需要将其转为适配器的 [Event](#event)，并调用 Bot 的 `handle_event` 方法来让 Bot 对事件进行处理：

```python title=adapter.py
import asyncio
from typing import Any, Dict

from nonebot.compat import type_validate_python

from .bot import Bot
from .event import Event
from .log import log

class Adapter(BaseAdapter):

    @classmethod
    def payload_to_event(cls, payload: Dict[str, Any]) -> Event:
        """根据平台事件的特性，转换平台 payload 为具体 Event

        Event 模型继承自 pydantic.BaseModel，具体请参考 pydantic 文档
        """

        # 做一层异常处理，以应对平台事件数据的变更
        try:
            return type_validate_python(your_event_class, payload)
        except Exception as e:
            # 无法正常解析为具体 Event 时，给出日志提示
            log(
                "WARNING",
                f"Parse event error: {str(payload)}",
            )
            # 也可以尝试转为基础 Event 进行处理
            return type_validate_python(Event, payload)


    async def _forward(self, bot: Bot):

        payload: Dict[str, Any]  # 接收到的事件数据
        event = self.payload_to_event(payload)
        # 让 bot 对事件进行处理
        asyncio.create_task(bot.handle_event(event))
```

#### 调用平台 API

我们需要实现 `Adapter` 的 `_call_api` 方法，使开发者能够调用平台提供的 API。如果通过 WebSocket 通信可以通过 `send` 方法来发送数据，如果采用 HTTP 请求，则需要通过 NoneBot 提供的 `Request` 对象，调用 `driver` 的 `request` 方法来发送请求。

```python {11} title=adapter.py
from typing import Any
from typing_extensions import override

from nonebot.drivers import Request, WebSocket

from .bot import Bot

class Adapter(BaseAdapter):

    @override
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        log("DEBUG", f"Calling API <y>{api}</y>")  # 给予日志提示
        platform_data = your_handle_data_method(data)  # 自行将数据转为平台所需要的格式

        # 采用 HTTP 请求的方式，需要构造一个 Request 对象
        request = Request(
            method="GET",  # 请求方法
            url=api,  # 接口地址
            headers=...,  # 请求头，通常需要包含鉴权信息
            params=platform_data,  # 自行处理数据的传输形式
            # json=platform_data,
            # data=platform_data,
        )
        # 发送请求，返回结果
        return await self.driver.request(request)


        # 采用 WebSocket 通信的方式，可以直接调用 send 方法发送数据
        # 通过某种方式获取到 bot 对应的 websocket 对象
        ws: WebSocket = your_get_websocket_method(bot.self_id)

        await ws.send_text(platform_data)  # 发送 str 类型的数据
        await ws.send_bytes(platform_data)  # 发送 bytes 类型的数据
        await ws.send(platform_data)  # 是以上两种方式的合体

        # 接收并返回结果，同样的，也有 str 和 bytes 的区别
        return await ws.receive_text()
        return await ws.receive_bytes()
        return await ws.receive()
```

`调用平台 API` 实现方式具体可以参考以下适配器：

Websocket:

- [OneBot V11](https://github.com/nonebot/adapter-onebot/blob/54270edbbdb2a71332d744f90b1a3d7f4bf6463a/nonebot/adapters/onebot/v11/adapter.py#L167-L177)
- [OneBot V12](https://github.com/nonebot/adapter-onebot/blob/54270edbbdb2a71332d744f90b1a3d7f4bf6463a/nonebot/adapters/onebot/v12/adapter.py#L204-L218)

HTTP:

- [OneBot V11](https://github.com/nonebot/adapter-onebot/blob/54270edbbdb2a71332d744f90b1a3d7f4bf6463a/nonebot/adapters/onebot/v11/adapter.py#L179-L215)
- [OneBot V12](https://github.com/nonebot/adapter-onebot/blob/54270edbbdb2a71332d744f90b1a3d7f4bf6463a/nonebot/adapters/onebot/v12/adapter.py#L220-L266)
- [QQ](https://github.com/nonebot/adapter-qq/blob/dc5d437e101f0e3db542de3300758a035ed7036e/nonebot/adapters/qq/adapter.py#L599-L605)
- [Telegram](https://github.com/nonebot/adapter-telegram/blob/4a8633627e619245516767f5503dec2f58fe2193/nonebot/adapters/telegram/adapter.py#L148-L253)
- [飞书](https://github.com/nonebot/adapter-feishu/blob/f8ab05e6d57a5e9013b944b0d019ca777725dfb0/nonebot/adapters/feishu/adapter.py#L201-L218)

### Bot

Bot 是机器人开发者能够直接获取并使用的核心对象，负责存储平台机器人相关信息，并提供回复事件、调用 API 的上层方法。我们需要继承基类 `Bot`，并实现相关方法：

```python {20,25,34} title=bot.py
from typing import TYPE_CHECKING, Any, Union
from typing_extensions import override

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

    @override
    def __init__(self, adapter: Adapter, self_id: str, **kwargs: Any):
        super().__init__(adapter, self_id)
        self.adapter: Adapter = adapter
        # 一些有关 Bot 的信息也可以在此定义和存储

    async def handle_event(self, event: Event):
        # 根据需要，对事件进行某些预处理，例如：
        # 检查事件是否和机器人有关操作，去除事件消息首尾的 @bot
        # 检查事件是否有回复消息，调用平台 API 获取原始消息的消息内容
        ...
        # 调用 handle_event 让 NoneBot 对事件进行处理
        await handle_event(self, event)

    @override
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

Event 是 NoneBot 中的事件主体对象，所有平台消息在进入处理流程前需要转换为 NoneBot 事件。我们需要继承基类 `Event`，并实现相关方法：

```python {5,8,13,18,23,28,33} title=event.py
from typing_extensions import override

from nonebot.compat import model_dump
from nonebot.adapters import Event as BaseEvent

class Event(BaseEvent):

    @override
    def get_event_name(self) -> str:
        # 返回事件的名称，用于日志打印
        return "event name"

    @override
    def get_event_description(self) -> str:
        # 返回事件的描述，用于日志打印，请注意转义 loguru tag
        return escape_tag(repr(model_dump(self)))

    @override
    def get_message(self):
        # 获取事件消息的方法，根据事件具体实现，如果事件非消息类型事件，则抛出异常
        raise ValueError("Event has no message!")

    @override
    def get_user_id(self) -> str:
        # 获取用户 ID 的方法，根据事件具体实现，如果事件没有用户 ID，则抛出异常
        raise ValueError("Event has no context!")

    @override
    def get_session_id(self) -> str:
        # 获取事件会话 ID 的方法，根据事件具体实现，如果事件没有相关 ID，则抛出异常
        raise ValueError("Event has no context!")

    @override
    def is_tome(self) -> bool:
        # 判断事件是否和机器人有关
        return False
```

然后根据平台消息的类型，编写各种不同的事件，并且注意要根据事件类型实现 `get_type` 方法，具体请参考[事件类型](../advanced/adapter#事件类型)。消息类型事件还应重写 `get_message` 和 `get_user_id` 等方法，例如：

```python {7,16,20,25,34,42} title=event.py
from .message import Message

class HeartbeatEvent(Event):
    """心跳时间，通常为元事件"""

    @override
    def get_type(self) -> str:
        return "meta_event"

class MessageEvent(Event):
    """消息事件"""
    message_id: str
    user_id: str

    @override
    def get_type(self) -> str:
        return "message"

    @override
    def get_message(self) -> Message:
        # 返回事件消息对应的 NoneBot Message 对象
        return self.message

    @override
    def get_user_id(self) -> str:
        return self.user_id

class JoinRoomEvent(Event):
    """加入房间事件，通常为通知事件"""
    user_id: str
    room_id: str

    @override
    def get_type(self) -> str:
        return "notice"

class ApplyAddFriendEvent(Event):
    """申请添加好友事件，通常为请求事件"""
    user_id: str

    @override
    def get_type(self) -> str:
        return "request"
```

### Message

Message 负责正确序列化消息，以便机器人插件处理。我们需要继承 `MessageSegment` 和 `Message` 两个类，并实现相关方法：

```python {9,12,17,22,27,30,36} title=message.py
from typing import Type, Iterable
from typing_extensions import override

from nonebot.utils import escape_tag

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment

class MessageSegment(BaseMessageSegment["Message"]):
    @classmethod
    @override
    def get_message_class(cls) -> Type["Message"]:
        # 返回适配器的 Message 类型本身
        return Message

    @override
    def __str__(self) -> str:
        # 返回该消息段的纯文本表现形式，通常在日志中展示
        return "text of MessageSegment"

    @override
    def is_text(self) -> bool:
        # 判断该消息段是否为纯文本
        return self.type == "text"


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @override
    def get_segment_class(cls) -> Type[MessageSegment]:
        # 返回适配器的 MessageSegment 类型本身
        return MessageSegment

    @staticmethod
    @override
    def _construct(msg: str) -> Iterable[MessageSegment]:
        # 实现从字符串中构造消息数组，如无字符串嵌入格式可直接返回文本类型 MessageSegment
        ...
```

然后根据平台具体的消息类型，来实现各种 `MessageSegment` 消息段，具体可以参考以下适配器：

- [OneBot V11](https://github.com/nonebot/adapter-onebot/blob/54270edbbdb2a71332d744f90b1a3d7f4bf6463a/nonebot/adapters/onebot/v11/message.py#L25-L259)
- [QQ](https://github.com/nonebot/adapter-qq/blob/dc5d437e101f0e3db542de3300758a035ed7036e/nonebot/adapters/qq/message.py#L30-L520)
- [Telegram](https://github.com/nonebot/adapter-telegram/blob/4a8633627e619245516767f5503dec2f58fe2193/nonebot/adapters/telegram/message.py#L13-L414)

## 适配器测试

关于适配器测试相关内容在这里不再展开，开发者可以根据需要进行合适的测试。这里为开发者提供几个常见问题的解决方法：

1. 在测试中无法导入 editable 模式安装的适配器代码。在 pytest 的 `conftest.py` 内添加如下代码：

   ```python title=tests/conftest.py
   from pathlib import Path
   import nonebot.adapters
   nonebot.adapters.__path__.append(  # type: ignore
       str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
   )
   ```

2. 需要计算适配器测试覆盖率，请在 `pyproject.toml` 中添加 pytest 配置：

   ```toml title=pyproject.toml
   [tool.pytest.ini_options]
   addopts = "--cov nonebot/adapters/{adapter-name} --cov-report term-missing"
   ```

## 后续工作

在完成适配器代码的编写后，如果想要将适配器发布到 NoneBot 商店，我们需要将适配器发布到 PyPI 中，然后前往[商店](/store/adapters)页面，切换到适配器页签，点击**发布适配器**按钮，填写适配器相关信息并提交。

另外建议编写适配器文档或者一些插件开发示例，以便其他开发者使用我们的适配器。
