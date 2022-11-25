---
sidebar_position: 2
description: 自定义事件响应器的响应规则

options:
  menu:
    weight: 30
    category: advanced
---

# 自定义匹配规则

机器人在实际应用中，往往会接收到多种多样的事件类型，NoneBot2 提供了可自定义的匹配规则 ── `Rule`。在[定义事件响应器](../tutorial/plugin/create-matcher.md#创建事件响应器)中，已经介绍了多种内置的事件响应器，接下来我们将说明自定义匹配规则的基本用法。

## 创建匹配规则

匹配规则可以是一个 `Rule` 对象，也可以是一个 `RuleChecker` 类型。`Rule` 是多个 `RuleChecker` 的集合，只有当所有 `RuleChecker` 检查通过时匹配成功。`RuleChecker` 是一个返回值为 `Bool` 类型的依赖函数，即，`RuleChecker` 支持依赖注入。

### 创建 `RuleChecker`

```python {1-2}
async def user_checker(event: Event) -> bool:
    return event.get_user_id() == "123123"

matcher = on_message(rule=user_checker)
```

在上面的代码中，我们定义了一个函数 `user_checker`，它检查事件的用户 ID 是否等于 `"123123"`。这个函数 `user_checker` 即为一个 `RuleChecker`。

### 创建 `Rule`

```python {1-2,4-5,7}
async def user_checker(event: Event) -> bool:
    return event.get_user_id() == "123123"

async def message_checker(event: Event) -> bool:
    return event.get_plaintext() == "hello"

rule = Rule(user_checker, message_checker)
matcher = on_message(rule=rule)
```

在上面的代码中，我们定义了两个函数 `user_checker` 和 `message_checker`，它们检查事件的用户 ID 是否等于 `"123123"`，以及消息的内容是否等于 `"hello"`。随后，我们定义了一个 `Rule` 对象，它包含了这两个函数。

## 注册匹配规则

在[定义事件响应器](../tutorial/plugin/create-matcher.md#创建事件响应器)中，我们已经了解了如何事件响应器的组成。现在，我们仅需要将匹配规则注册到事件响应器中。

```python {4}
async def user_checker(event: Event) -> bool:
    return event.get_user_id() == "123123"

matcher = on_message(rule=user_checker)
```

在定义事件响应器的辅助函数中，都有一个 `rule` 参数，用于指定自定义的匹配规则。辅助函数会为你将自定义匹配规则与内置规则组合，并注册到事件响应器中。

## 合并匹配规则

在定义匹配规则时，我们往往希望将规则进行细分，来更好地复用规则。而在使用时，我们需要合并多个规则。除了使用 `Rule` 对象来组合多个 `RuleChecker` 外，我们还可以对 `Rule` 对象进行合并。

```python {4-6}
rule1 = Rule(foo_checker)
rule2 = Rule(bar_checker)

rule = rule1 & rule2
rule = rule1 & bar_checker
rule = foo_checker & rule2
```

同时，你也无需担心合并了一个 `None` 值，`Rule` 会忽略 `None` 值。

```python
assert (rule & None) is rule
```
