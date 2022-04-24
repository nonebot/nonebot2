---
sidebar_position: 2
description: 测试事件响应和 API 调用
---

# 定义事件响应和 API 调用

事件响应器可以使用 `Rule` 和 `Permission` 来判断当前事件是否触发事件响应器，使用 `send` 发送消息和使用 `call_api` 调用平台 API，这里我们将对上述行为进行测试。

## 定义预期响应行为

NoneBug 提供了定义 `Rule` 和 `Permission` 的预期行为的方法来进行测试。

接下来将以如下插件进行演示。

<details>
  <summary>示例插件</summary>

```python
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot import on_command

permission = on_command("权限测试", permission=SUPERUSER)
rule = on_command("规则测试", rule=to_me())


@permission.handle()
async def _():
  await permission.finish("权限测试通过")


@rule.handle()
async def _():
  await rule.finish("规则测试通过")

```

</details>

### should_pass_rule 和 should_pass_permission

定义预期通过 `Rule` / `Permission` 限制。

不通过时引发 `AssertionError`。

```python {4}
msg = Message("/权限测试")
# 将此处的 make_fake_event() 替换为对应平台的事件类型
event = make_fake_event(_message=msg, _to_me=True)()
ctx.should_pass_permission()  # 出错：AssertionError
```

```python {4}
msg = Message("/规则测试")
# 将此处的 make_fake_event() 替换为对应平台的事件类型
event = make_fake_event(_message=msg, _to_me=True)()
ctx.should_pass_rule()  # 通过
ctx.should_send_message(event, "规则测试通过", True)
ctx.should_finished()
```

### should_not_pass_rule 和 should_not_pass_permission

与 `should_pass_rule` 和 `should_pass_permission` 相反。

通过时引发 `AssertionError`。

```python {4}
msg = Message("/权限测试")
# 将此处的 make_fake_event() 替换为对应平台的事件类型
event = make_fake_event(_message=msg, _to_me=True)()
ctx.should_not_pass_permission()  # 通过
ctx.should_send_message(event, "权限测试通过", True)
ctx.should_finished()
```

```python {4}
msg = Message("/规则测试")
# 将此处的 make_fake_event() 替换为对应平台的事件类型
event = make_fake_event(_message=msg, _to_me=True)()
ctx.should_not_pass_rule()  # 出错：AssertionError
```

### should_ignore_rule 和 should_ignore_permission

使事件响应器忽略 `Rule` / `Permission` 限制。

```python {4}
msg = Message("/权限测试")
# 将此处的 make_fake_event() 替换为对应平台的事件类型
event = make_fake_event(_message=msg, _to_me=True)()
ctx.should_ignore_permission()
ctx.should_send_message(event, "权限测试通过", True)
ctx.should_finished()
```

```python {4}
msg = Message("/规则测试")
# 将此处的 make_fake_event() 替换为对应平台的事件类型
event = make_fake_event(_message=msg)()
ctx.should_ignore_rule()
ctx.should_send_message(event, "规则测试通过", True)
ctx.should_finished()
```

## 定义预期 API 调用行为

在[事件响应器操作](../../tutorial/plugin/matcher-operation.md)和[调用平台 API](../../tutorial/call-api.md) 中，我们已经了解如何向平台发送消息或调用 `API`
。

接下来让我们定义下面的预期操作对 [`send`](../../tutorial/plugin/matcher-operation.md#send)
和 [`call_api`](../../api/adapters/index.md#Bot-call_api)
进行测试。

### should_call_send

定义事件响应器预期发送消息。

适用操作：`send`。

参数：

`event`：事件对象。

`message`：预期的消息对象，可以是`str`、[`Message`](../../api/adapters/index.md#Message)
和 [`MessageSegment`](../../api/adapters/index.md#MessageSegment)。

`result`：`send` 的返回值。

`**kwargs`：`send` 方法的额外参数。

```python {5}
msg = Message("/天气 上海")
# 将此处的 make_fake_event() 替换为对应平台的事件类型
event = make_fake_event(_message=msg)()
ctx.receive_event(bot, event)
ctx.should_call_send(event=event, message="上海的天气是...", result=True)
ctx.should_finished()
```

### should_call_api

定义事件响应器预期调用机器人 API 接口。

适用操作：`call_api`。

参数：

`api`：API 名称。

`data`：预期的请求数据。

`result`：`call_api` 的返回值。

`**kwargs`：`call_api` 方法的额外参数。

```python {5}
msg = Message("/test")
# 将此处的 make_fake_event() 替换为对应平台的事件类型
event = make_fake_event(_message=msg, _to_me=True)()
ctx.receive_event(bot, event)
ctx.should_call_api("test", {"test": True}, None)
ctx.should_finished()
```

<details>
  <summary>call_api 示例</summary>

```python
from nonebot import Bot, on_command

test = on_command("test")


@test.handle()
async def _(bot: Bot):
  await bot.call_api("test", test=True)
  await test.finish()
```

</details>
