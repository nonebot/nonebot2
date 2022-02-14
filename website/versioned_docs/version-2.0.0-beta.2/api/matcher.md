---
sidebar_position: 3
description: nonebot.matcher 模块
---

# nonebot.matcher

本模块实现事件响应器的创建与运行，并提供一些快捷方法来帮助用户更好的与机器人进行对话。

## _class_ `Matcher()` {#Matcher}

- **说明**

  事件响应器类

### _class-var_ `block` {#Matcher-block}

- **类型:** bool

### _class-var_ `expire_time` {#Matcher-expire_time}

- **类型:** datetime.datetime | None

### _instance-var_ `handlers` {#Matcher-handlers}

- **类型:** list[nonebot.dependencies.Dependent[Any]]

### _class-var_ `module` {#Matcher-module}

- **类型:** module | None

### _class-var_ `module_name` {#Matcher-module_name}

- **类型:** str | None

### _class-var_ `permission` {#Matcher-permission}

- **类型:** nonebot.internal.permission.Permission

### _class-var_ `plugin` {#Matcher-plugin}

- **类型:** Plugin | None

### _class-var_ `plugin_name` {#Matcher-plugin_name}

- **类型:** str | None

### _class-var_ `priority` {#Matcher-priority}

- **类型:** int

### _class-var_ `rule` {#Matcher-rule}

- **类型:** nonebot.internal.rule.Rule

### _class-var_ `temp` {#Matcher-temp}

- **类型:** bool

### _class-var_ `type` {#Matcher-type}

- **类型:** str

### _classmethod_ `append_handler(cls, handler, parameterless=None)` {#Matcher-append_handler}

- **参数**

  - `handler` ((\*Any, \*\*Any) -> Any)

  - `parameterless` (list[Any] | None)

