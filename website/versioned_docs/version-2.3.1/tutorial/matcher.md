---
sidebar_position: 4
description: 响应接收到的特定事件

options:
  menu:
    - category: tutorial
      weight: 60
---

# 事件(消息)响应器

事件响应器（Matcher）是对接收到的事件进行响应的基本单元，所有的事件响应器都继承自 `Matcher` 基类。

Matcher用于将消息和规则进行匹配/检查/筛选, 当消息匹配时执行`@matcher_obj.handle()`装饰的函数

# 定义响应规则(Matcher/Rule/事件响应器辅助函数)

事件响应器辅助函数具体细节已移至[事件响应器进阶](../advanced/matcher.md)

响应器(Matcher)对消息进行初筛, 常用的有

- on_message() 处理所有消息(无限制)
- on_command() 匹配指令例如"/echo hello world"中匹配"/echo"
- on_regex() 对整个消息文本进行正则表达式匹配

Rule对消息进行二次筛选, 常用的有:

- to_me() 私聊或 `@bot`或`@全体成员` 时才会响应

经过Matcher和Rule筛选的消息会触发函数进行处理

## 在哪导入

**matcher**
编辑器中输入`from nonebot import on`以后, 大部分编辑器已经能够给出代码提示

示例`from nonebot import on_message, on_regex`

**rule**
示例`from nonebot.rule import to_me`

## on_command示例

```python {3} title=weather/__init__.py
from nonebot import on_command
from nonebot.rule import to_me

weather = on_command("天气", rule=to_me(), aliases={"weather", "查天气"}, priority=10, block=True)
```

:::tip 提示
如果一条消息中包含“@机器人”或以“机器人的昵称”开始，例如 `@bot /天气` 时，协议适配器会将 `event.is_tome()`(is to me)
判断为 `True` ，同时也会自动去除 `@bot`，即事件响应器收到的信息内容为 `/天气`，方便进行命令匹配。
:::

这样，我们就获得了一个可以响应 `天气`、`weather`、`查天气`(aliases可以设置命令的别名) 三个命令的响应规则，需要私聊或 `@bot`
或`@全体成员` 时才会响应，优先级为 10 (越小越先)，阻断事件传播(block=True, 不响应优先级值更大的matcher)
的事件响应器了。这些内容的意义和使用方法将会在后续的章节中一一介绍。

:::tip 提示
需要注意的是，不同的辅助函数有不同的可选参数，在使用之前可以参考[事件响应器进阶](../advanced/matcher.md)或编辑器的提示。
:::

## on_regex示例

```
on_regex(r"^1$", flags=re.IGNORECASE, priority=5, block=True)
```

这段代码会将所有消息进行正则表达式匹配, 当消息文本为"1"的时候(匹配"^1$")满足该matcher
