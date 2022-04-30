---
sidebar_position: 3
description: 测试事件响应处理
---

# 测试事件响应处理行为

除了 `send`，事件响应器还有其他的操作，我们也需要对它们进行测试，下面我们将定义如下事件响应器操作的预期行为对对应的事件响应器操作进行测试。

## should_finished

定义事件响应器预取结束当前事件的整个处理流程。

适用事件响应器操作：[`finish`](../../tutorial/plugin/matcher-operation.md#finish)。

<!-- markdownlint-disable MD033 -->
<details>
  <summary>示例插件</summary>

```python title=example.py
from nonebot import on_message

foo = on_message()

@foo.handle()
async def _():
    await foo.finish("test")
```

</details>

```python {13}
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
        ctx.should_finished()
```

## should_paused

定义事件响应器预期立即结束当前事件处理依赖并等待接收一个新的事件后进入下一个事件处理依赖。

适用事件响应器操作：[`pause`](../../tutorial/plugin/matcher-operation.md#pause)。

<details>
  <summary>示例插件</summary>

```python title=example.py
from nonebot import on_message

foo = on_message()

@foo.handle()
async def _():
    await foo.pause("test")
```

</details>

```python {13}
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
        ctx.should_paused()
```

## should_rejected

定义事件响应器预期立即结束当前事件处理依赖并等待接收一个新的事件后再次执行当前事件处理依赖。

适用事件响应器操作：[`reject`](../../tutorial/plugin/matcher-operation.md#reject)
、[`reject_arg`](../../tutorial/plugin/matcher-operation.md#reject_arg)
和 [`reject_receive`](../../tutorial/plugin/matcher-operation.md#reject_receive)。

<details>
  <summary>示例插件</summary>

```python title=example.py
from nonebot import on_message

foo = on_message()

@foo.got("key")
async def _():
    await foo.reject("test")
```

</details>

```python {13}
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
        ctx.should_rejected()
```
