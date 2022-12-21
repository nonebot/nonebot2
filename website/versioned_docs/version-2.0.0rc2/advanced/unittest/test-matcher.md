---
sidebar_position: 2
description: 测试事件响应和 API 调用
---

# 测试事件响应和 API 调用

事件响应器通过 `Rule` 和 `Permission` 来判断当前事件是否触发事件响应器，通过 `send` 发送消息或使用 `call_api` 调用平台 API，这里我们将对上述行为进行测试。

## 定义预期响应行为

NoneBug 提供了六种定义 `Rule` 和 `Permission` 的预期行为的方法来进行测试：

- `should_pass_rule`
- `should_not_pass_rule`
- `should_ignore_rule`
- `should_pass_permission`
- `should_not_pass_permission`
- `should_ignore_permission`

以下为示例代码

<!-- markdownlint-disable MD033 -->
<details>
  <summary>示例插件</summary>

```python title=example.py
from nonebot import on_message

async def always_pass():
    return True

async def never_pass():
    return False

foo = on_message(always_pass)
bar = on_message(never_pass, permission=never_pass)
```

</details>

```python {12,13,19,20,27,28}
import pytest
from nonebug import App

@pytest.mark.asyncio
async def test_matcher(app: App, load_plugins):
    from awesome_bot.plugins.example import foo, bar

    async with app.test_matcher(foo) as ctx:
        bot = ctx.create_bot()
        event = make_fake_event()()  # 此处替换为平台事件
        ctx.receive_event(bot, event)
        ctx.should_pass_rule()
        ctx.should_pass_permission()

    async with app.test_matcher(bar) as ctx:
        bot = ctx.create_bot()
        event = make_fake_event()()  # 此处替换为平台事件
        ctx.receive_event(bot, event)
        ctx.should_not_pass_rule()
        ctx.should_not_pass_permission()

    # 如需忽略规则/权限不通过
    async with app.test_matcher(bar) as ctx:
        bot = ctx.create_bot()
        event = make_fake_event()()  # 此处替换为平台事件
        ctx.receive_event(bot, event)
        ctx.should_ignore_rule()
        ctx.should_ignore_permission()
```

## 定义预期 API 调用行为

在[事件响应器操作](../../tutorial/plugin/matcher-operation.md)和[调用平台 API](../../tutorial/call-api.md) 中，我们已经了解如何向发送消息或调用平台 `API`。接下来对 [`send`](../../tutorial/plugin/matcher-operation.md#send) 和 [`call_api`](../../api/adapters/index.md#Bot-call_api) 进行测试。

### should_call_send

定义事件响应器预期发送消息，包括使用 [`send`](../../tutorial/plugin/matcher-operation.md#send)、[`finish`](../../tutorial/plugin/matcher-operation.md#finish)、[`pause`](../../tutorial/plugin/matcher-operation.md#pause)、[`reject`](../../tutorial/plugin/matcher-operation.md#reject) 以及 [`got`](../../tutorial/plugin/create-handler.md#使用-got-装饰器) 的 prompt 等方法发送的消息。

`should_call_send` 需要提供四个参数：

- `event`：事件对象。
- `message`：预期的消息对象，可以是`str`、[`Message`](../../api/adapters/index.md#Message) 或 [`MessageSegment`](../../api/adapters/index.md#MessageSegment)。
- `result`：`send` 的返回值，将会返回给插件。
- `**kwargs`：`send` 方法的额外参数。

<details>
  <summary>示例插件</summary>

```python title=example.py
from nonebot import on_message

foo = on_message()

@foo.handle()
async def _():
    await foo.send("test")
```

</details>

```python {12}
import pytest
from nonebug import App

@pytest.mark.asyncio
async def test_matcher(app: App, load_plugins):
    from awesome_bot.plugins.example import foo

    async with app.test_matcher(foo) as ctx:
        bot = ctx.create_bot()
        event = make_fake_event()()  # 此处替换为平台事件
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "test", True)
```

### should_call_api

定义事件响应器预期调用机器人 API 接口，包括使用 `call_api` 或者直接使用 `bot.some_api` 的方式调用 API。

`should_call_api` 需要提供四个参数：

- `api`：API 名称。
- `data`：预期的请求数据。
- `result`：`call_api` 的返回值，将会返回给插件。
- `**kwargs`：`call_api` 方法的额外参数。

<details>
  <summary>示例插件</summary>

```python
from nonebot import on_message
from nonebot.adapters import Bot

foo = on_message()


@foo.handle()
async def _(bot: Bot):
  await bot.example_api(test="test")
```

</details>

```python {12}
import pytest
from nonebug import App

@pytest.mark.asyncio
async def test_matcher(app: App, load_plugins):
    from awesome_bot.plugins.example import foo

    async with app.test_matcher(foo) as ctx:
        bot = ctx.create_bot()
        event = make_fake_event()()  # 此处替换为平台事件
        ctx.receive_event(bot, event)
        ctx.should_call_api("example_api", {"test": "test"}, True)
```
