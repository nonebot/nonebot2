---
sidebar: auto
---

# 术语表

## 酷 Q

[酷 Q](https://cqp.cc) 是一个易语言编写的 QQ 机器人平台，其本身没有任何具体的功能，只是负责实现 QQ 协议，并以 DLL 导出函数的形式向插件提供 API 和事件上报。

## CoolQ HTTP API 插件

[CoolQ HTTP API 插件](https://github.com/richardchien/coolq-http-api) 是酷 Q 的一个第三方插件，用于将酷 Q 所提供的所有 DLL 接口转换为 HTTP 或 WebSocket 的 web 形式，从而使利用任意语言编写酷 Q 插件成为可能。

有时被称为 cqhttp、CQHttp、酷 Q HTTP API 等。

## aiocqhttp

[aiocqhttp](https://github.com/richardchien/python-aiocqhttp)（或称 python-aiocqhttp）是 CoolQ HTTP API 插件的一个 Python 异步 SDK，基于 asyncio，在 Quart 的基础上封装了与 CoolQ HTTP API 插件的网络交互。

## asyncio

[asyncio](https://docs.python.org/3/library/asyncio.html) 是 Python 3.4 引入的一个模块，实际上它是 Python 中整个基于事件循环（Event Loop）的异步 I/O 编程机制。

## Quart

[Quart](https://pgjones.gitlab.io/quart/) 是一个基于异步 I/O 的 web 框架，支持 HTTP 和 WebSocket，是 aiocqhttp 的基础。

## 异步 I/O

有时直接称为「异步」，是一种对 I/O 操作的处理方式，它可以在单个线程内实现非阻塞 I/O，即在 I/O 操作进行时，仍可以调度程序的其它部分。在 Python 3.4+ 中，asyncio 模块提供的异步 I/O 调度的基本单位是「协程（Coroutine）」，通过 `await` 关键字即可在进行 I/O 操作时将程序的执行权转移给其它协程，直到 I/O 结束再次被唤起。

## 通信方式

CoolQ HTTP API 插件中的一个术语，表示其与通过 web 技术编写的酷 Q 插件之间通信的手段。

目前 CoolQ HTTP API 插件支持 HTTP、WebSocket、反向 WebSocket 三种通信方式，见 [通信方式](https://cqhttp.cc/docs/#/CommunicationMethods)，NoneBot 支持其中的 HTTP 和反向 WebSocket。

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

## 命令处理器

或称为「命令处理函数」，有时也简称为「命令」，是 NoneBot 插件中实际用于实现某个命令功能的函数。

通过 `none.on_command` 装饰器可以将一个函数注册为命令处理器，例如：

```python
from none import on_command

@on_command('echo')
async def echo(session):
    pass
```
