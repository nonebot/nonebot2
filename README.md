<div align=center>
  <img src="./docs/.vuepress/public/logo.png" width="200" height="200">

# NoneBot

[![License](https://img.shields.io/github/license/nonebot/nonebot2.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/nonebot2.svg)](https://pypi.python.org/pypi/nonebot2)
![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![CQHTTP Version](https://img.shields.io/badge/cqhttp-11+-black.svg)
[![QQ 群](https://img.shields.io/badge/qq%E7%BE%A4-768887710-orange.svg)](https://jq.qq.com/?_wv=1027&k=5OFifDh)
[![Telegram](https://img.shields.io/badge/telegram-chat-blue.svg)](https://t.me/cqhttp)
[![QQ 版本发布群](https://img.shields.io/badge/%E7%89%88%E6%9C%AC%E5%8F%91%E5%B8%83%E7%BE%A4-218529254-green.svg)](https://jq.qq.com/?_wv=1027&k=5Nl0zhE)
[![Telegram 版本发布频道](https://img.shields.io/badge/%E7%89%88%E6%9C%AC%E5%8F%91%E5%B8%83%E9%A2%91%E9%81%93-join-green.svg)](https://t.me/cqhttp_release)

</div>

## 简介

NoneBot2 是一个可扩展的 Python 异步机器人框架，它会对机器人收到的消息进行解析和处理，并以插件化的形式，分发给消息所对应的命令处理器和自然语言处理器，来完成具体的功能。

除了起到解析消息的作用，NoneBot 还为插件提供了大量实用的预设操作和权限控制机制，尤其对于命令处理器，它更是提供了完善且易用的会话机制和内部调用机制，以分别适应命令的连续交互和插件内部功能复用等需求。

目前 NoneBot2 在 [FastAPI](https://fastapi.tiangolo.com/) 的基础上封装了与 [CQHTTP(OneBot) 协议](http://cqhttp.cc/)插件的网络交互。

得益于 Python 的 [asyncio](https://docs.python.org/3/library/asyncio.html) 机制，NoneBot 处理消息的吞吐量有了很大的保障，再配合 WebSocket 通信方式（也是最建议的通信方式），NoneBot 的性能可以达到 HTTP 通信方式的两倍以上，相较于传统同步 I/O 的 HTTP 通信，更是有质的飞跃。

需要注意的是，NoneBot 仅支持 Python 3.7+ 及 CQHTTP(OneBot) 插件 v11+。

## 文档

文档目前尚未完成，「API」部分由 sphinx 自动生成，你可以在 [这里](https://v2.nonebot.dev/) 查看。

## 贡献

如果你在使用过程中发现任何问题，可以 [提交 issue](https://github.com/nonebot/nonebot2/issues/new) 或自行 fork 修改后提交 pull request。

如果你要提交 pull request，请确保你的代码风格和项目已有的代码保持一致，遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)，变量命名清晰，有适当的注释。
