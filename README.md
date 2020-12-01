<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot

_✨ Python 异步机器人框架 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/nonebot/nonebot2/master/LICENSE">
    <img src="https://img.shields.io/github/license/nonebot/nonebot2.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot2">
    <img src="https://img.shields.io/pypi/v/nonebot2.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">
  <img src="https://img.shields.io/badge/cqhttp-11+-black.svg" alt="cqhttp"><br />
  <a href="https://jq.qq.com/?_wv=1027&k=5OFifDh">
    <img src="https://img.shields.io/badge/qq%E7%BE%A4-768887710-orange.svg" alt="QQ Chat">
  </a>
  <a href="https://t.me/cqhttp">
    <img src="https://img.shields.io/badge/telegram-chat-blue.svg" alt="Telegram Chat">
  </a>
  <a href="https://jq.qq.com/?_wv=1027&k=5Nl0zhE">
    <img src="https://img.shields.io/badge/%E7%89%88%E6%9C%AC%E5%8F%91%E5%B8%83%E7%BE%A4-218529254-green.svg" alt="QQ Release">
  </a>
  <a href="https://t.me/cqhttp_release">
    <img src="https://img.shields.io/badge/版本发布频道-join-green.svg" alt="Telegram Release">
  </a>
</p>

<p align="center">
  <a href="https://v2.nonebot.dev/">文档</a>
  ·
  <a href="https://v2.nonebot.dev/guide/installation.html">安装</a>
  ·
  <a href="https://v2.nonebot.dev/guide/getting-started.html">开始使用</a>
  ·
  <a href="#插件">文档打不开？</a>
</p>

## 简介

NoneBot2 是一个可扩展的 Python 异步机器人框架，它会对机器人收到的事件进行解析和处理，并以插件化的形式，按优先级分发给事件所对应的事件响应器，来完成具体的功能。

除了起到解析事件的作用，NoneBot 还为插件提供了大量实用的预设操作和权限控制机制。对于命令处理，它更是提供了完善且易用的会话机制和内部调用机制，以分别适应命令的连续交互和插件内部功能复用等需求。

得益于 Python 的 [asyncio](https://docs.python.org/3/library/asyncio.html) 机制，NoneBot 处理事件的吞吐量有了很大的保障，再配合 WebSocket 通信方式（也是最建议的通信方式），NoneBot 的性能可以达到 HTTP 通信方式的两倍以上，相较于传统同步 I/O 的 HTTP 通信，更是有质的飞跃。

## 特色

NoneBot2 的驱动框架 `Driver` 以及通信协议 `Adapter` 均可**自定义**，并且可以作为插件进行**替换/添加**！

目前 NoneBot2 内置的驱动框架：

- [FastAPI](https://fastapi.tiangolo.com/)

目前 NoneBot2 内置的协议适配：

- [CQHTTP(OneBot) 协议](https://github.com/howmanybots/onebot/blob/master/README.md)
- [钉钉](https://ding-doc.dingtalk.com/doc#/serverapi2/krgddi) _开发中_
- [Telegram](https://core.telegram.org/bots/api) _计划中_

## 即刻开始

~~完整~~文档可以在 [这里](https://v2.nonebot.dev/) 查看。

懒得看文档？下面是快速安装指南：~~这是坏文明~~

1. (可选)使用你喜欢的 Python 环境管理工具创建新的虚拟环境。
2. 使用 `pip` (或其他) 安装 NoneBot 脚手架。

   ```bash
   pip install nb-cli
   ```

3. 使用脚手架创建项目

   ```bash
   nb create
   ```

## 插件

此外，NoneBot2 还有丰富的官方以及第三方现成的插件供大家使用：

- [NoneBot-Plugin-Docs](https://github.com/nonebot/nonebot2/tree/master/packages/nonebot-plugin-docs)：离线文档至本地使用(别再说文档打不开了！)

  ```bash
  nb plugin install nonebot_plugin_docs
  ```

- 其他插件请查看 [插件商店](https://v2.nonebot.dev/plugin-store.html)

## 贡献

如果你在使用过程中发现任何问题，可以 [提交 issue](https://github.com/nonebot/nonebot2/issues/new) 或自行 fork 修改后提交 pull request。

如果你要提交 pull request，请确保你的代码风格和项目已有的代码保持一致，遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)，变量命名清晰，有适当的注释。
