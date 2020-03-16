---
sidebar: auto
---

# 术语表

## 酷Q

[酷Q](https://cqp.cc) 是一个易语言编写的 QQ 机器人平台，其本身没有任何具体的功能，只是负责实现 QQ 协议，并以 DLL 导出函数的形式向插件提供 API 和事件上报。

## CQHTTP 插件

[CQHTTP 插件](https://cqhttp.cc/)即 CoolQ HTTP API 插件，是 酷Q 的一个第三方插件，用于将 酷Q 所提供的所有 DLL 接口转换为 HTTP 或 WebSocket 的 web 形式，从而使利用任意语言编写 酷Q 插件成为可能。

有时被称为 cqhttp、CQHTTP、酷Q HTTP API 等。

## aiocqhttp

[aiocqhttp](https://github.com/richardchien/python-aiocqhttp)（或称 python-aiocqhttp）是 CQHTTP 插件的一个 Python 异步 SDK，基于 asyncio，在 Quart 的基础上封装了与 CQHTTP 插件的网络交互。

## asyncio

[asyncio](https://docs.python.org/3/library/asyncio.html) 是 Python 3.4 引入的一个模块，实际上它是 Python 中整个基于事件循环（Event Loop）的异步 I/O 编程机制。

## Quart

[Quart](https://pgjones.gitlab.io/quart/) 是一个基于异步 I/O 的 web 框架，支持 HTTP 和 WebSocket，是 aiocqhttp 的基础。

## 异步 I/O

有时直接称为「异步」，是一种对 I/O 操作的处理方式，它可以在单个线程内实现非阻塞 I/O，即在 I/O 操作进行时，仍可以调度程序的其它部分。在 Python 3.4+ 中，asyncio 模块提供的异步 I/O 调度的基本单位是「协程（Coroutine）」，通过 `await` 关键字即可在进行 I/O 操作时将程序的执行权转移给其它协程，直到 I/O 结束再次被唤起。

## 通信方式

CQHTTP 插件中的一个术语，表示其与通过 web 技术编写的 酷Q 插件之间通信的手段。

目前 CQHTTP 插件支持 HTTP、WebSocket、反向 WebSocket 三种通信方式，见 [通信方式](https://cqhttp.cc/docs/#/CommunicationMethods)，NoneBot 支持其中的 HTTP 和反向 WebSocket。

## 负载均衡

多个 QQ 连接到同一个后端，使用同一套逻辑分别服务不同的用户和群，以防止单个 QQ 无法承受过大的消息量或被腾讯封禁。

## 命令

NoneBot 主要支持的插件形式之一，主要用于处理符合特定格式的、意图明确的用户消息，例如：

```
天气 南京 明天
/echo 喵喵喵
note.add 这是一条笔记
```

上面的每行都符合一种固定的格式，消息的第一个空格左边是命令的名字（可能包含命令的起始符和分隔符），右边是命令所需的参数，可能以空格分隔，或是完全作为单个参数。

你可以将命令理解为操作系统中的命令行程序，NoneBot 执行命令就像在 Shell 中运行程序一样：

```bash
docker run hello-world
```

## 可交互命令

能够和用户「对话」的命令，称为可交互命令。

## 命令处理器

或称为「命令处理函数」，有时也简称为「命令」，是 NoneBot 插件中实际用于实现某个命令功能的函数。

通过 `nonebot.on_command` 装饰器可以将一个函数注册为命令处理器，例如：

```python
from nonebot import on_command

@on_command('echo')
async def echo(session):
    pass
```

## 自然语言处理器

或称为「自然语言处理函数」，是 NoneBot 插件中用于将用户的自然语言消息解析为命令和参数的函数。

通过 `nonebot.on_natural_language` 装饰器可以将一个函数注册为自然语言处理器，例如：

```python
from nonebot import on_natural_language

@on_natural_language
async def _(session):
    pass
```

## 会话（Session）

是命令处理器、自然语言处理器等插件形式被调用时传入的一个包含有当前消息上下文的对象，它根据当前的插件形式的不同而不同，例如命令处理器拿到的 Session 是 `CommandSession` 类型，而自然语言处理器拿到的是 `NLPSession` 类型，不同类型的 Session 包含的属性不太一样，能进行的操作也有所区别。

特别地，命令的 Session 在需要和用户交互的情况下，会一直保留到下一次调用，以保证命令的多次交互能够共享数据。

## 表达（Expression）

是 NoneBot 支持的一种消息渲染的机制，可以通过随机选择或函数生成+字符串格式化的方式根据参数生成出自然的、不固定的消息回复，提升用户体验。

Expression 可以是一个 `str`、元素类型是 `str` 的序列（一般为 `list` 或 `tuple`）或返回类型为 `str` 的 `Callable`。

## CQ 码

是 酷Q 用来表示非文本消息的一种表示方法，形如 `[CQ:image,file=ABC.jpg]`。具体的格式规则，请参考 酷Q 文档的 [CQ 码](https://d.cqp.me/Pro/CQ%E7%A0%81) 和 CQHTTP 插件文档的 [CQ 码](https://cqhttp.cc/docs/#/CQCode)。

## 消息段

是 CQHTTP 定义的、和 CQ 码可以互相转换的一个消息表示格式，具体表示方式见 [消息格式](https://cqhttp.cc/docs/#/Message)。

除了纯文本消息段之外，每一个消息段都和一个 CQ 码对应，例如下面这个消息段：

```json
{
    "type": "face",
    "data": {
        "id": "14"
    }
}
```

对应的 CQ 码表示形式就是：

```
[CQ:face,id=14]
```

具体的，NoneBot 中使用 `MessageSegment` 类来表示消息段（继承自 aiocqhttp），例如，要创建上面这个消息段，可以使用如下代码：

```python
seg = MessageSegment(type="face", data={"id": "14"})
```

或：

```python
seg = MessageSegment.face(14)
```
