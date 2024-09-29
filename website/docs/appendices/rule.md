---
sidebar_position: 1
description: 自定义响应规则

options:
  menu:
    - category: appendices
      weight: 20
---

# 响应规则

机器人在实际应用中，往往会接收到多种多样的事件类型，NoneBot 通过响应规则来控制事件的处理。

在[指南](../tutorial/matcher.md#为事件响应器添加参数)中，我们为 `weather` 命令添加了一个 `rule=to_me()` 参数，这个参数就是一个响应规则，确保只有在私聊或者 `@bot` 时才会响应。

响应规则是一个 `Rule` 对象，它由一系列的 `RuleChecker` 函数组成，每个 `RuleChecker` 函数都会检查事件是否符合条件，如果所有的检查都通过，则事件会被处理。

## RuleChecker

`RuleChecker` 是一个返回值为 `bool` 类型的依赖函数，即 `RuleChecker` 支持依赖注入。我们可以根据上一节中添加的[配置项](./config.mdx#插件配置)，在 `weather` 插件目录中编写一个响应规则：

```python {7,8} title=weather/__init__.py
from nonebot import get_plugin_config

from .config import Config

plugin_config = get_plugin_config(Config)

async def is_enable() -> bool:
    return plugin_config.weather_plugin_enabled

weather = on_command("天气", rule=is_enable)
```

在上面的代码中，我们定义了一个函数 `is_enable`，它会检查配置项 `weather_plugin_enabled` 是否为 `True`。这个函数 `is_enable` 即为一个 `RuleChecker`。

## Rule

`Rule` 是若干个 `RuleChecker` 的集合，它会并发调用每个 `RuleChecker`，只有当所有 `RuleChecker` 检查通过时匹配成功。例如：我们可以组合两个 `RuleChecker`，一个用于检查插件是否启用，一个用于检查用户是否在黑名单中：

```python {10}
from nonebot.rule import Rule
from nonebot.adapters import Event

async def is_enable() -> bool:
    return plugin_config.weather_plugin_enabled

async def is_blacklisted(event: Event) -> bool:
    return event.get_user_id() not in BLACKLIST

rule = Rule(is_enable, is_blacklisted)

weather = on_command("天气", rule=rule)
```

## 合并响应规则

在定义响应规则时，我们可以将规则进行细分，来更好地复用规则。而在使用时，我们需要合并多个规则。除了使用 `Rule` 对象来组合多个 `RuleChecker` 外，我们还可以对 `Rule` 对象进行合并。在原 `weather` 插件中，我们可以将 `rule=to_me()` 与 `rule=is_enable` 使用 `&` 运算符合并：

```python {13} title=weather/__init__.py
from nonebot.rule import to_me
from nonebot import get_plugin_config

from .config import Config

plugin_config = get_plugin_config(Config)

async def is_enable() -> bool:
    return plugin_config.weather_plugin_enabled

weather = on_command(
    "天气",
    rule=to_me() & is_enable,
    aliases={"weather", "查天气"},
    priority=plugin_config.weather_command_priority,
    block=True,
)
```

这样，`weather` 命令就只会在插件启用且在私聊或者 `@bot` 时才会响应。

合并响应规则可以有多种形式，例如：

```python {4-6}
rule1 = Rule(foo_checker)
rule2 = Rule(bar_checker)

rule = rule1 & rule2
rule = rule1 & bar_checker
rule = foo_checker & rule2
```

同时，我们也无需担心合并了一个 `None` 值，`Rule` 会忽略 `None` 值。

```python
assert (rule & None) is rule
```

## 主动使用响应规则

除了在事件响应器中使用响应规则外，我们也可以主动使用响应规则来判断事件是否符合条件。例如：

```python {3}
rule = Rule(some_checker)

result: bool = await rule(bot, event, state)
```

我们只需要传入 `Bot` 对象、事件和会话状态，`Rule` 会并发调用所有 `RuleChecker` 进行检查，并返回结果。

## 内置响应规则

NoneBot 内置了一些常用的响应规则，可以直接通过事件响应器辅助函数或者自行合并其他规则使用。内置响应规则列表可以参考[事件响应器进阶](../advanced/matcher.md)
