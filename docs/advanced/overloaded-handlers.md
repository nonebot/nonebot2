# 事件处理函数重载

当我们在编写 `nonebot2` 应用时， 常常会遇到这样一个问题：该怎么让同一类型的不同事件执行不同的响应逻辑？又或者如何让不同的 `adapter` 针对同一类型的事件作出不同响应？

聪明的你可能很快就想到了，编写相对应的 `Rule` 来应用到不同的 `Matcher` 上面不就可以了！

诚然，此种方法是十分有效的，但是它在编写的过程中会有一些繁琐：需要编写多种不同的 `Rule` ，同时也需要注册不同的 `Matcher` 来适配不同的 `Rule` 。

针对这个情况， `nonebot2` 提供一个便捷而高效的解决方案：`事件处理函数重载` 机制。 简单地说，`handler` ( `事件处理函数` ) 会根据其参数的 `typing hint` (` 类型标注 `) 来对相对应的 `adapter`  和相对应的 `Event` 进行响应，并且忽略不符合其参数 `类型标注` 的情况。

必须要注意的是， 该机制的原理是利用了 `inspect` 获取到了函数的 `singnature` ( `签名` )， 并在其中提取了参数的名称和对应的 `类型标注` 。故而，我们在编写 `handler` 时，参数的名称和 `类型标注`  必须要符合 `T_handler` 之规定，详情可以参看 **指南** 中的[事件处理](../guide/creating-a-handler)。

::: tip

如果想了解更多关于 `inspect` 标准库的信息，可以查看[官方文档](https://docs.python.org/zh-cn/3.9/library/inspect.html)。

:::

下面，我们会以 `CQHTTP` 中的 `消息事件` 中的 `群聊消息事件` 和 `私聊消息事件` 为例，对该机制的应用进行简单的介绍。

## 一个例子

首先，我们需要导入需要的方法，类型。

```python
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent, PrivateMessageEvent
from nonebot.plugin import on_command
```

之后，我们可以注册一个 `Matcher` 来响应 `消息事件` 。

```python
testmatcher = on_command('testoverload')
```

最后,  我们编写不同的`handler ` 并编写不同的 `类型标注` 来实现事件处理函数重载：

```python
@matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await matcher.send('群聊消息事件响应成功！')


@matcher.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    await matcher.send('私聊消息事件响应成功！')
```

此时，我们可以在群聊或者私聊中对我们的机器人发送 `testoverload` ，它会在不同的场景做出不同的应答。

这样一个简单的事件处理函数重载就完成了。