# NoneBot

[![License](https://img.shields.io/pypi/l/none-bot.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/none-bot.svg)](https://pypi.python.org/pypi/none-bot)

NoneBot 是一个基于 [酷 Q](https://cqp.cc/) 的 Python 异步 QQ 机器人框架，框架与酷 Q 交互的部分使用 [aiocqhttp](https://github.com/richardchien/python-aiocqhttp)，后者是 [CoolQ HTTP API 插件](https://github.com/richardchien/coolq-http-api) 的一个 Python 异步 SDK。NoneBot 仅支持 Python 3.6+ 及 CoolQ HTTP API 插件 v4.2+。

NoneBot 本身不包含任何实际功能，仅仅提供处理消息、解析命令等核心功能，框架的使用者需要使用框架提供的接口，以插件的形式来编写具体功能。

文档暂时还没完成，请先参考 [none.plugins](none/plugins)、[demo](demo) 模块和 [richardchien/maruko](https://github.com/richardchien/maruko) 项目中的使用方式。
