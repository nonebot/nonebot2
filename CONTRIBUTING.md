# NoneBot2 贡献指南

首先，感谢你愿意为 NoneBot2 贡献自己的一份力量！

本指南旨在引导你更加恰当地为 NoneBot2 做贡献，请务必认真阅读。

## 提交 Issue

在提交 Issue 前，我们建议你先查看 [FAQ](https://github.com/nonebot/discussions/discussions/13) 与 [已有的 Issues](https://github.com/nonebot/nonebot2/issues)，以防重复提交。

### 报告漏洞

NoneBot2 仍然是一个不够稳定的开发中项目，如果你在使用过程中发现问题并确信是由 NoneBot2 引起的，欢迎提交 Issue。

### 建议功能

NoneBot2 还未进入正式版，欢迎建议我们要加入哪些新功能。不过由于 NoneBot 已经进入 beta 开发阶段，请尽量让新的功能不破坏对旧版本的兼容性。

## Pull Request

NoneBot 的 commit message 遵循 [gitmoji](https://gitmoji.dev/) 规范，在 commit 时请牢记这一点。

NoneBot 使用 [Poetry](https://python-poetry.org/) 管理项目依赖，由于 pre-commit 也经其管理，所以在此一并说明。

下面的命令能在已安装 Poetry 和 npm 的情况下帮你快速配置开发环境。

```sh
poetry install
precommit install
npm -g i gitmoji-cli
gitmoji -i
```

### 撰写文档

NoneBot2 的文档使用 docusaurus，它有一些 [Markdown 特性](https://docusaurus.io/zh-CN/docs/markdown-features) 可能会帮助到你。

NoneBot2 文档并没有具体的行文风格规范，但我们建议你尽量写得简单易懂。

如果你需要在本地预览修改后的文档，可以使用 yarn 或 npm 等 Nodejs 的依赖管理工具安装文档依赖后自行部署。

### 参与开发

NoneBot2 的代码风格遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 与 [PEP 484](https://www.python.org/dev/peps/pep-0484/) 规范，请确保你的代码风格和项目已有的代码保持一致，变量命名清晰，有适当的注释与测试代码。

## 为社区做贡献

你可以在 NoneBot 商店上架自己的适配器、插件、机器人，具体步骤可参考 [发布插件](https://v2.nonebot.dev/docs/next/advanced/publish-plugin) 一节。

我们仅对插件的兼容性进行简单测试，并在下一个版本发布前处理不兼容的插件。

虽然对插件的内容没有严格限制，但我们还是建议在上架插件之前先查看商店有无功能一致的插件。

如果你想要上架的插件是其他插件的 fork，请遵守开源协议，以及补充自己相较于原版的区别。

## Git 工作流

`dev` 分支 为 NoneBot 的开发分支，如无特殊情况请将 Pull Request 提交到该分支。

如果你已经是 NoneBot 团队的成员，请注意千万不要直接 commit 到 `dev` 分支。你必须创建新的分支以提出 Pull Request，并邀请其他团队成员审计代码，以防止开发分支出错。

如果你不是 NoneBot 团队的成员，自行 fork 后即可提出 Pull Request，请尤其注意在前面提到的 commit message 规范，
