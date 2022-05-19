# NoneBot2 贡献指南

首先，感谢你愿意为 NoneBot2 贡献自己的一份力量！

本指南旨在引导你更规范地向 NoneBot2 提交贡献，请务必认真阅读。

## 提交 Issue

在提交 Issue 前，我们建议你先查看 [FAQ](https://github.com/nonebot/discussions/discussions/13) 与 [已有的 Issues](https://github.com/nonebot/nonebot2/issues)，以防重复提交。

### 报告问题、故障与漏洞

NoneBot2 仍然是一个不够稳定的开发中项目，如果你在使用过程中发现问题并确信是由 NoneBot2 引起的，欢迎提交 Issue。

### 建议功能

NoneBot2 还未进入正式版，欢迎在 Issue 中提议要加入哪些新功能。

为了让开发者更好地理解你的意图，请认真描述你所需要的特性，可能的话可以提出你认为可行的解决方案。

## Pull Request

NoneBot 使用 [poetry](https://python-poetry.org/) 管理项目依赖，由于 pre-commit 也经其管理，所以在此一并说明。

下面的命令能在已安装 poetry 和 yarn 的情况下帮你快速配置开发环境。

```bash
# 安装 python 依赖
poetry install
# 安装 pre-commit git hook
pre-commit install
# 安装 gitmoji git hook
yarn global add gitmoji-cli
gitmoji -i
```

### 使用 GitHub Codespaces (Dev Container)

使用 GitHub Codespaces 选择 `NoneBot2` 项目，然后选择 `.devcontainer/devcontainer.json` 配置即可。

### Commit 规范

请确保你的每一个 commit 都能清晰地描述其意图，一个 commit 尽量只有一个意图。

NoneBot 的 commit message 格式遵循 [gitmoji](https://gitmoji.dev/) 规范，在创建 commit 时请牢记这一点。

### 撰写文档

NoneBot2 的文档使用 [docusaurus](https://docusaurus.io/)，它有一些 [Markdown 特性](https://docusaurus.io/zh-CN/docs/markdown-features) 可能会帮助到你。

NoneBot2 文档并没有具体的行文风格规范，但我们建议你尽量写得简单易懂。

如果你需要在本地预览修改后的文档，可以使用 yarn 安装文档依赖后启动 dev server，如下所示：

```bash
yarn install
yarn start
```

### 参与开发

NoneBot2 的代码风格遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 与 [PEP 484](https://www.python.org/dev/peps/pep-0484/) 规范，请确保你的代码风格和项目已有的代码保持一致，变量命名清晰，有适当的注释与测试代码。

## 为社区做贡献

你可以在 NoneBot 商店上架自己的适配器、插件、机器人，具体步骤可参考 [发布插件](https://v2.nonebot.dev/docs/advanced/publish-plugin) 一节。

我们仅对插件的兼容性进行简单测试，并会在下一个版本发布前对与该版本不兼容的插件作出处理。

虽然对插件的内容没有严格限制，但我们还是建议在上架插件之前先查看商店有无功能一致的插件。如果你想要上架商店的插件功能与现有插件不完全重合，请在插件说明中补充其与现有插件的区别。

同时，如果你参考或基于他人发行的代码进行开发，请注意遵守各代码所使用的开源许可协议。

## Git 工作流

`master` 分支为 NoneBot 的开发分支，请在任何情况下都不要直接修改 `master` 分支，而是创建一个目标分支为 `nonebot:master` 的 Pull Request 来提交修改。

如果你不是 NoneBot 团队的成员，可在 fork 本仓库后，向本仓库的 `master` 分支发起 Pull Request，注意遵循先前提到的 commit message 规范创建 commit。我们将在 code review 通过后通过 squash merge 方式将您的贡献合并到主分支。
