---
sidebar_position: 0
description: 在商店发布自己的插件
---

# 发布插件

如果已经写好了一个好用的插件想给大家使用，本章节可以帮助您上架你的插件。

:::tip 提示
本章节仅包含插件发布流程指导，插件开发请查阅前述章节。
:::

## 项目结构

:::tip 提示
不同构建工具的使用可能存在差别。本文以 [`setuptools`](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)
构建系统为示例讲解，其余构建/管理工具等的用法请读者自行探索。
:::

### 手动组织项目

一个插件项目的基本组织结构如下：

```tree
📦 nonebot-plugin-{your-plugin-name}
├── 📂 nonebot_plugin_{your_plugin_name}
│   ├── 📜 __init__.py
│   └── 📜 config.py
├── 📜 pyproject.toml
└── 📜 README.md
```

其中：

- `nonebot-plugin-{your-plugin-name}` 为你的项目名；
- `nonebot_plugin_{your_plugin_name}` 为你的插件导入包名（建议项目名使用横杠 `-` 分隔，插件导入名使用下划线 `_` 分隔）；
- `pyproject.toml` 为项目信息文件；
- `README.md` 为项目介绍文件（编写可参考其它插件）。

#### 插件程序结构

插件程序本身结构可参考 [插件结构](../tutorial/create-plugin.md#插件结构)，唯一区别在于，插件包可以直接处于项目顶层。

#### 填写插件元数据

目前版本的插件要求必须填写必要元数据才允许发布。下面是一个示例：

```python
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="{插件名称}",
    description="{插件介绍}",
    usage="{插件用法}",
    type="{插件分类}",  # 发布必填，当前有效值可为 `application`（向聊天用户提供功能） 或 `library`（只向开发者提供功能）。
    homepage="{项目主页}",  # 发布必填。
    config=Config,  # 插件配置项，如无需配置可不填写。
    supported_adapters={"~onebot.v11"},  # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式表记。
    # 若插件可以保证支持当下及未来所有适配器（即仅使用基本适配器功能）可留空，否则应该列出插件支持的适配器。
    extra={},  # 自定义扩充字段，按需填写
)
```

#### 填写项目信息

下面是一个 `pyproject.toml` 的基本的填写示例：

```toml
[project]
name = "nonebot-plugin-{your-plugin-name}"
version = "{插件版本号}"
description = "{插件介绍}"
authors = [
    {name = "{作者名}", email = "{作者邮箱}"},
]
license = {text = "{开源协议}"}  # 可选，与实际项目对应
dependencies = ["nonebot2>=2.0.0"]  # 插件依赖
requires-python = ">=3.8"  # Python 版本限制
readme = "README.md"

[project.urls]
Homepage = "{项目主页（可以为仓库地址）}"
Repository = "{仓库地址}"

[build-system]
requires = ["setuptools", "setuptools-scm"]
build-backend = "setuptools.build_meta"
```

:::tip 提示
“插件依赖”中**必须**存在 `nonebot2`，且若有使用特定的适配器（adapter）也要加入依赖列表。
:::

:::tip 提示
带花括号 `{}` 的内容需要自行替换，注意**一定要把原有的花括号去掉**。
:::

### 使用现成的项目模板

一些社区用户可能会分享自己制作的项目模板方便大家使用。如
[https://github.com/A-kirami/nonebot-plugin-template](https://github.com/A-kirami/nonebot-plugin-template) 就是一个可用的模板。

:::tip 提示
本文档**不保证**第三方模板的适用性。

根据项目模板提供的使用指导补全/修改相应内容后上传到 GitHub 上即可。
:::

## 发布到商店

:::tip 提示
请确保您的插件项目已经托管到 GitHub 等平台的**公开**代码仓库。

请确保您的代码仓地址能够被正确的访问，检查您的插件在代码仓的地址，如 `https://github.com/{您的 GitHub 用户名}/nonebot-plugin-{your-plugin-name}` 。
:::

### 发布到 PyPI

:::tip 提示
本章节重点讲述通过 GitHub Actions 完成发布，其余方式请读者自行探索。
:::

本节提供了一个简单的自动工作流，它可以在开发者给项目创建 Release 时自动构建并发布到 [PyPI](https://pypi.org)。在此之前，您需要拥有一个
PyPI 账号且已经准备好一个可用于上传程序包的 token。

在项目的 `.github/workflows` 下创建一个 `python-publish.yml`（文件名可以不同，便于辨识即可，后缀必须为 `.yml`），文件内容如下：

```yaml
name: Upload Python Package

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip build
      - name: Build package
        run: |
          python -m build --sdist --wheel --outdir dist/ .
      - name: Publish package
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

保存并上传后，您需要找到项目的 `Settings > Security: Secrets and variables > Actions`，进入后点击 `New repository secret` 按钮创建私密数据。
在 Name 一栏输入 `PYPI_API_TOKEN`，在 Secret 一栏输入事先准备好的 token，点击下方 `Add secret` 按钮完成创建。至此，该工作流已经可用。

从项目主页进入 Releases 页面，点击 `Draft a new release` 按钮，在 `Choose a tag` 处输入你的新版本号（推荐用 `v`
开头）并回车（创建一个新标签），然后分别填写标题（一般与标签相同）和描述等信息。确认无误后点击 `Publish release` 发布版本。

:::tip 提示
发布新版本插件前一定要注意同步更新 `pyproject.toml` 中的版本号！
:::

### 提交申请到商店

完成在 PyPI 的插件发布流程后，前往 **[NoneBot2 商店](https://nonebot.dev/store)** 页面，切换到插件页签，点击 **发布插件** 按钮。

在弹出的插件信息提交表单内，填入您所要发布的相应插件信息。

完成填写后，点击 **发布** 按钮，这将自动使用 **[NoneBot2](https://github.com/nonebot/nonebot2)**
代码仓库内的“发布插件”模板填写相应信息（标签会被正确处理）。确认信息无误后点击页面下方的 `Submit new issue` 按钮进行最终提交即可。

### 等待插件发布处理

您的插件发布 Issue 创建后，将会经过 **Noneflow Bot** 的检查，以确保插件信息正确无误、插件能被正确加载。

:::tip 提示
若插件检查未通过或信息有误，**不必**关闭当前 Issue。只需更新插件并上传到 PyPI/修改信息后在当前 Issue 追加任意内容的评论（如“已更新”等）即可重新触发插件检查。
:::

之后，NoneBot2 的维护者和一些插件开发者会初步检查插件代码，帮助减少该插件的问题。

完成这些步骤后，您的插件将会被合并到 **[NoneBot2 商店](https://nonebot.dev/store)**，而您也将成为
**[NoneBot2 贡献者](https://github.com/nonebot/nonebot2/graphs/contributors)** 的一员。

### 成功发布

恭喜，经过上述的发布流程，您的插件已经成功发布到 NoneBot2 商店了。

此时，您可以在 **[NoneBot2 商店](https://nonebot.dev/store)** 的插件页签查找到您的插件。同时，欢迎您成为 **[NoneBot2 贡献者](https://github.com/nonebot/nonebot2/graphs/contributors)**！

**Congratulations!**
