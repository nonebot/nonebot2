---
sidebar_position: 1
description: 注册适配器与指定平台交互

options:
  menu:
    weight: 20
    category: advanced
---

# 使用适配器

适配器 (Adapter) 是机器人与平台交互的核心桥梁，它负责在驱动器和机器人插件之间转换与传递消息。

## 适配器功能与组成

适配器通常有两种功能，分别是**接收事件**和**调用平台接口**。其中，接收事件是指将驱动器收到的事件消息转换为 NoneBot 定义的事件模型，然后交由机器人插件处理；调用平台接口是指将机器人插件调用平台接口的数据转换为平台指定的格式，然后交由驱动器发送，并接收接口返回数据。

为了实现这两种功能，适配器通常有四个部分组成：

- **适配器**：负责转换事件和调用接口，正确创建 Bot 对象并注册到 NoneBot 中。
- **Bot**：负责存储平台机器人相关信息，并提供回复事件的方法。
- **事件模型**：负责定义事件内容，以及事件主体对象。
- **消息序列**：负责正确序列化消息，以便机器人插件处理。

## 注册适配器

在使用适配器之前，我们需要先将适配器注册到驱动器中，这样适配器就可以通过驱动器接收事件和调用接口了。我们以 Console 适配器为例，来看看如何注册适配器：

```python {2,5} title=bot.py
import nonebot
from nonebot.adapters.console import Adapter

driver = nonebot.get_driver()
driver.register_adapter(Adapter)
```

我们首先需要从适配器模块中导入所需要的适配器类，然后通过驱动器的 `register_adapter` 方法将适配器注册到驱动器中即可。

## 获取已注册的适配器

NoneBot 提供了 `get_adapter` 方法来获取已注册的适配器，我们可以通过适配器的名称或类型来获取指定的适配器实例：

```python
import nonebot
from nonebot.adapters.console import Adapter

adapters = nonebot.get_adapters()
console_adapter = nonebot.get_adapter(Adapter)
console_adapter = nonebot.get_adapter(Adapter.get_name())
```

## 获取 Bot 对象

当前所有适配器已连接的 Bot 对象可以通过 `get_bots` 方法获取，这是一个以机器人 ID 为键的字典：

```python
import nonebot

bots = nonebot.get_bots()
```

我们也可以通过 `get_bot` 方法获取指定 ID 的 Bot 对象。如果省略 ID 参数，将会返回所有 Bot 中的第一个：

```python
import nonebot

bot = nonebot.get_bot("bot_id")
```

如果需要获取指定适配器连接的 Bot 对象，我们可以通过适配器的 `bots` 属性获取，这也是一个以机器人 ID 为键的字典：

```python
import nonebot
from nonebot.adapters.console import Adapter

console_adapter = nonebot.get_adapter(Adapter)
bots = console_adapter.bots
```

Bot 对象都具有一个 `self_id` 属性，它是机器人的唯一 ID，由适配器填写，通常为机器人的帐号 ID 或者 APP ID。

## 获取事件通用信息

适配器的所有事件模型均继承自 `Event` 基类，在[事件类型与重载](../appendices/overload.md)一节中，我们也提到了如何使用基类抽象方法来获取事件通用信息。基类所能提供的信息有如下几个方法：

- `get_type`：获取事件类型。
- `get_event_name`：获取事件名称。通常用于日志记录。
- `get_event_description`：获取事件描述。通常用于日志记录。
- `get_log_string`：获取事件日志字符串。
- `get_user_id`：获取事件主体 ID。
- `get_session_id`：获取事件会话 ID。
- `get_message`：获取事件消息。
- `get_plaintext`：获取事件消息的纯文本内容。
- `is_tome`：判断事件是否与机器人有关。

## 更多

官方支持的适配器和社区贡献的适配器均可在[商店](/store)中查看。如果你想要开发自己的适配器，可以参考[开发文档](../developer/adapter-writing.md)。欢迎通过商店发布你的适配器。
