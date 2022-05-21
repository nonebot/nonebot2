<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_✨ 跨平台 Python 异步机器人框架 ✨_
<!-- prettier-ignore-end -->

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/nonebot/nonebot2/master/LICENSE">
    <img src="https://img.shields.io/github/license/nonebot/nonebot2" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot2">
    <img src="https://img.shields.io/pypi/v/nonebot2" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.7.3+-blue" alt="python">
  <a href="https://codecov.io/gh/nonebot/nonebot2">
    <img src="https://codecov.io/gh/nonebot/nonebot2/branch/master/graph/badge.svg?token=2P0G0VS7N4" alt="codecov"/>
  </a>
  <a href="https://github.com/nonebot/nonebot2/actions/workflows/website-deploy.yml">
    <img src="https://github.com/nonebot/nonebot2/actions/workflows/website-deploy.yml/badge.svg?branch=master&event=push" alt="site"/>
  </a>
  <a href="https://results.pre-commit.ci/latest/github/nonebot/nonebot2/master">
    <img src="https://results.pre-commit.ci/badge/github/nonebot/nonebot2/master.svg" />
  </a>
  <br />
  <a href="https://onebot.dev/">
    <img src="https://img.shields.io/badge/OneBot-v11-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="cqhttp">
  </a>
  <a href="https://ding-doc.dingtalk.com/document#/org-dev-guide/elzz1p">
    <img src="https://img.shields.io/badge/%E9%92%89%E9%92%89-Bot-lightgrey?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAnFBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD4jUzeAAAAM3RSTlMAQKSRaA+/f0YyFevh29R3cyklIfrlyrGsn41tVUs48c/HqJm9uZdhX1otGwkF9IN8V1CX0Q+IAAABY0lEQVRYw+3V2W7CMBAF0JuNQAhhX9OEfYdu9///rUVWpagE27Ef2gfO+0zGozsKnv6bMGzAhkNytIe5gDdzrwtTCwrbI8x4/NF668NAxgI3Q3UtFi3TyPwNQtPLUUmDd8YfqGLNe4v22XwEYb5zoOuF5baHq2UHtsKe5ivWfGAwrWu2mC34QM0PoCAuqZdOmiwV+5BLyMRtZ7dTSEcs48rzWfzwptMLyzpApka1SJ5FtR4kfCqNIBPEVDmqoqgwUYY5plQOlf6UEjNoOPnuKB6wzDyCrks///TDza8+PnR109WQdxLo8RKWq0PPnuXG0OXKQ6wWLFnCg75uYYbhmMIVVdQ709q33aHbGIj6Duz+2k1HQFX9VwqmY8xYsEJll2ahvhWgsjYLHFRXvIi2Qb0jzMQCzC3FAoydxCma88UCzE3JCWwkjCNYyMUCzHX4DiuTMawEwwhW6hnshPhjZzzJfAH0YacpbmRd7QAAAABJRU5ErkJggg==" alt="ding">
  </a>
  <a href="https://core.telegram.org/bots/api">
    <img src="https://img.shields.io/badge/telegram-Bot-lightgrey?style=social&logo=telegram">
  </a>
  <a href="https://open.feishu.cn/document/home/index">
    <img src="https://img.shields.io/badge/%E9%A3%9E%E4%B9%A6-Bot-lightgrey?style=social&logo=data:image/png;base64,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" alt="feishu">
  </a>
  <a href="https://bot.q.qq.com/wiki/">
    <img src="https://img.shields.io/badge/QQ%E9%A2%91%E9%81%93-Bot-lightgrey?style=social&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMTIuODIgMTMwLjg5Ij48ZyBkYXRhLW5hbWU9IuWbvuWxgiAyIj48ZyBkYXRhLW5hbWU9IuWbvuWxgiAxIj48cGF0aCBkPSJNNTUuNjMgMTMwLjhjLTcgMC0xMy45LjA4LTIwLjg2IDAtMTkuMTUtLjI1LTMxLjcxLTExLjQtMzQuMjItMzAuMy00LjA3LTMwLjY2IDE0LjkzLTU5LjIgNDQuODMtNjYuNjQgMi0uNTEgNS4yMS0uMzEgNS4yMS0xLjYzIDAtMi4xMy4xNC0yLjEzLjE0LTUuNTcgMC0uODktMS4zLTEuNDYtMi4yMi0yLjMxLTYuNzMtNi4yMy03LjY3LTEzLjQxLTEtMjAuMTggNS40LTUuNTIgMTEuODctNS40IDE3LjgtLjU5IDYuNDkgNS4yNiA2LjMxIDEzLjA4LS44NiAyMS0uNjguNzQtMS43OCAxLjYtMS43OCAyLjY3djQuMjFjMCAxLjM1IDIuMiAxLjYyIDQuNzkgMi4zNSAzMS4wOSA4LjY1IDQ4LjE3IDM0LjEzIDQ1IDY2LjM3LTEuNzYgMTguMTUtMTQuNTYgMzAuMjMtMzIuNyAzMC42My04LjAyLjE5LTE2LjA3LS4wMS0yNC4xMy0uMDF6IiBmaWxsPSIjMDI5OWZlIi8+PHBhdGggZD0iTTMxLjQ2IDExOC4zOGMtMTAuNS0uNjktMTYuOC02Ljg2LTE4LjM4LTE3LjI3LTMtMTkuNDIgMi43OC0zNS44NiAxOC40Ni00Ny44MyAxNC4xNi0xMC44IDI5Ljg3LTEyIDQ1LjM4LTMuMTkgMTcuMjUgOS44NCAyNC41OSAyNS44MSAyNCA0NS4yOS0uNDkgMTUuOS04LjQyIDIzLjE0LTI0LjM4IDIzLjUtNi41OS4xNC0xMy4xOSAwLTE5Ljc5IDAiIGZpbGw9IiNmZWZlZmUiLz48cGF0aCBkPSJNNDYuMDUgNzkuNThjLjA5IDUgLjIzIDkuODItNyA5Ljc3LTcuODItLjA2LTYuMS01LjY5LTYuMjQtMTAuMTktLjE1LTQuODItLjczLTEwIDYuNzMtOS44NHM2LjM3IDUuNTUgNi41MSAxMC4yNnoiIGZpbGw9IiMxMDlmZmUiLz48cGF0aCBkPSJNODAuMjcgNzkuMjdjLS41MyAzLjkxIDEuNzUgOS42NC01Ljg4IDEwLTcuNDcuMzctNi44MS00LjgyLTYuNjEtOS41LjItNC4zMi0xLjgzLTEwIDUuNzgtMTAuNDJzNi41OSA0Ljg5IDYuNzEgOS45MnoiIGZpbGw9IiMwODljZmUiLz48L2c+PC9nPjwvc3ZnPg==" alt="QQ频道">
  </a>
  <br />
  <a href="https://jq.qq.com/?_wv=1027&k=5OFifDh">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-768887710-orange?style=flat-square" alt="QQ Chat Group">
  </a>
  <a href="https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&appChannel=share&inviteCode=7b4a3&appChannel=share&businessType=9&from=246610&biz=ka">
    <img src="https://img.shields.io/badge/QQ%E9%A2%91%E9%81%93-NoneBot-5492ff?style=flat-square" alt="QQ Channel">
  </a>
  <a href="https://t.me/botuniverse">
    <img src="https://img.shields.io/badge/telegram-botuniverse-blue?style=flat-square" alt="Telegram Channel">
  </a>
  <a href="https://discord.gg/VKtE6Gdc4h">
    <img src="https://discordapp.com/api/guilds/847819937858584596/widget.png?style=shield" alt="Discord Server">
  </a>
