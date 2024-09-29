---
sidebar_position: 4
description: 响应接收到的特定事件

options:
  menu:
    - category: tutorial
      weight: 60
---

# 事件响应器

事件响应器（Matcher）是对接收到的事件进行响应的基本单元，所有的事件响应器都继承自 `Matcher` 基类。

在 NoneBot 中，事件响应器可以通过一系列特定的规则**筛选**出**具有某种特征的事件**，并按照**特定的流程**交由**预定义的事件处理依赖**进行处理。例如，在[快速上手](../quick-start.mdx)中，我们使用了内置插件 `echo` ，它定义的事件响应器能响应机器人用户发送的“/echo hello world”消息，提取“hello world”信息并作为回复消息发送。

## 事件响应器辅助函数

NoneBot 中所有事件响应器均继承自 `Matcher` 基类，但直接使用 `Matcher.new()` 方法创建事件响应器过于繁琐且不能记录插件信息。因此，NoneBot 中提供了一系列“事件响应器辅助函数”（下称“辅助函数”）来辅助我们用**最简的方式**创建**带有不同规则预设**的事件响应器，提高代码可读性和书写效率。通常情况下，我们只需要使用辅助函数即可完成事件响应器的创建。

在 NoneBot 中，辅助函数以 `on()` 或 `on_<type/rule>()` 形式出现（例如 `on_command()`），调用后根据不同的参数返回一个 `Type[Matcher]` 类型的新事件响应器。

目前 NoneBot 提供了多种功能各异的辅助函数、具有共同命令名称前缀的命令组以及具有共同参数的响应器组，均可以从 `nonebot` 模块直接导入使用，具体内容参考[事件响应器进阶](../advanced/matcher.md)。

## 创建事件响应器

在上一节[创建插件](./create-plugin.md#创建插件)中，我们创建了一个 `weather` 插件，现在我们来实现他的功能。

我们直接使用 `on_command()` 辅助函数来创建一个事件响应器：

```python {3} title=weather/__init__.py
from nonebot import on_command

weather = on_command("天气")
```

这样，我们就获得一个名为 `weather` 的事件响应器了，这个事件响应器会对 `/天气` 开头的消息进行响应。

:::tip 提示
如果一条消息中包含“@机器人”或以“机器人的昵称”开始，例如 `@bot /天气` 时，协议适配器会将 `event.is_tome()` 判断为 `True` ，同时也会自动去除 `@bot`，即事件响应器收到的信息内容为 `/天气`，方便进行命令匹配。
:::

### 为事件响应器添加参数

在辅助函数中，我们可以添加一些参数来对事件响应器进行更加精细的调整，例如事件响应器的优先级、匹配规则等。例如：

```python {4} title=weather/__init__.py
from nonebot import on_command
from nonebot.rule import to_me

weather = on_command("天气", rule=to_me(), aliases={"weather", "查天气"}, priority=10, block=True)
```

这样，我们就获得了一个可以响应 `天气`、`weather`、`查天气` 三个命令的响应规则，需要私聊或 `@bot` 时才会响应，优先级为 10（越小越优先），阻断事件向后续优先级传播的事件响应器了。这些内容的意义和使用方法将会在后续的章节中一一介绍。

:::tip 提示
需要注意的是，不同的辅助函数有不同的可选参数，在使用之前可以参考[事件响应器进阶 - 基本辅助函数](../advanced/matcher.md#基本辅助函数)或 [API 文档](../api/plugin/on.md#on)。
:::
