---
sidebar_position: 4
description: 定义事件处理流程，完成事件响应

options:
  menu:
    weight: 27
    category: guide
---

# 定义事件处理流程

在上一章节中，我们已经定义了事件响应器，在这一章中，我们将会为事件响应器填充处理流程。

## 添加一个处理依赖

在事件响应器中，事件处理流程由一个或多个处理依赖组成，每个处理依赖都是一个 `Dependent`，详情可以参考[进阶 - 依赖注入](../../advanced/di/dependency-injection.md)。下面介绍如何添加一个处理依赖。

### 使用 `handle` 装饰器

```python {3-5}
matcher = on_message()

@matcher.handle()
async def handle_func():
    # do something here
```

如上方示例所示，我们使用 `matcher` 响应器的 `handle` 装饰器装饰了一个函数 `handle_func` 。`handle_func` 函数会被自动转换为 `Dependent` 对象，并被添加到 `matcher` 的事件处理流程中。

在 `handle_func` 函数中，我们可以编写任何事件响应逻辑，如：操作数据库，发送消息等。上下文信息可以通过依赖注入的方式获取，参考：[获取上下文信息](#获取上下文信息)。发送消息可以通过[事件响应器操作](./matcher-operation.md)或者直接调用 Bot 的方法（ API 等，由协议适配器决定）。

:::warning 注意
`handle_func` 函数虽然会被装饰器自动转换为 `Dependent` 对象，但 `handle_func` 仍然为原本的函数，因此 `handle_func` 函数可以进行复用。如：

```python
matcher1 = on_message()
matcher2 = on_message()

@matcher1.handle()
@matcher2.handle()
async def handle_func():
    # do something here
```

:::

### 使用 `receive` 装饰器

```python {3-5}
matcher = on_message()

@matcher.receive("id")
async def handle_func(e: Event = Received("id")):
    # do something here
```

`receive` 装饰器与 `handle` 装饰器一样，可以装饰一个函数添加到事件响应器的事件处理流程中。但与 `handle` 装饰器不同的是，`receive` 装饰器会中断当前事件处理流程，等待接收一个新的事件，就像是会话状态等待用户一个新的事件。可以接收的新的事件类型取决于事件响应器的 [`type`](./create-matcher.md#事件响应器类型-type) 更新值以及 [`permission`](./create-matcher.md#事件触发权限-permission) 更新值，可以通过自定义更新方法来控制会话响应（如进行非消息交互、多人会话、跨群会话等）。

`receive` 装饰器接受一个可选参数 `id`，用于标识当前需要接收的事件，如果不指定，则默认为空 `""`。

在 `handle_func` 函数中，可以通过依赖注入的方式来获取接收到的事件，参考：[`Received`](#received)、[`LastReceived`](#lastreceived)。

:::important 提示
`receive` 装饰器可以和自身与 `got` 装饰器嵌套使用
:::

:::warning 注意
如果存在多个 `receive` 装饰器，则必须指定不相同的多个 `id`；否则相同的 `id` 将会被跳过接收。

```python
matcher = on_message()

@matcher.receive("id1")
@matcher.receive("id2")
async def handle_func():
    # do something here
```

:::

### 使用 `got` 装饰器

```python {3-5}
matcher = on_message()

@matcher.got("key", prompt="Key?")
async def handle_func(key: Message = Arg()):
    # do something here
```

`got` 装饰器与 `receive` 装饰器一样，会中断当前事件处理流程，等待接收一个新的事件。但与 `receive` 装饰器不同的是，`got` 装饰器用于接收一条消息，并且可以控制是否向用户发送询问 `prompt` 等，更贴近于对话形式会话。

`got` 装饰器接受一个参数 `key` 和一个可选参数 `prompt`，当 `key` 不存在时，会向用户发送 `prompt` 消息，并等待用户回复。

在 `handle_func` 函数中，可以通过依赖注入的方式来获取接收到的消息，参考：[`Arg`](#arg)、[`ArgStr`](#argstr)、[`ArgPlainText`](#argplaintext)。

:::important 提示
`got` 装饰器可以和自身与 `receive` 装饰器嵌套使用
:::

### 直接添加

```python {2}
matcher = on_message(
    handlers=[handle_func, or_dependent]
)
```

:::warning 注意
通过该方法添加的处理依赖将会处于整个事件处理流程的最前，因此，如果再使用 `handle` 等装饰器，则会在其之后。
:::

## 事件处理流程

在一个事件响应器中，事件被添加的处理依赖依次执行，直到所有处理依赖都执行完毕，或者遇到了某个处理依赖需要更多的事件来进行下一步的处理。在下一个事件到来并符合响应要求时，继续执行。更多有关 NoneBot 事件分发与处理流程的详细信息，请参考[进阶 - 深入](../../advanced/README.md)。

## 获取上下文信息

在事件处理流程中，事件响应器具有自己独立的上下文，例如：当前的事件、机器人等信息，可以通过依赖注入的方式来获取。

### Bot

获取当前事件的 Bot 对象。

```python {7-9}
from typing import Union

from nonebot.adapters import Bot
from nonebot.adapters.ding import Bot as DingBot
from nonebot.adapters.onebot.v11 import Bot as OneBotV11Bot

async def _(foo: Bot): ...
async def _(foo: Union[DingBot, OneBotV11Bot]): ...
async def _(bot): ...  # 兼容性处理
```

### Event

获取当前事件。

```python {6-8}
from typing import Union

from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent

async def _(foo: Event): ...
async def _(foo: Union[PrivateMessageEvent, GroupMessageEvent]): ...
async def _(event): ...  # 兼容性处理
```

### EventType

获取当前事件的类型。

```python {3}
from nonebot.params import EventType

async def _(foo: str = EventType()): ...
```

### EventMessage

获取当前事件的消息。

```python {4}
from nonebot.adapters import Message
from nonebot.params import EventMessage

async def _(foo: Message = EventMessage()): ...
```

### EventPlainText

获取当前事件的消息纯文本部分。

```python {3}
from nonebot.params import EventPlainText

async def _(foo: str = EventPlainText()): ...
```

### EventToMe

获取当前事件是否与机器人相关。

```python {3}
from nonebot.params import EventToMe

async def _(foo: bool = EventToMe()): ...
```

### State

获取当前事件处理上下文状态，State 为一个字典，用户可以向 State 中添加数据来保存状态等操作。（请注意不要随意覆盖 State 中 NoneBot 的数据）

```python {4}
from nonebot.typing import T_State

async def _(foo: T_State): ...
```

### Command

获取当前命令型消息的元组形式命令名。

```python {7}
from nonebot import on_command
from nonebot.params import Command

matcher = on_command("cmd")

@matcher.handle()
async def _(foo: Tuple[str, ...] = Command()): ...
```

:::tip 提示
命令详情只能在首次接收到命令型消息时获取，如果在事件处理后续流程中获取，则会获取到不同的值。
:::

### RawCommand

获取当前命令型消息的文本形式命令名。

```python {7}
from nonebot import on_command
from nonebot.params import RawCommand

matcher = on_command("cmd")

@matcher.handle()
async def _(foo: str = RawCommand()): ...
```

:::tip 提示
命令详情只能在首次接收到命令型消息时获取，如果在事件处理后续流程中获取，则会获取到不同的值。
:::

### CommandArg

获取命令型消息命令后跟随的参数。

```python {8}
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg

matcher = on_command("cmd")

@matcher.handle()
async def _(foo: Message = CommandArg()): ...
```

:::tip 提示
命令详情只能在首次接收到命令型消息时获取，如果在事件处理后续流程中获取，则会获取到不同的值。
:::

### CommandStart

获取命令型消息命令前缀。

```python {8}
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandStart

matcher = on_command("cmd")

@matcher.handle()
async def _(foo: str = CommandStart()): ...
```

:::tip 提示
命令详情只能在首次接收到命令型消息时获取，如果在事件处理后续流程中获取，则会获取到不同的值。
:::

### ShellCommandArgs

获取 shell 命令解析后的参数。

:::tip 提示
如果参数解析失败，则为 [`ParserExit`](../../api/exception.md#ParserExit) 异常，并携带错误码与错误信息。

由于 `ArgumentParser` 在解析到 `--help` 参数时也会抛出异常，这种情况下错误码为 `0` 且错误信息即为帮助信息。
:::

```python {8,12}
from nonebot import on_shell_command
from nonebot.params import ShellCommandArgs

matcher = on_shell_command("cmd", parser)

# 解析失败
@matcher.handle()
async def _(foo: ParserExit = ShellCommandArgs()): ...

# 解析成功
@matcher.handle()
async def _(foo: Dict[str, Any] = ShellCommandArgs()): ...
```

### ShellCommandArgv

获取 shell 命令解析前的参数列表。

```python {7}
from nonebot import on_shell_command
from nonebot.params import ShellCommandArgs

matcher = on_shell_command("cmd")

@matcher.handle()
async def _(foo: List[str] = ShellCommandArgv()): ...
```

### RegexMatched

获取正则匹配结果。

```python {7}
from nonebot import on_regex
from nonebot.params import RegexMatched

matcher = on_regex("regex")

@matcher.handle()
async def _(foo: str = RegexMatched()): ...
```

### RegexGroup

获取正则匹配结果的 group 元组。

```python {7}
from nonebot import on_regex
from nonebot.params import RegexGroup

matcher = on_regex("regex")

@matcher.handle()
async def _(foo: Tuple[Any, ...] = RegexGroup()): ...
```

### RegexDict

获取正则匹配结果的 group 字典。

```python {7}
from nonebot import on_regex
from nonebot.params import RegexDict

matcher = on_regex("regex")

@matcher.handle()
async def _(foo: Dict[str, Any] = RegexDict()): ...
```

### Matcher

获取当前事件响应器实例。

```python {7}
from nonebot import on_message
from nonebot.matcher import Matcher

foo = on_message()

@foo.handle()
async def _(matcher: Matcher): ...
```

### Received

获取某次 `receive` 接收的事件。

```python {8}
from nonebot import on_message
from nonebot.adapters import Event
from nonebot.params import Received

matcher = on_message()

@matcher.receive("id")
async def _(foo: Event = Received("id")): ...
```

### LastReceived

获取最近一次 `receive` 接收的事件。

```python {8}
from nonebot import on_message
from nonebot.adapters import Event
from nonebot.params import LastReceived

matcher = on_message()

@matcher.receive("any")
async def _(foo: Event = LastReceived()): ...
```

### Arg

获取某次 `got` 接收的参数。

```python {8-9}
from nonebot.params import Arg
from nonebot import on_message
from nonebot.adapters import Message

matcher = on_message()

@matcher.got("key")
async def _(key: Message = Arg()): ...
async def _(foo: Message = Arg("key")): ...
```

### ArgStr

获取某次 `got` 接收的参数，并转换为字符串。

```python {7-8}
from nonebot import on_message
from nonebot.params import ArgStr

matcher = on_message()

@matcher.got("key")
async def _(key: str = ArgStr()): ...
async def _(foo: str = ArgStr("key")): ...
```

### ArgPlainText

获取某次 `got` 接收的参数的纯文本部分。

```python {7-8}
from nonebot import on_message
from nonebot.params import ArgPlainText

matcher = on_message()

@matcher.got("key")
async def _(key: str = ArgPlainText()): ...
async def _(foo: str = ArgPlainText("key")): ...
```

### Exception

获取事件响应器运行中抛出的异常。

```python {4}
from nonebot.message import run_postprocessor

@run_postprocessor
async def _(e: Exception): ...
```

### Default

带有默认值的参数，便于复用依赖。

```python {1}
async def _(foo="bar"): ...
```
