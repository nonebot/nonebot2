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
    <img src="https://codecov.io/gh/nonebot/nonebot2/branch/master/graph/badge.svg?token=2P0G0VS7N4"/>
  </a>
  <br />
  <a href="https://onebot.dev/">
    <img src="https://img.shields.io/badge/OneBot-v11-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="cqhttp">
  </a>
  <a href="http://github.com/mamoe/mirai">
    <img src="https://img.shields.io/badge/mirai-HTTP-lightgrey?style=social">
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
    <img src="https://img.shields.io/badge/QQ%E9%A2%91%E9%81%93-Bot-lightgrey?style=social&logo=data:image/png;base64,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" alt="QQ频道">
  </a>
  <br />
  <a href="https://jq.qq.com/?_wv=1027&k=5OFifDh">
    <img src="https://img.shields.io/badge/qq%E7%BE%A4-768887710-orange?style=flat-square" alt="QQ Chat">
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
  <a href="https://v2.nonebot.dev/guide/installation.html">安装</a>
  ·
  <a href="https://v2.nonebot.dev/guide/getting-started.html">开始使用</a>
  ·
  <a href="#插件">文档打不开？</a>
</p>

<!-- TODO: asciinema for install -->

## 简介

NoneBot2 是一个现代、跨平台、可扩展的 Python 聊天机器人框架，它基于 Python 的类型注解和异步特性，能够为你的需求实现提供便捷灵活的支持。

## 特色

- 异步优先：基于 Python 的异步特性，即使是~~非常~~大量的消息，也能吞吐自如
- 易于开发：配合 NB-CLI 脚手架，代码编写上手简单，没有过多的冗余代码，可以让开发者专注于业务逻辑
- 生而可靠：100% 类型注解覆盖，配合编辑器的类型推导功能，能将绝大多数的 Bug 杜绝在编辑器中 ([编辑器支持](https://v2.nonebot.dev/docs/start/editor-support))
- 社区丰富：社区用户众多，直接和间接用户超过十万人，每天都有大量的活跃用户 ([社区资源](#社区资源))
- 海纳百川：一个框架，支持多个聊天软件平台，可自定义通信协议
  - [OneBot 协议](https://onebot.dev/) (QQ 等)
  - [Mirai-API-HTTP 协议](https://github.com/project-mirai/mirai-api-http)
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

- 其他插件请查看 [商店](https://v2.nonebot.dev/store.html)

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
