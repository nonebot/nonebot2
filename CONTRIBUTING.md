# NoneBot2 贡献指南

首先，感谢你愿意为 NoneBot2 贡献自己的一份力量！

本指南旨在引导你更规范地向 NoneBot2 提交贡献，请务必认真阅读。

## 提交 Issue

在提交 Issue 前，我们建议你先查看 [FAQ](https://github.com/nonebot/discussions/discussions/13) 与 [已有的 Issues](https://github.com/nonebot/nonebot2/issues)，以防重复提交。

### 报告问题、故障与漏洞

NoneBot2 仍然是一个不够稳定的开发中项目，如果你在使用过程中发现问题并确信是由 NoneBot2 引起的，欢迎提交 Issue。

### 建议功能

NoneBot2 还未进入正式版，欢迎在 Issue 中提议要加入哪些新功能。

为了让其他开发者们更好地理解你的意图, 请认真填写预期行为等内容, 如果可能, 可以提出可行的解决方案猜想

## Pull Request

### Commit 提交规范

NoneBot 的 commit message 格式遵循 [gitmoji](https://gitmoji.dev/) 规范，在创建 commit 时请牢记这一点。

NoneBot 使用 [Poetry](https://python-poetry.org/) 管理项目依赖，由于 pre-commit 也经其管理，所以在此一并说明。

下面的命令能在已安装 Poetry 和 npm 的情况下帮你快速配置开发环境。

```sh
poetry install
precommit install
npm -g i gitmoji-cli
gitmoji -i
```

请确保你的每一条 commit 都有清晰的描述它做了什么, 一个 commit 尽量只做一件事情。

### 撰写文档

NoneBot2 的文档使用 docusaurus，它有一些 [Markdown 特性](https://docusaurus.io/zh-CN/docs/markdown-features) 可能会帮助到你。

NoneBot2 文档并没有具体的行文风格规范，但我们建议你尽量写得简单易懂。

如果你需要在本地预览修改后的文档，可以使用 yarn 或 npm 等 Nodejs 的依赖管理工具安装文档依赖后自行部署。

### 参与开发

NoneBot2 的代码风格遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 与 [PEP 484](https://www.python.org/dev/peps/pep-0484/) 规范，请确保你的代码风格和项目已有的代码保持一致，变量命名清晰，有适当的注释与测试代码。

## 为社区做贡献

你可以在 NoneBot 商店上架自己的适配器、插件、机器人，具体步骤可参考 [发布插件](https://v2.nonebot.dev/docs/next/advanced/publish-plugin) 一节。

我们仅对插件的兼容性进行简单测试，并会在下一个版本发布前对与该版本不兼容的插件作出处理。

虽然对插件的内容没有严格限制，但我们还是建议在上架插件之前先查看商店有无功能一致的插件。如果你想要上架商店的插件的功能与现有插件的功能不完全重合，请在插件说明中补充与现有插件存在的区别。

同时，如果你参考或基于他人发行的代码进行开发，请注意遵守各代码所使用的开源许可协议。

## Git 工作流

`dev` 分支 为 NoneBot 的开发分支，如无特殊情况请将 Pull Request 提交到该分支。

如果你不是 NoneBot 团队的成员，可在 fork 本仓库后，向本仓库的 `dev` 分支发起 Pull Request 提交贡献，注意遵循先前提到的 commit message 规范创建 commit，
