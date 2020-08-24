---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.typing 模块

## 类型

下面的文档中，「类型」部分使用 Python 的 Type Hint 语法，见 [PEP 484](https://www.python.org/dev/peps/pep-0484/)、[PEP 526](https://www.python.org/dev/peps/pep-0526/) 和 [typing](https://docs.python.org/3/library/typing.html)。

除了 Python 内置的类型，下面还出现了如下 NoneBot 自定类型，实际上它们是 Python 内置类型的别名。

以下类型均可从 nonebot.typing 模块导入。


## `Driver`


* **类型**

    BaseDriver



* **说明**

    所有 Driver 的基类。




## `WebSocket`


* **类型**

    BaseWebSocket



* **说明**

    所有 WebSocket 的基类。




## `Bot`


* **类型**

    BaseBot



* **说明**

    所有 Bot 的基类。




## `Event`


* **类型**

    BaseEvent



* **说明**

    所有 Event 的基类。




## `Message`


* **类型**

    BaseMessage



* **说明**

    所有 Message 的基类。




## `MessageSegment`


* **类型**

    BaseMessageSegment



* **说明**

    所有 MessageSegment 的基类。




## `PreProcessor`


* **类型**

    Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]



* **说明**

    消息预处理函数 PreProcessor 类型




## `Matcher`


* **类型**

    Matcher



* **说明**

    Matcher 即响应事件的处理类。通过 Rule 判断是否响应事件，运行 Handler。




## `Rule`


* **类型**

    Rule



* **说明**

    Rule 即判断是否响应事件的处理类。内部存储 RuleChecker ，返回全为 True 则响应事件。




## `RuleChecker`


* **类型**

    Callable[[Bot, Event, dict], Awaitable[bool]]



* **说明**

    RuleChecker 即判断是否响应事件的处理函数。




## `Permission`


* **类型**

    Permission



* **说明**

    Permission 即判断是否响应消息的处理类。内部存储 PermissionChecker ，返回只要有一个 True 则响应消息。




## `PermissionChecker`


* **类型**

    Callable[[Bot, Event], Awaitable[bool]]



* **说明**

    RuleChecker 即判断是否响应消息的处理函数。




## `Handler`


* **类型**

    Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]



* **说明**

    Handler 即事件的处理函数。




## `ArgsParser`


* **类型**

    Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]



* **说明**

    ArgsParser 即消息参数解析函数，在 Matcher.got 获取参数时被运行。
