# 介绍

::: tip 提示
如果在阅读本文档时遇到难以理解的词汇，请随时查阅 [术语表](/glossary.md) 或使用 [Google 搜索](https://www.google.com/ncr)。
:::

::: tip 提示
初次使用时可能会觉得这里的介绍过于枯燥，可以先简单略读之后直接前往 [安装](/guide/installation.md) 查看安装方法，并进行后续的基础使用教程。
:::

NoneBot 是一个基于 [酷 Q](https://cqp.cc/) 的 Python 异步 QQ 机器人框架，它会对 QQ 机器人收到的消息进行解析和处理，并以插件化的形式，分发给消息所对应的命令处理器和自然语言处理器，来完成具体的功能。

除了起到解析消息的作用，NoneBot 还为插件提供了大量实用的预设操作和权限控制机制，尤其对于命令处理器，它更是提供了完善且易用的会话机制和内部调用机制，以分别适应命令的连续交互和插件内部功能复用等需求。

NoneBot 在其底层与酷 Q 交互的部分使用 [python-aiocqhttp](https://github.com/richardchien/python-aiocqhttp) 库，后者是 [CoolQ HTTP API 插件](https://github.com/richardchien/coolq-http-api) 的一个 Python 异步 SDK，在 [Quart](https://pgjones.gitlab.io/quart/) 的基础上封装了与 CoolQ HTTP API 插件的网络交互。

得益于 Python 的 [asyncio](https://docs.python.org/3/library/asyncio.html) 机制，NoneBot 处理消息的吞吐量有了很大的保障，再配合 CoolQ HTTP API 插件可选的 WebSocket 通信方式（也是最建议的通信方式），NoneBot 的性能可以达到 HTTP 通信方式的两倍以上，相较于传统同步 I/O 的 HTTP 通信，更是有质的飞跃。

需要注意的是，NoneBot 仅支持 Python 3.6+ 及 CoolQ HTTP API 插件 v4.2+。

## 它如何工作？

NoneBot 的运行离不开酷 Q 和 CoolQ HTTP API 插件。酷 Q 扮演着「无头 QQ 客户端」的角色，它进行实际的消息、通知、请求的接收和发送，当酷 Q 收到消息时，它将这个消息包装为一个事件（通知和请求同理），并通过它自己的插件机制将事件传送给 CoolQ HTTP API 插件，后者再根据其配置中的 `post_url` 或 `ws_reverse_event_url` 等项来将事件发送至 NoneBot。

在 NoneBot 收到事件前，它底层的 aiocqhttp 实际已经先看到了事件，aiocqhttp 根据事件的类型信息，通知到 NoneBot 的相应函数。特别地，对于消息类型的事件，还将消息内容转换成了 `aiocqhttp.message.Message` 类型，以便处理。

NoneBot 的事件处理函数收到通知后，对于不同类型的事件，再做相应的预处理和解析，然后调用对应的插件，并向其提供适合此类事件的会话（Session）对象。NoneBot 插件的编写者要做的，就是利用 Session 对象中提供的数据，在插件的处理函数中实现所需的功能。

## 特色

- 基于异步 I/O
- 同时支持 HTTP 和反向 WebSocket 通信方式
- 支持命令、自然语言处理器等多种插件形式
- 提供直观的交互式会话接口
- 命令和自然语言处理器提供权限控制机制
- 支持在命令会话运行过程中切换到其它命令或自然语言处理器
- 多种方式渲染要发送的消息内容，使对话足够自然
