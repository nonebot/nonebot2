---
sidebar_position: 3
description: 定义预期处理行为
---

# 定义预期处理行为

除了 `send`，事件响应器还有其他的操作，我们也需要对它们进行测试，下面我们将定义如下事件响应器操作的预期行为对对应的事件响应器操作进行测试。

## should_finished

定义事件响应器预取结束当前事件的整个处理流程。

适用事件响应器操作：[`finish`](../../tutorial/plugin/matcher-operation.md#finish)。

```python {6}
msg = Message("/天气 上海")
# 将此处的 make_fake_event() 替换为对应平台的事件类型
event = make_fake_event(_message=msg)()
ctx.receive_event(bot, event)
ctx.should_call_send(event=event, message="上海的天气是...", result=True)
ctx.should_finished()
```

## should_paused

定义事件响应器预期立即结束当前事件处理依赖并等待接收一个新的事件后进入下一个事件处理依赖。

适用事件响应器操作：[`pause`](../../tutorial/plugin/matcher-operation.md#pause)。

```python {4}
ctx.receive_event(bot, event)
# 如果事件响应器发送了消息
ctx.should_call_send(event=event, message="", result=True)
ctx.should_paused()
...
```

## should_reject

定义事件响应器预期立即结束当前事件处理依赖并等待接收一个新的事件后再次执行当前事件处理依赖。

适用事件响应器操作：[`reject`](../../tutorial/plugin/matcher-operation.md#reject)
、[`reject_arg`](../../tutorial/plugin/matcher-operation.md#reject_arg)
和 [`reject_receive`](../../tutorial/plugin/matcher-operation.md#reject_receive)。

```python {10}
msg = Message("/天气 南京")
# 将此处的 make_fake_event() 替换为对应平台的事件类型
event = make_fake_event(_message=msg, _to_me=True)()
ctx.receive_event(bot, event)
ctx.should_call_send(
    event,
    Message.template("你想查询的城市 {} 暂不支持，请重新输入！").format("南京"),
    True,
)
ctx.should_rejected()
msg = Message("北京")
# 将此处的 make_fake_event() 替换为对应平台的事件类型
event = make_fake_event(_message=msg)()
ctx.receive_event(bot, event)
ctx.should_call_send(event, "北京的天气是...", True)
ctx.should_finished()
```