</p>

<p align="center">
  <a href="https://v2.nonebot.dev/">文档</a>
  ·
  <a href="https://v2.nonebot.dev/docs/start/installation">安装</a>
  ·
  <a href="https://v2.nonebot.dev/docs/tutorial/create-project">开始使用</a>
  ·
  <a href="#插件">文档打不开？</a>
</p>

<p align="center">
  <a href="https://asciinema.org/a/464654">
    <img src="https://v2.nonebot.dev/img/setup.svg">
  </a>
</p>

## 简介

NoneBot2 是一个现代、跨平台、可扩展的 Python 聊天机器人框架，它基于 Python 的类型注解和异步特性，能够为你的需求实现提供便捷灵活的支持。

## 特色

- 异步优先：基于 Python 的异步特性，即使是~~非常~~大量的消息，也能吞吐自如
- 易于开发：配合 NB-CLI 脚手架，代码编写上手简单，没有过多的冗余代码，可以让开发者专注于业务逻辑
- 生而可靠：100% 类型注解覆盖，配合编辑器的类型推导功能，能将绝大多数的 Bug 杜绝在编辑器中 ([编辑器支持](https://v2.nonebot.dev/docs/start/editor-support))
- 社区丰富：社区用户众多，直接和间接用户超过十万人，每天都有大量的活跃用户 ([社区资源](#社区资源))
- 海纳百川：一个框架，支持多个聊天软件平台，可自定义通信协议
  - [OneBot 协议](https://onebot.dev/) (QQ 等)
  - [钉钉](https://ding-doc.dingtalk.com/document#/org-dev-guide/elzz1p)
  - [Telegram](https://core.telegram.org/bots/api)
  - [飞书](https://open.feishu.cn/document/home/index)
  - [QQ 频道](https://bot.q.qq.com/wiki/)
- 坚实后盾：支持多种 web 框架，可自定义替换
  - [FastAPI](https://fastapi.tiangolo.com/)
  - [Quart](https://pgjones.gitlab.io/quart/) (异步 Flask)
  - [aiohttp](https://docs.aiohttp.org/en/stable/)
  - [httpx](https://www.python-httpx.org/)
  - [websockets](https://websockets.readthedocs.io/en/stable/)

更多：[概览](https://v2.nonebot.dev/docs/)

## 什么不是 NoneBot2

NoneBot2 不是某个平台或者协议的具体实现，它只负责和已有协议适配器通信，并处理接收到的事件。所以，“NoneBot 有 blabla 平台的 blabla 功能吗？”这种问题是与 NoneBot2 无关的。请在相应平台的功能文档中确认，或与相应平台的协议适配开发者联系。

NoneBot2 不是 NoneBot1 的替代品。事实上，它们都在被积极的维护着。但是，如果你想尝试一些新功能，或者想要支持更多的平台，可以考虑使用 NoneBot2。

> ~~NoneBot2 和 NoneBot1 的区别，就像是 VisualStudio Code 和 VisualStudio 一样~~

## 即刻开始

~~完整~~文档可以在 [这里](https://v2.nonebot.dev/) 查看。

懒得看文档？下面是快速安装指南：

1. (**强烈建议**)使用你喜欢的 Python 环境管理工具创建新的虚拟环境。

2. 使用 `pip` (或其他) 安装 NoneBot 脚手架。

   ```bash
   pip install nb-cli
   ```

3. 使用脚手架创建项目

   ```bash
   nb create
   ```

## 社区资源

### 常见问题

- [常见问题解答(FAQ)](https://faq.nonebot.dev/)
- [论坛(Discussion)](https://discussions.nonebot.dev/)

### 教程/实际项目/经验分享

- [awesome-nonebot](https://github.com/nonebot/awesome-nonebot)

### 插件

此外，NoneBot2 还有丰富的官方以及第三方现成的插件供大家使用：

- [NoneBot-Plugin-Docs](https://github.com/nonebot/nonebot2/tree/master/packages/nonebot-plugin-docs)：离线文档至本地项目使用 (别再说文档打不开了！)

  在项目目录下执行：

  ```bash
  nb plugin install nonebot_plugin_docs
  ```

  或者尝试以下镜像：

  - [文档镜像(中国境内)](https://nb2.baka.icu)
  - [文档镜像(Vercel)](https://nonebot2-vercel-mirror.vercel.app)

- 其他插件请查看 [商店](https://v2.nonebot.dev/store)

## 许可证

`NoneBot` 采用 `MIT` 许可证进行开源

```text
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## 贡献

请参考 [贡献指南](./CONTRIBUTING.md)

### 鸣谢

感谢以下开发者对 NoneBot2 作出的贡献：

<a href="https://github.com/nonebot/nonebot2/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=nonebot/nonebot2" />
</a>
