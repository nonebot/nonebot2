# NoneBot.typing 模块

## 类型

下面的文档中，「类型」部分使用 Python 的 Type Hint 语法，见 [PEP 484](https://www.python.org/dev/peps/pep-0484/)、[PEP 526](https://www.python.org/dev/peps/pep-0526/) 和 [typing](https://docs.python.org/3/library/typing.html)。

除了 Python 内置的类型，下面还出现了如下 NoneBot 自定类型，实际上它们是 Python 内置类型的别名。

以下类型均可从 nonebot.typing 模块导入。


### `Bot`


* **类型**

    BaseBot



* **说明**

    所有 Bot 的基类。


alias of TypeVar('Bot')


### `Driver`


* **类型**

    BaseDriver



* **说明**

    所有 Driver 的基类。


alias of TypeVar('Driver')


### `Event`


* **类型**

    BaseEvent



* **说明**

    所有 Event 的基类。


alias of TypeVar('Event')


### `Message`


* **类型**

    BaseMessage



* **说明**

    所有 Message 的基类。


alias of TypeVar('Message')


### `MessageSegment`


* **类型**

    BaseMessageSegment



* **说明**

    所有 MessageSegment 的基类。


alias of TypeVar('MessageSegment')


### `PreProcessor`


* **类型**

    Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]



* **说明**

    消息预处理函数 PreProcessor 类型


alias of Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]


### `WebSocket`


* **类型**

    BaseWebSocket



* **说明**

    所有 WebSocket 的基类。


alias of TypeVar('WebSocket')
