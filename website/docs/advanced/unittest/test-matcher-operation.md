---
sidebar_position: 2
description: 测试事件响应器操作

options:
menu:
weight: 51
category: advanced
---

# 测试事件处理流程

在[教程 - 插件 - 定义事件处理流程](../../tutorial/plugin/matcher-operation.md)中，我们已经了解如何通过事件响应器操作来改变事件处理流程。

接下来让我们对这些事件响应器操作进行测试。

## should_call_send

测试事件响应器应当发送的消息。

适用操作：[`send`](../../api/adapters/index.md#Bot-send)

参数：

`event`：事件对象。

`message`：预期的消息对象，可以是`str`、[`Message`](../../api/adapters/index.md#Message)
、[`MessageSegment`](../../api/adapters/index.md#MessageSegment)
或 [`MessageTemplate`](../../api/adapters/index.md#MessageTemplate)。

`result`：[`send`](../../api/adapters/index.md#Bot-send)的返回值。

`**kwargs`：其他参数。

```python {4}
msg = Message("/天气 上海")
event = make_fake_event(_message=msg)()  # 这里的event替换为对应平台的事件类型
ctx.receive_event(bot, event)
ctx.should_call_send(event=event, message="上海的天气是...", result=True)
ctx.should_finished()
```

## should_finished

测试事件响应器是否结束当前事件的整个处理流程。

适用操作：[`finish`](../../api/matcher#Matcher-finish)

```python {5}
msg = Message("/天气 上海")
event = make_fake_event(_message=msg)()  # 这里的event替换为对应平台的事件类型
ctx.receive_event(bot, event)
ctx.should_call_send(event=event, message="上海的天气是...", result=True)
ctx.should_finished()
```

## should_paused

测试事件响应器是否立即结束当前事件处理依赖并等待接收一个新的事件后进入下一个事件处理依赖。

适用操作：[`pause`](../../api/matcher#Matcher-pause)

```python {3}
ctx.receive_event(bot, event)
ctx.should_call_send(event=event, message="", result=True)  # if the handler sended message
ctx.should_paused()
...
```

## should_reject

测试事件响应器是否立即结束当前事件处理依赖并等待接收一个新的事件后再次执行当前事件处理依赖。

适用操作：[`reject`](../../api/matcher#Matcher-reject)、[`reject_arg`](../../api/matcher#Matcher-reject_arg)
和 [`reject_receive`](../../api/matcher#Matcher-reject_receive)

```python {9}
msg = Message("/天气 南京")
event = make_fake_event(_message=msg, _to_me=True)()  # 这里的event替换为对应平台的事件类型
ctx.receive_event(bot, event)
ctx.should_call_send(
    event,
    Message.template("你想查询的城市 {} 暂不支持，请重新输入！").format("南京"),
    True,
)
ctx.should_rejected()
msg = Message("北京")
event = make_fake_event(_message=msg)()  # 这里的event替换为对应平台的事件类型
ctx.receive_event(bot, event)
ctx.should_call_send(event, "北京的天气是...", True)
ctx.should_finished()
```

## should_call_api

测试事件响应器是否调用机器人 API 接口。

参数：

`event`：事件对象。

`data`：预期的 API 数据。

`result`：[`call_api`](../../api/adapters/index.md#Bot-call_api)的返回值。

`**kwargs`：其他参数。

适用操作：[`call_api`](../../api/adapters/index.md#Bot-call_api)

```python {4}
msg = Message("/test")
event = make_fake_event(_message=msg, _to_me=True)()  # 这里的event替换为对应平台的事件类型
ctx.receive_event(bot, event)
ctx.should_call_api("test", {"test": True}, None)
ctx.should_finished()
```

<details>
  <summary>call_api示例</summary>

```python
from nonebot import Bot, on_command

test = on_command("test")


@test.handle()
async def _(bot: Bot):
  await bot.call_api("test", test=True)
  await test.finish()

```

</details>
