---
sidebar_position: 3
description: nonebot.matcher 模块
---

# nonebot.matcher

本模块实现事件响应器的创建与运行，并提供一些快捷方法来帮助用户更好的与机器人进行对话。

## _class_ `Matcher()` {#Matcher}

- **说明:** 事件响应器类

- **参数**

  empty

### _instance-var_ `handlers` {#Matcher-handlers}

- **类型:** list[[Dependent](dependencies/index.md#Dependent)[Any]]

- **说明:** 事件响应器拥有的事件处理函数列表

### _class-var_ `type` {#Matcher-type}

- **类型:** ClassVar[str]

- **说明:** 事件响应器类型

### _class-var_ `rule` {#Matcher-rule}

- **类型:** ClassVar[[Rule](rule.md#Rule)]

- **说明:** 事件响应器匹配规则

### _class-var_ `permission` {#Matcher-permission}

- **类型:** ClassVar[[Permission](permission.md#Permission)]

- **说明:** 事件响应器触发权限

### _class-var_ `priority` {#Matcher-priority}

- **类型:** ClassVar[int]

- **说明:** 事件响应器优先级

### _class-var_ `block` {#Matcher-block}

- **类型:** bool

- **说明:** 事件响应器是否阻止事件传播

### _class-var_ `temp` {#Matcher-temp}

- **类型:** ClassVar[bool]

- **说明:** 事件响应器是否为临时

### _class-var_ `expire_time` {#Matcher-expire-time}

- **类型:** ClassVar[datetime | None]

- **说明:** 事件响应器过期时间点

### _classmethod_ `new(type_="", rule=None, permission=None, handlers=None, temp=False, priority=1, block=False, *, plugin=None, module=None, source=None, expire_time=None, default_state=None, default_type_updater=None, default_permission_updater=None)` {#Matcher-new}

- **说明:** 创建一个新的事件响应器，并存储至 `matchers <#matchers>`\_

- **参数**

  - `type_` (str): 事件响应器类型，与 `event.get_type()` 一致时触发，空字符串表示任意

  - `rule` ([Rule](rule.md#Rule) | None): 匹配规则

  - `permission` ([Permission](permission.md#Permission) | None): 权限

  - `handlers` (list[[T\_Handler](typing.md#T-Handler) | [Dependent](dependencies/index.md#Dependent)[Any]] | None): 事件处理函数列表

  - `temp` (bool): 是否为临时事件响应器，即触发一次后删除

  - `priority` (int): 响应优先级

  - `block` (bool): 是否阻止事件向更低优先级的响应器传播

  - `plugin` ([Plugin](plugin/model.md#Plugin) | None): **Deprecated.** 事件响应器所在插件

  - `module` (ModuleType | None): **Deprecated.** 事件响应器所在模块

  - `source` (MatcherSource | None): 事件响应器源代码上下文信息

  - `expire_time` (datetime | timedelta | None): 事件响应器最终有效时间点，过时即被删除

  - `default_state` ([T_State](typing.md#T-State) | None): 默认状态 `state`

  - `default_type_updater` ([T_TypeUpdater](typing.md#T-TypeUpdater) | [Dependent](dependencies/index.md#Dependent)[str] | None): 默认事件类型更新函数

  - `default_permission_updater` ([T_PermissionUpdater](typing.md#T-PermissionUpdater) | [Dependent](dependencies/index.md#Dependent)[[Permission](permission.md#Permission)] | None): 默认会话权限更新函数

- **返回**

  - type[Matcher]: 新的事件响应器类

### _classmethod_ `destroy()` {#Matcher-destroy}

- **说明:** 销毁当前的事件响应器

- **参数**

  empty

- **返回**

  - None

### _classmethod_ `check_perm(bot, event, stack=None, dependency_cache=None)` {#Matcher-check-perm}

- **说明:** 检查是否满足触发权限

- **参数**

  - `bot` ([Bot](adapters/index.md#Bot)): Bot 对象

  - `event` ([Event](adapters/index.md#Event)): 上报事件

  - `stack` (AsyncExitStack | None): 异步上下文栈

  - `dependency_cache` ([T_DependencyCache](typing.md#T-DependencyCache) | None): 依赖缓存

- **返回**

  - bool: 是否满足权限

### _classmethod_ `check_rule(bot, event, state, stack=None, dependency_cache=None)` {#Matcher-check-rule}

- **说明:** 检查是否满足匹配规则

- **参数**

  - `bot` ([Bot](adapters/index.md#Bot)): Bot 对象

  - `event` ([Event](adapters/index.md#Event)): 上报事件

  - `state` ([T_State](typing.md#T-State)): 当前状态

  - `stack` (AsyncExitStack | None): 异步上下文栈

  - `dependency_cache` ([T_DependencyCache](typing.md#T-DependencyCache) | None): 依赖缓存

- **返回**

  - bool: 是否满足匹配规则

### _classmethod_ `type_updater(func)` {#Matcher-type-updater}

- **说明:** 装饰一个函数来更改当前事件响应器的默认响应事件类型更新函数

- **参数**

  - `func` ([T_TypeUpdater](typing.md#T-TypeUpdater)): 响应事件类型更新函数

- **返回**

  - [T_TypeUpdater](typing.md#T-TypeUpdater)

### _classmethod_ `permission_updater(func)` {#Matcher-permission-updater}

- **说明:** 装饰一个函数来更改当前事件响应器的默认会话权限更新函数

- **参数**

  - `func` ([T_PermissionUpdater](typing.md#T-PermissionUpdater)): 会话权限更新函数

- **返回**

  - [T_PermissionUpdater](typing.md#T-PermissionUpdater)

### _classmethod_ `append_handler(handler, parameterless=None)` {#Matcher-append-handler}

- **参数**

  - `handler` ([T_Handler](typing.md#T-Handler))

  - `parameterless` (Iterable[Any] | None)

- **返回**

  - [Dependent](dependencies/index.md#Dependent)[Any]

### _classmethod_ `handle(parameterless=None)` {#Matcher-handle}

- **说明:** 装饰一个函数来向事件响应器直接添加一个处理函数

- **参数**

  - `parameterless` (Iterable[Any] | None): 非参数类型依赖列表

- **返回**

  - ([T_Handler](typing.md#T-Handler)) -> [T_Handler](typing.md#T-Handler)

### _classmethod_ `receive(id="", parameterless=None)` {#Matcher-receive}

- **说明:** 装饰一个函数来指示 NoneBot 在接收用户新的一条消息后继续运行该函数

- **参数**

  - `id` (str): 消息 ID

  - `parameterless` (Iterable[Any] | None): 非参数类型依赖列表

- **返回**

  - ([T_Handler](typing.md#T-Handler)) -> [T_Handler](typing.md#T-Handler)

### _classmethod_ `got(key, prompt=None, parameterless=None)` {#Matcher-got}

- **说明**

  装饰一个函数来指示 NoneBot 获取一个参数 `key`

  当要获取的 `key` 不存在时接收用户新的一条消息再运行该函数，
  如果 `key` 已存在则直接继续运行

- **参数**

  - `key` (str): 参数名

  - `prompt` (str | [Message](adapters/index.md#Message) | [MessageSegment](adapters/index.md#MessageSegment) | [MessageTemplate](adapters/index.md#MessageTemplate) | None): 在参数不存在时向用户发送的消息

  - `parameterless` (Iterable[Any] | None): 非参数类型依赖列表

- **返回**

  - ([T_Handler](typing.md#T-Handler)) -> [T_Handler](typing.md#T-Handler)

### _classmethod_ `send(message, **kwargs)` {#Matcher-send}

- **说明:** 发送一条消息给当前交互用户

- **参数**

  - `message` (str | [Message](adapters/index.md#Message) | [MessageSegment](adapters/index.md#MessageSegment) | [MessageTemplate](adapters/index.md#MessageTemplate)): 消息内容

  - `**kwargs` (Any): [Bot.send](adapters/index.md#Bot-send) 的参数， 请参考对应 adapter 的 bot 对象 api

- **返回**

  - Any

### _classmethod_ `finish(message=None, **kwargs)` {#Matcher-finish}

- **说明:** 发送一条消息给当前交互用户并结束当前事件响应器

- **参数**

  - `message` (str | [Message](adapters/index.md#Message) | [MessageSegment](adapters/index.md#MessageSegment) | [MessageTemplate](adapters/index.md#MessageTemplate) | None): 消息内容

  - `**kwargs`: [Bot.send](adapters/index.md#Bot-send) 的参数， 请参考对应 adapter 的 bot 对象 api

- **返回**

  - NoReturn

### _classmethod_ `pause(prompt=None, **kwargs)` {#Matcher-pause}

- **说明:** 发送一条消息给当前交互用户并暂停事件响应器，在接收用户新的一条消息后继续下一个处理函数

- **参数**

  - `prompt` (str | [Message](adapters/index.md#Message) | [MessageSegment](adapters/index.md#MessageSegment) | [MessageTemplate](adapters/index.md#MessageTemplate) | None): 消息内容

  - `**kwargs`: [Bot.send](adapters/index.md#Bot-send) 的参数， 请参考对应 adapter 的 bot 对象 api

- **返回**

  - NoReturn

### _classmethod_ `reject(prompt=None, **kwargs)` {#Matcher-reject}

- **说明:** 最近使用 `got` / `receive` 接收的消息不符合预期， 发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一个事件后从头开始执行当前处理函数

- **参数**

  - `prompt` (str | [Message](adapters/index.md#Message) | [MessageSegment](adapters/index.md#MessageSegment) | [MessageTemplate](adapters/index.md#MessageTemplate) | None): 消息内容

  - `**kwargs`: [Bot.send](adapters/index.md#Bot-send) 的参数， 请参考对应 adapter 的 bot 对象 api

- **返回**

  - NoReturn

### _classmethod_ `reject_arg(key, prompt=None, **kwargs)` {#Matcher-reject-arg}

- **说明:** 最近使用 `got` 接收的消息不符合预期， 发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一条消息后从头开始执行当前处理函数

- **参数**

  - `key` (str): 参数名

  - `prompt` (str | [Message](adapters/index.md#Message) | [MessageSegment](adapters/index.md#MessageSegment) | [MessageTemplate](adapters/index.md#MessageTemplate) | None): 消息内容

  - `**kwargs`: [Bot.send](adapters/index.md#Bot-send) 的参数， 请参考对应 adapter 的 bot 对象 api

- **返回**

  - NoReturn

### _classmethod_ `reject_receive(id="", prompt=None, **kwargs)` {#Matcher-reject-receive}

- **说明:** 最近使用 `receive` 接收的消息不符合预期， 发送一条消息给当前交互用户并将当前事件处理流程中断在当前位置，在接收用户新的一个事件后从头开始执行当前处理函数

- **参数**

  - `id` (str): 消息 id

  - `prompt` (str | [Message](adapters/index.md#Message) | [MessageSegment](adapters/index.md#MessageSegment) | [MessageTemplate](adapters/index.md#MessageTemplate) | None): 消息内容

  - `**kwargs`: [Bot.send](adapters/index.md#Bot-send) 的参数， 请参考对应 adapter 的 bot 对象 api

- **返回**

  - NoReturn

### _classmethod_ `skip()` {#Matcher-skip}

- **说明**

  跳过当前事件处理函数，继续下一个处理函数

  通常在事件处理函数的依赖中使用。

- **参数**

  empty

- **返回**

  - NoReturn

### _method_ `get_receive(id, default=None)` {#Matcher-get-receive}

- **说明**

  获取一个 `receive` 事件

  如果没有找到对应的事件，返回 `default` 值

- **重载**

  **1.** `(id) -> Event | None`

  - **参数**

    - `id` (str)

  - **返回**

    - [Event](adapters/index.md#Event) | None

  **2.** `(id, default) -> Event | T`

  - **参数**

    - `id` (str)

    - `default` (T)

  - **返回**

    - [Event](adapters/index.md#Event) | T

### _method_ `set_receive(id, event)` {#Matcher-set-receive}

- **说明:** 设置一个 `receive` 事件

- **参数**

  - `id` (str)

  - `event` ([Event](adapters/index.md#Event))

- **返回**

  - None

### _method_ `get_last_receive(default=None)` {#Matcher-get-last-receive}

- **说明**

  获取最近一次 `receive` 事件

  如果没有事件，返回 `default` 值

- **重载**

  **1.** `() -> Event | None`

  - **参数**

    empty

  - **返回**

    - [Event](adapters/index.md#Event) | None

  **2.** `(default) -> Event | T`

  - **参数**

    - `default` (T)

  - **返回**

    - [Event](adapters/index.md#Event) | T

### _method_ `get_arg(key, default=None)` {#Matcher-get-arg}

- **说明**

  获取一个 `got` 消息

  如果没有找到对应的消息，返回 `default` 值

- **重载**

  **1.** `(key) -> Message | None`

  - **参数**

    - `key` (str)

  - **返回**

    - [Message](adapters/index.md#Message) | None

  **2.** `(key, default) -> Message | T`

  - **参数**

    - `key` (str)

    - `default` (T)

  - **返回**

    - [Message](adapters/index.md#Message) | T

### _method_ `set_arg(key, message)` {#Matcher-set-arg}

- **说明:** 设置一个 `got` 消息

- **参数**

  - `key` (str)

  - `message` ([Message](adapters/index.md#Message))

- **返回**

  - None

### _method_ `set_target(target, cache=True)` {#Matcher-set-target}

- **参数**

  - `target` (str)

  - `cache` (bool)

- **返回**

  - None

### _method_ `get_target(default=None)` {#Matcher-get-target}

- **重载**

  **1.** `() -> str | None`

  - **参数**

    empty

  - **返回**

    - str | None

  **2.** `(default) -> str | T`

  - **参数**

    - `default` (T)

  - **返回**

    - str | T

### _method_ `stop_propagation()` {#Matcher-stop-propagation}

- **说明:** 阻止事件传播

- **参数**

  empty

- **返回**

  - untyped

### _async method_ `update_type(bot, event, stack=None, dependency_cache=None)` {#Matcher-update-type}

- **参数**

  - `bot` ([Bot](adapters/index.md#Bot))

  - `event` ([Event](adapters/index.md#Event))

  - `stack` (AsyncExitStack | None)

  - `dependency_cache` ([T_DependencyCache](typing.md#T-DependencyCache) | None)

- **返回**

  - str

### _async method_ `update_permission(bot, event, stack=None, dependency_cache=None)` {#Matcher-update-permission}

- **参数**

  - `bot` ([Bot](adapters/index.md#Bot))

  - `event` ([Event](adapters/index.md#Event))

  - `stack` (AsyncExitStack | None)

  - `dependency_cache` ([T_DependencyCache](typing.md#T-DependencyCache) | None)

- **返回**

  - [Permission](permission.md#Permission)

### _async method_ `resolve_reject()` {#Matcher-resolve-reject}

- **参数**

  empty

- **返回**

  - untyped

### _method_ `ensure_context(bot, event)` {#Matcher-ensure-context}

- **参数**

  - `bot` ([Bot](adapters/index.md#Bot))

  - `event` ([Event](adapters/index.md#Event))

- **返回**

  - untyped

### _async method_ `simple_run(bot, event, state, stack=None, dependency_cache=None)` {#Matcher-simple-run}

- **参数**

  - `bot` ([Bot](adapters/index.md#Bot))

  - `event` ([Event](adapters/index.md#Event))

  - `state` ([T_State](typing.md#T-State))

  - `stack` (AsyncExitStack | None)

  - `dependency_cache` ([T_DependencyCache](typing.md#T-DependencyCache) | None)

- **返回**

  - untyped

### _async method_ `run(bot, event, state, stack=None, dependency_cache=None)` {#Matcher-run}

- **参数**

  - `bot` ([Bot](adapters/index.md#Bot))

  - `event` ([Event](adapters/index.md#Event))

  - `state` ([T_State](typing.md#T-State))

  - `stack` (AsyncExitStack | None)

  - `dependency_cache` ([T_DependencyCache](typing.md#T-DependencyCache) | None)

- **返回**

  - untyped

## _var_ `matchers` {#matchers}

- **类型:** untyped

## _class_ `MatcherManager()` {#MatcherManager}

- **说明**

  事件响应器管理器

  实现了常用字典操作，用于管理事件响应器。

- **参数**

  empty

### _method_ `keys()` {#MatcherManager-keys}

- **参数**

  empty

- **返回**

  - KeysView[int]

### _method_ `values()` {#MatcherManager-values}

- **参数**

  empty

- **返回**

  - ValuesView[list[type[[Matcher](#Matcher)]]]

### _method_ `items()` {#MatcherManager-items}

- **参数**

  empty

- **返回**

  - ItemsView[int, list[type[[Matcher](#Matcher)]]]

### _method_ `get(key, default=None)` {#MatcherManager-get}

- **重载**

  **1.** `(key) -> list[type[Matcher]] | None`

  - **参数**

    - `key` (int)

  - **返回**

    - list[type[[Matcher](#Matcher)]] | None

  **2.** `(key, default) -> list[type[Matcher]] | T`

  - **参数**

    - `key` (int)

    - `default` (T)

  - **返回**

    - list[type[[Matcher](#Matcher)]] | T

### _method_ `pop(key)` {#MatcherManager-pop}

- **参数**

  - `key` (int)

- **返回**

  - list[type[[Matcher](#Matcher)]]

### _method_ `popitem()` {#MatcherManager-popitem}

- **参数**

  empty

- **返回**

  - tuple[int, list[type[[Matcher](#Matcher)]]]

### _method_ `clear()` {#MatcherManager-clear}

- **参数**

  empty

- **返回**

  - None

### _method_ `update(__m)` {#MatcherManager-update}

- **参数**

  - `__m` (MutableMapping[int, list[type[[Matcher](#Matcher)]]])

- **返回**

  - None

### _method_ `setdefault(key, default)` {#MatcherManager-setdefault}

- **参数**

  - `key` (int)

  - `default` (list[type[[Matcher](#Matcher)]])

- **返回**

  - list[type[[Matcher](#Matcher)]]

### _method_ `set_provider(provider_class)` {#MatcherManager-set-provider}

- **说明:** 设置事件响应器存储器

- **参数**

  - `provider_class` (type[[MatcherProvider](#MatcherProvider)]): 事件响应器存储器类

- **返回**

  - None

## _abstract class_ `MatcherProvider(matchers)` {#MatcherProvider}

- **说明:** 事件响应器存储器基类

- **参数**

  - `matchers` (Mapping[int, list[type[[Matcher](#Matcher)]]]): 当前存储器中已有的事件响应器

## _var_ `DEFAULT_PROVIDER_CLASS` {#DEFAULT-PROVIDER-CLASS}

- **类型:** untyped

- **说明:** 默认存储器类型
