# NoneBot2 贡献指南

首先，感谢你愿意为 NoneBot2 贡献自己的一份力量！

本指南旨在引导你更规范地向 NoneBot2 提交贡献，请务必认真阅读。

## 提交 Issue

在提交 Issue 前，我们建议你先查看 [FAQ](https://github.com/nonebot/discussions/discussions/13) 与 [已有的 Issues](https://github.com/nonebot/nonebot2/issues)，以防重复提交。

### 报告问题、故障与漏洞

如果你在使用过程中发现问题并确信是由 NoneBot2 引起的，欢迎提交 Issue。

### 建议功能

为了让开发者更好地理解你的意图，请认真描述你所需要的特性，可能的话可以提出你认为可行的解决方案。

## Pull Request

NoneBot 使用 [poetry](https://python-poetry.org/) 管理项目依赖，由于 pre-commit 也经其管理，所以在此一并说明。

下面的命令能在已安装 poetry 和 yarn 的情况下帮你快速配置开发环境。

```bash
# 安装 python 依赖
poetry install
# 安装 pre-commit git hook
pre-commit install
```

### 使用 GitHub Codespaces（Dev Container）

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=master&repo=289605524)

### Commit 规范

请确保你的每一个 commit 都能清晰地描述其意图，一个 commit 尽量只有一个意图。

NoneBot 的 commit message 格式遵循 [gitmoji](https://gitmoji.dev/) 规范，在创建 commit 时请牢记这一点。

或者使用 [nonemoji](https://github.com/nonebot/nonemoji) 代替 git 进行 commit，nonemoji 已默认作为项目开发依赖安装。

```bash
nonemoji commit [-e EMOJI] [-m MESSAGE] [-- ...]
```

### 工作流概述

`master` 分支为 NoneBot 的开发分支，在任何情况下都请不要直接修改 `master` 分支，而是创建一个目标分支为 `nonebot:master` 的 Pull Request 来提交修改。Pull Request 标题请尽量更改成中文，以便自动生成更新日志。

如果你不是 NoneBot 团队的成员，可在 fork 本仓库后，向本仓库的 `master` 分支发起 Pull Request，注意遵循先前提到的 commit message 规范创建 commit。我们将在 code review 通过后通过 squash merge 方式将您的贡献合并到主分支。

### 撰写文档

NoneBot2 的文档使用 [docusaurus](https://docusaurus.io/)，它有一些 [Markdown 特性](https://docusaurus.io/zh-CN/docs/markdown-features) 可能会帮助到你。

如果你需要在本地预览修改后的文档，可以使用 yarn 安装文档依赖后启动 dev server，如下所示：

```bash
yarn install
yarn start
```

NoneBot2 文档并没有具体的行文风格规范，但我们建议你尽量写得简单易懂。

以下是比较重要的编写与排版规范。目前 NoneBot2 文档中仍有部分文档不完全遵守此规范，如果在阅读时发现欢迎提交 PR。

1. 中文与英文、数字、半角符号之间需要有空格。例：`NoneBot2 是一个可扩展的 Python 异步机器人框架。`
2. 若非英文整句，使用全角标点符号。例：`现在你可以看到机器人回复你：“Hello, World !”。`
3. 直引号`「」`和弯引号`“”`都可接受，但同一份文件里应使用同种引号。
4. **不要使用斜体**，你不需要一种与粗体不同的强调。除此之外，你也可以考虑使用 docusaurus 提供的[告示](https://docusaurus.io/zh-CN/docs/markdown-features/admonitions)功能。
5. 文档中应以“我们”指代机器人开发者，以“机器人用户”指代机器人的使用者。

以上由[社区创始人 richardchien 的中文排版规范](https://stdrc.cc/style-guides/chinese)补充修改得到。

如果你需要编辑器检查 Markdown 规范，可以在 VSCode 中安装 markdownlint 扩展。

### 参与开发

NoneBot2 的代码风格遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 与 [PEP 484](https://www.python.org/dev/peps/pep-0484/) 规范，请确保你的代码风格和项目已有的代码保持一致，变量命名清晰，有适当的注释与测试代码。

## 为社区做贡献

你可以在 NoneBot 商店上架自己的适配器、插件、机器人，具体步骤可参考 [发布插件](https://nonebot.dev/docs/developer/plugin-publishing) 一节。

我们仅对插件的兼容性进行简单测试，并会在下一个版本发布前对与该版本不兼容的插件作出处理。

虽然对插件的内容没有严格限制，但我们还是建议在上架插件之前先查看商店有无功能一致的插件。如果你想要上架商店的插件功能与现有插件不完全重合，请在插件说明中补充其与现有插件的区别。

同时，如果你参考或基于他人发行的代码进行开发，请注意遵守各代码所使用的开源许可协议。