- **返回**

  - [Dependent](./dependencies/index.md#Dependent)[typing.Any]

### _async classmethod_ `check_perm(cls, bot, event, stack=None, dependency_cache=None)` {#Matcher-check_perm}

- **说明**

  检查是否满足触发权限

- **参数**

  - `bot` (nonebot.internal.adapter.bot.Bot): Bot 对象

  - `event` (nonebot.internal.adapter.event.Event): 上报事件

  - `stack` (contextlib.AsyncExitStack | None): 异步上下文栈

  - `dependency_cache` (dict[(\*Any, \*\*Any) -> Any, Task[Any]] | None): 依赖缓存

- **返回**

  - bool: 是否满足权限

### _async classmethod_ `check_rule(cls, bot, event, state, stack=None, dependency_cache=None)` {#Matcher-check_rule}

- **说明**

  检查是否满足匹配规则

- **参数**

  - `bot` (nonebot.internal.adapter.bot.Bot): Bot 对象

  - `event` (nonebot.internal.adapter.event.Event): 上报事件

  - `state` (dict[Any, Any]): 当前状态

  - `stack` (contextlib.AsyncExitStack | None): 异步上下文栈

  - `dependency_cache` (dict[(\*Any, \*\*Any) -> Any, Task[Any]] | None): 依赖缓存

- **返回**

  - bool: 是否满足匹配规则

### _async classmethod_ `finish(cls, message=None, **kwargs)` {#Matcher-finish}

- **说明**

  发送一条消息给当前交互用户并结束当前事件响应器

- **参数**

  - `message` (str | nonebot.internal.adapter.message.Message | nonebot.internal.adapter.message.MessageSegment | nonebot.internal.adapter.template.MessageTemplate | NoneType): 消息内容

  - `**kwargs`: [Bot.send](./adapters/index.md#Bot-send) 的参数，请参考对应 adapter 的 bot 对象 api

- **返回**

  - NoReturn

### _method_ `get_arg(self, key, default=None)` {#Matcher-get_arg}

- **说明**

  获取一个 `got` 消息

  如果没有找到对应的消息，返回 `default` 值

- **参数**

  - `key` (str)

  - `default` ((~ T))

- **返回**

  - nonebot.internal.adapter.message.Message | (~ T)

### _method_ `get_last_receive(self, default=None)` {#Matcher-get_last_receive}

- **说明**

  获取最近一次 `receive` 事件

  如果没有事件，返回 `default` 值

- **参数**

  - `default` ((~ T))

- **返回**

  - nonebot.internal.adapter.event.Event | (~ T)

### _method_ `get_receive(self, id, default=None)` {#Matcher-get_receive}

- **说明**

  获取一个 `receive` 事件

  如果没有找到对应的事件，返回 `default` 值

- **参数**

  - `id` (str)

  - `default` ((~ T))

- **返回**

  - nonebot.internal.adapter.event.Event | (~ T)

### _method_ `get_target(self, default=None)` {#Matcher-get_target}

- **参数**

  - `default` ((~ T))

- **返回**

  - str | (~ T)

### _classmethod_ `got(cls, key, prompt=None, parameterless=None)` {#Matcher-got}

- **说明**

  装饰一个函数来指示 NoneBot 获取一个参数 `key`

  当要获取的 `key` 不存在时接收用户新的一条消息再运行该函数，如果 `key` 已存在则直接继续运行

- **参数**

  - `key` (str): 参数名

  - `prompt` (str | nonebot.internal.adapter.message.Message | nonebot.internal.adapter.message.MessageSegment | nonebot.internal.adapter.template.MessageTemplate | NoneType): 在参数不存在时向用户发送的消息

  - `parameterless` (list[Any] | None): 非参数类型依赖列表

- **返回**

  - ((\*Any, \*\*Any) -> Any) -> (\*Any, \*\*Any) -> Any

### _classmethod_ `handle(cls, parameterless=None)` {#Matcher-handle}

- **说明**

  装饰一个函数来向事件响应器直接添加一个处理函数

- **参数**

  - `parameterless` (list[Any] | None): 非参数类型依赖列表

- **返回**

  - ((\*Any, \*\*Any) -> Any) -> (\*Any, \*\*Any) -> Any

### _classmethod_ `new(cls, type_='', rule=None, permission=None, handlers=None, temp=False, priority=1, block=False, *, plugin=None, module=None, expire_time=None, default_state=None, default_type_updater=None, default_permission_updater=None)` {#Matcher-new}

- **说明**

  创建一个新的事件响应器，并存储至 `matchers <#matchers>`\_

- **参数**

  - `type_` (str): 事件响应器类型，与 `event.get_type()` 一致时触发，空字符串表示任意

  - `rule` (nonebot.internal.rule.Rule | None): 匹配规则

  - `permission` (nonebot.internal.permission.Permission | None): 权限

  - `handlers` (list[(\*Any, \*\*Any) -> Any | [Dependent](./dependencies/index.md#Dependent)[Any]] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器，即触发一次后删除

  - `priority` (int): 响应优先级

  - `block` (bool): 是否阻止事件向更低优先级的响应器传播

  - `plugin` (Plugin | None): 事件响应器所在插件

  - `module` (module | None): 事件响应器所在模块

  - `expire_time` (datetime.datetime | None): 事件响应器最终有效时间点，过时即被删除

  - `default_state` (dict[Any, Any] | None): 默认状态 `state`

  - `default_type_updater` ((\*Any, \*\*Any) -> str | Awaitable[str] | [Dependent](./dependencies/index.md#Dependent)[str] | NoneType)

  - `default_permission_updater` ((\*Any, \*\*Any) -> Permission | Awaitable[Permission] | [Dependent](./dependencies/index.md#Dependent)[nonebot.internal.permission.Permission] | NoneType)

- **返回**

  - Type[Matcher]: 新的事件响应器类

### _async classmethod_ `pause(cls, prompt=None, **kwargs)` {#Matcher-pause}

- **说明**

  发送一条消息给当前交互用户并暂停事件响应器，在接收用户新的一条消息后继续下一个处理函数

- **参数**

  - `prompt` (str | nonebot.internal.adapter.message.Message | nonebot.internal.adapter.message.MessageSegment | nonebot.internal.adapter.template.MessageTemplate | NoneType): 消息内容

  - `**kwargs`: [Bot.send](./adapters/index.md#Bot-send) 的参数，请参考对应 adapter 的 bot 对象 api

- **返回**

  - NoReturn

### _classmethod_ `permission_updater(cls, func)` {#Matcher-permission_updater}

- **说明**

  装饰一个函数来更改当前事件响应器的默认会话权限更新函数

- **参数**

  - `func` ((\*Any, \*\*Any) -> Permission | Awaitable[Permission]): 会话权限更新函数

- **返回**

  - (\*Any, \*\*Any) -> Permission | Awaitable[Permission]

### _classmethod_ `receive(cls, id='', parameterless=None)` {#Matcher-receive}

- **说明**

  装饰一个函数来指示 NoneBot 在接收用户新的一条消息后继续运行该函数

- **参数**

  - `id` (str): 消息 ID

  - `parameterless` (list[Any] | None): 非参数类型依赖列表

- **返回**

  - ((\*Any, \*\*Any) -> Any) -> (\*Any, \*\*Any) -> Any

### _async classmethod_ `reject(cls, prompt=None, **kwargs)` {#Matcher-reject}

- **说明**

  最近使用 `got` / `receive` 接收的消息不符合预期，
  发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一个事件后从头开始执行当前处理函数

- **参数**

  - `prompt` (str | nonebot.internal.adapter.message.Message | nonebot.internal.adapter.message.MessageSegment | nonebot.internal.adapter.template.MessageTemplate | NoneType): 消息内容

  - `**kwargs`: [Bot.send](./adapters/index.md#Bot-send) 的参数，请参考对应 adapter 的 bot 对象 api

- **返回**

  - NoReturn

### _async classmethod_ `reject_arg(cls, key, prompt=None, **kwargs)` {#Matcher-reject_arg}

- **说明**

  最近使用 `got` 接收的消息不符合预期，
  发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一条消息后从头开始执行当前处理函数

- **参数**

  - `key` (str): 参数名

  - `prompt` (str | nonebot.internal.adapter.message.Message | nonebot.internal.adapter.message.MessageSegment | nonebot.internal.adapter.template.MessageTemplate | NoneType): 消息内容

  - `**kwargs`: [Bot.send](./adapters/index.md#Bot-send) 的参数，请参考对应 adapter 的 bot 对象 api

- **返回**

  - NoReturn

### _async classmethod_ `reject_receive(cls, id='', prompt=None, **kwargs)` {#Matcher-reject_receive}

- **说明**

  最近使用 `receive` 接收的消息不符合预期，
  发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一个事件后从头开始执行当前处理函数

- **参数**

  - `id` (str): 消息 id

  - `prompt` (str | nonebot.internal.adapter.message.Message | nonebot.internal.adapter.message.MessageSegment | nonebot.internal.adapter.template.MessageTemplate | NoneType): 消息内容

  - `**kwargs`: [Bot.send](./adapters/index.md#Bot-send) 的参数，请参考对应 adapter 的 bot 对象 api

- **返回**

  - NoReturn

### _async method_ `resolve_reject(self)` {#Matcher-resolve_reject}

- **返回**

  - Unknown

### _async method_ `run(self, bot, event, state, stack=None, dependency_cache=None)` {#Matcher-run}

- **参数**

  - `bot` (nonebot.internal.adapter.bot.Bot)

  - `event` (nonebot.internal.adapter.event.Event)

  - `state` (dict[Any, Any])

  - `stack` (contextlib.AsyncExitStack | None)

  - `dependency_cache` (dict[(\*Any, \*\*Any) -> Any, Task[Any]] | None)

- **返回**

  - Unknown

### _async classmethod_ `send(cls, message, **kwargs)` {#Matcher-send}

- **说明**

  发送一条消息给当前交互用户

- **参数**

  - `message` (str | nonebot.internal.adapter.message.Message | nonebot.internal.adapter.message.MessageSegment | nonebot.internal.adapter.template.MessageTemplate): 消息内容

  - `**kwargs` (Any): [Bot.send](./adapters/index.md#Bot-send) 的参数，请参考对应 adapter 的 bot 对象 api

- **返回**

  - Any

### _method_ `set_arg(self, key, message)` {#Matcher-set_arg}

- **说明**

  设置一个 `got` 消息

- **参数**

  - `key` (str)

  - `message` (nonebot.internal.adapter.message.Message)

- **返回**

  - None

### _method_ `set_receive(self, id, event)` {#Matcher-set_receive}

- **说明**

  设置一个 `receive` 事件

- **参数**

  - `id` (str)

  - `event` (nonebot.internal.adapter.event.Event)

- **返回**

  - None

### _method_ `set_target(self, target, cache=True)` {#Matcher-set_target}

- **参数**

  - `target` (str)

  - `cache` (bool)

- **返回**

  - None

### _async method_ `simple_run(self, bot, event, state, stack=None, dependency_cache=None)` {#Matcher-simple_run}

- **参数**

  - `bot` (nonebot.internal.adapter.bot.Bot)

  - `event` (nonebot.internal.adapter.event.Event)

  - `state` (dict[Any, Any])

  - `stack` (contextlib.AsyncExitStack | None)

  - `dependency_cache` (dict[(\*Any, \*\*Any) -> Any, Task[Any]] | None)

- **返回**

  - Unknown

### _classmethod_ `skip(cls)` {#Matcher-skip}

- **说明**

  跳过当前事件处理函数，继续下一个处理函数

  通常在事件处理函数的依赖中使用。

- **返回**

  - NoReturn

### _method_ `stop_propagation(self)` {#Matcher-stop_propagation}

- **说明**

  阻止事件传播

- **返回**

  - Unknown

### _classmethod_ `type_updater(cls, func)` {#Matcher-type_updater}

- **说明**

  装饰一个函数来更改当前事件响应器的默认响应事件类型更新函数

- **参数**

  - `func` ((\*Any, \*\*Any) -> str | Awaitable[str]): 响应事件类型更新函数

- **返回**

  - (\*Any, \*\*Any) -> str | Awaitable[str]

### _async method_ `update_permission(self, bot, event)` {#Matcher-update_permission}

- **参数**

  - `bot` (nonebot.internal.adapter.bot.Bot)

  - `event` (nonebot.internal.adapter.event.Event)

- **返回**

  - nonebot.internal.permission.Permission

### _async method_ `update_type(self, bot, event)` {#Matcher-update_type}

- **参数**

  - `bot` (nonebot.internal.adapter.bot.Bot)

  - `event` (nonebot.internal.adapter.event.Event)

- **返回**

  - str
