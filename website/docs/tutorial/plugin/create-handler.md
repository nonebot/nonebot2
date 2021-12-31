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

## 事件处理流程

## 获取上下文信息

### Bot

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

```python {6-8}
from typing import Union

from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent

async def _(foo: Event): ...
async def _(foo: Union[PrivateMessageEvent, GroupMessageEvent]): ...
async def _(event): ...  # 兼容性处理
```

### EventType

```python {3}
from nonebot.params import EventType

async def _(foo: str = EventType()): ...
```

### EventMessage

```python {4}
from nonebot.adapters import Message
from nonebot.params import EventMessage

async def _(foo: str = EventMessage()): ...
```

### EventPlainText

```python {3}
from nonebot.params import EventPlainText

async def _(foo: str = EventPlainText()): ...
```

### EventToMe

```python {3}
from nonebot.params import EventToMe

async def _(foo: bool = EventToMe()): ...
```

### State

```python {4}
from nonebot.params import State
from nonebot.typing import T_State

async def _(foo: T_State = State()): ...
```

### Command

```python {7}
from nonebot import on_command
from nonebot.params import Command

matcher = on_command("cmd")

@matcher.handle()
async def _(foo: Tuple[str, ...] = Command()): ...
```

### CommandArg

```python {8}
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg

matcher = on_command("cmd")

@matcher.handle()
async def _(foo: Message = CommandArg()): ...
```

### ShellCommandArgs

```python {7}
from nonebot import on_command
from nonebot.params import ShellCommandArgs

matcher = on_shell_command("cmd", parser)

@matcher.handle()
async def _(foo: Dict[str, Any] = ShellCommandArgs()): ...
```

### ShellCommandArgv

```python {7}
from nonebot import on_command
from nonebot.params import ShellCommandArgs

matcher = on_shell_command("cmd")

@matcher.handle()
async def _(foo: List[str] = ShellCommandArgv()): ...
```

### RegexMatched

```python {7}
from nonebot import on_regex
from nonebot.params import RegexMatched

matcher = on_regex("regex")

@matcher.handle()
async def _(foo: str = RegexMatched()): ...
```

### RegexGroup

```python {7}
from nonebot import on_regex
from nonebot.params import RegexGroup

matcher = on_regex("regex")

@matcher.handle()
async def _(foo: Tuple[Any, ...] = RegexGroup()): ...
```

### RegexDict

```python {7}
from nonebot import on_regex
from nonebot.params import RegexDict

matcher = on_regex("regex")

@matcher.handle()
async def _(foo: Dict[str, Any] = RegexDict()): ...
```

### Matcher

```python {7}
from nonebot import on_message
from nonebot.matcher import Matcher

foo = on_message()

@foo.handle()
async def _(matcher: Matcher): ...
```

### Received

```python {8}
from nonebot import on_message
from nonebot.adapters import Event
from nonebot.params import Received

matcher = on_message()

@matcher.receive("id")
async def _(foo: Event = Received("id")): ...
```

### LastReceived

```python {8}
from nonebot import on_message
from nonebot.adapters import Event
from nonebot.params import LastReceived

matcher = on_message()

@matcher.receive("any")
async def _(foo: Event = LastReceived()): ...
```

### Arg

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

```python {7-8}
from nonebot import on_message
from nonebot.params import ArgStr

matcher = on_message()

@matcher.got("key")
async def _(key: str = ArgStr()): ...
async def _(foo: str = ArgStr("key")): ...
```

### ArgPlainText

```python {7-8}
from nonebot import on_message
from nonebot.params import ArgPlainText

matcher = on_message()

@matcher.got("key")
async def _(key: str = ArgPlainText()): ...
async def _(foo: str = ArgPlainText("key")): ...
```

### Exception

```python {4}
from nonebot.message import run_postprocessor

@run_postprocessor
async def _(e: Exception): ...
```

### Default

```python {1}
async def _(foo="bar"): ...
```
