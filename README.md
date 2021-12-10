<!-- markdownlint-disable MD033 MD041-->
<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>
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
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fnonebot%2Fnonebot2?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fnonebot%2Fnonebot2.svg?type=shield"/></a>
  <img src="https://img.shields.io/badge/python-3.7.3+-blue" alt="python"><br />
  <a href="https://github.com/howmanybots/onebot/blob/master/README.md">
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
<!-- markdownlint-enable MD033 -->


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fnonebot%2Fnonebot2.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fnonebot%2Fnonebot2?ref=badge_large)

## 简介

NoneBot2 是一个可扩展的 Python 异步机器人框架，它会对机器人收到的事件进行解析和处理，并以插件化的形式，按优先级分发给事件所对应的事件响应器，来完成具体的功能。

除了起到解析事件的作用，NoneBot 还为插件提供了大量实用的预设操作和权限控制机制。对于命令处理，它更是提供了完善且易用的会话机制和内部调用机制，以分别适应命令的连续交互和插件内部功能复用等需求。

得益于 Python 的 [asyncio](https://docs.python.org/3/library/asyncio.html) 机制，NoneBot 处理事件的吞吐量有了很大的保障，再配合 WebSocket 通信方式（也是最建议的通信方式），NoneBot 的性能可以达到 HTTP 通信方式的两倍以上，相较于传统同步 I/O 的 HTTP 通信，更是有质的飞跃。

## 特色

NoneBot2 的驱动框架 `Driver` 以及通信协议 `Adapter` 均可**自定义**，并且可以作为插件进行**替换/添加**！

目前 NoneBot2 内置的驱动框架：

- [FastAPI](https://fastapi.tiangolo.com/)
- [Quart](https://pgjones.gitlab.io/quart/) (异步 flask )

目前 NoneBot2 官方维护的协议适配：

- [OneBot(CQHTTP) 协议](https://github.com/howmanybots/onebot/blob/master/README.md) (QQ 等)
- [Mirai-API-HTTP 协议](https://github.com/project-mirai/mirai-api-http)
- [钉钉](https://ding-doc.dingtalk.com/document#/org-dev-guide/elzz1p)
- [Telegram](https://core.telegram.org/bots/api)
- [飞书](https://open.feishu.cn/document/home/index)

更多：[商店](https://v2.nonebot.dev/store.html)

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

## 社区资源

### 常见问题

- [常见问题解答(FAQ)](https://faq.nonebot.dev/)

### 教程/实际项目/经验分享

- [awesome-nonebot](https://github.com/nonebot/awesome-nonebot)

### 插件

此外，NoneBot2 还有丰富的官方以及第三方现成的插件供大家使用：

- [NoneBot-Plugin-Docs](https://github.com/nonebot/nonebot2/tree/master/packages/nonebot-plugin-docs)：离线文档至本地使用(别再说文档打不开了！)

  ```bash
  nb plugin install nonebot_plugin_docs
  ```

  或者尝试以下镜像：

  - [文档镜像(中国境内)](https://nb2.baka.icu)
  - [文档镜像(vercel)](https://nonebot2-vercel-mirror.vercel.app)

- 其他插件请查看 [商店](https://v2.nonebot.dev/store.html)

## 贡献

如果你在使用过程中发现任何问题，可以 [提交 issue](https://github.com/nonebot/nonebot2/issues/new) 或自行 fork 修改后提交 pull request。

如果你要提交 pull request，请确保你的代码风格和项目已有的代码保持一致，遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)，变量命名清晰，有适当的注释。

## 许可证

`NoneBot` 采用 `MIT` 协议开源，协议文件参考 [LICENSE](./LICENSE)。

特别的，由于 `mirai` 使用 `AGPLv3` 协议并要求使用 `mirai` 的软件同样以 `AGPLv3` 协议开源，本项目 `mirai` 适配器部分（即 [`packages/nonebot-adapter-mirai`](./packages/nonebot-adapter-mirai/) 目录）以 `AGPLv3` 协议开源，协议文件参考 [LICENSE](./packages/nonebot-adapter-mirai/LICENSE)。