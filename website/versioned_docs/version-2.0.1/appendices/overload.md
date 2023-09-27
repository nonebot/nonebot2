---
sidebar_position: 7
description: 根据事件类型进行不同的处理

options:
  menu:
    - category: appendices
      weight: 80
---

# 事件类型与重载

在之前的示例中，我们已经了解了如何[获取事件信息](../tutorial/event-data.mdx)以及[使用平台接口](./api-calling.mdx)。但是，事件信息通常不仅仅包含消息这一个内容，还有其他平台提供的信息，例如消息发送时间、消息发送者等等。同时，在使用平台接口时，我们需要确保使用的**平台接口**与所要发送的**平台类型**一致，对不同类型的事件需要做出不同的处理。在本章节中，我们将介绍如何获取事件更多的信息以及根据事件类型进行不同的处理。

## 事件类型

在 NoneBot 中，事件均是 `nonebot.adapters.Event` 基类的子类型，基类对一些必要的属性进行了抽象，子类型则根据不同的平台进行了实现。在[自定义权限](./permission.mdx#自定义权限)一节中，我们就使用了 `Event` 的抽象方法 `get_user_id` 来获取事件发送者 ID，这个方法由协议适配器进行了实现，返回机器人用户对应的平台 ID。更多的基类抽象方法可以在[使用适配器](../advanced/adapter.md#获取事件通用信息)中查看。

既然事件是基类的子类型，我们实际可以获得的信息通常多于基类抽象方法所提供的。如果我们不满足于基类能获得的信息，我们可以小小的修改一下事件处理函数的事件参数类型注解，使其变为子类型，这样我们就可以通过协议适配器定义的子类型来获取更多的信息。我们以 `Console` 协议适配器为例：

```python {4} title=weather/__init__.py
from nonebot.adapters.console import MessageEvent

@weather.got("location", prompt="请输入地名")
async def got_location(event: MessageEvent, location: str = ArgPlainText()):
    await weather.finish(f"{event.time.strftime('%Y-%m-%d')} {location} 的天气是...")
```

在上面的代码中，我们获取了 `Console` 协议适配器的消息事件提供的发送时间 `time` 属性。

:::caution 注意
如果**基类**就能满足你的需求，那么就**不要修改**事件参数类型注解，这样可以使你的代码更加**通用**，可以在更多平台上运行。如何根据不同平台事件类型进行不同的处理，我们将在[重载](#重载)一节中介绍。
:::

## 重载

我们在编写机器人时，常常会遇到这样一个问题：如何对私聊和群聊消息进行不同的处理？如何对不同平台的事件进行不同的处理？针对这些问题，NoneBot 提供了一个便捷而高效的解决方案 ── 重载。简单来说，依赖函数会根据其参数的类型注解来决定是否执行，忽略不符合其参数类型注解的情况。这样，我们就可以通过修改事件参数类型注解来实现对不同事件的处理，或者修改 `Bot` 参数类型注解来实现使用不同平台的接口。我们以 `OneBot` 协议适配器为例：

```python {4,8}
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent

@matcher.handle()
async def handle_private(event: PrivateMessageEvent):
    await matcher.finish("私聊消息")

@matcher.handle()
async def handle_group(event: GroupMessageEvent):
    await matcher.finish("群聊消息")
```

这样，机器人用户就会在私聊和群聊中分别收到不同的回复。同样的，我们也可以通过修改 `Bot` 参数类型注解来实现使用不同平台的接口：

```python
from nonebot.adapters.console import Bot as ConsoleBot
from nonebot.adapters.onebot.v11 import Bot as OneBot

@matcher.handle()
async def handle_console(bot: ConsoleBot):
    await bot.bell()

@matcher.handle()
async def handle_onebot(bot: OneBot):
    await bot.send_group_message(group_id=123123, message="OneBot")
```

:::caution 注意
重载机制对所有的参数类型注解都有效，因此，依赖注入也可以使用这个特性来对不同的返回值进行处理。

但 Bot、Event 和 Matcher 三者的参数类型注解具有最高检查优先级，如果三者任一类型注解不匹配，那么其他依赖注入将不会执行（如：`Depends`）。
:::

:::tip 提示
如何更好地编写一个跨平台的插件，我们将在[最佳实践](../best-practice/multi-adapter.mdx)中介绍。
:::
