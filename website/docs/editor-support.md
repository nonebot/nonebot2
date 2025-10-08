---
sidebar_position: 2
description: 配置编辑器以获得最佳体验
---

# 编辑器支持

框架基于 [PEP 484](https://www.python.org/dev/peps/pep-0484/)、[PEP 561](https://www.python.org/dev/peps/pep-0561/)、[PEP 8](https://www.python.org/dev/peps/pep-0008/) 等规范进行开发并且**拥有完整类型注解**。框架使用 Pyright（Pylance）工具进行类型检查，确保代码可以被编辑器正确解析。

## CLI 脚手架提供的编辑器工具支持

在使用 NB-CLI [创建项目](./quick-start.mdx#创建项目)时，如果选择了用于插件开发的 `simple` 模板，其会根据选择的开发工具，**自动配置项目根目录下的 `.vscode/extensions.json` 文件**，以推荐最匹配的 VS Code 插件，同时自动将相应的预设配置项写入 `pyproject.toml` 作为“开箱即用”配置，从而提升开发体验。

```bash
[?] 选择一个要使用的模板: simple (插件开发者)
...
[?] 要使用哪些开发工具?
```

### 支持的开发工具

1. Pyright (Pylance)

   [VS Code 插件](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) | [项目](https://github.com/microsoft/pyright) | [文档](https://microsoft.github.io/pyright/)

   由微软开发的 Python 静态类型检查器和语言服务器，提供智能感知、跳转定义、查找引用、实时错误检查等强大功能。

   作为 VS Code 官方推荐的 Python 语言服务器，与 Pylance 扩展配合使用，能提供最流畅、最准确的代码补全和类型推断体验，是绝大多数开发者的首选。

2. Ruff

   [VS Code 插件](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) | [项目](https://github.com/astral-sh/ruff) | [文档](https://docs.astral.sh/ruff/)

   一个用 Rust 编写的超快 Python 代码格式化和 lint 工具，完全兼容 `black`、`isort`、`flake8` 等主流工具的规则。

   速度极快（比 `black` 和 `flake8` 快 100 倍以上），配置简单，能自动格式化代码并检测潜在错误、代码风格问题（尤其是误用同步网络请求库），是提升代码质量和开发效率的必备利器。

3. MyPy

   [VS Code 插件](https://marketplace.visualstudio.com/items?itemName=matangover.mypy) | [项目](https://github.com/python/mypy) | [文档](https://mypy.readthedocs.io/en/stable/index.html)

   一个官方实现的 Python 静态类型检查器，通过分析代码中的类型注解来发现类型错误。

4. BasedPyright

   [VS Code 插件](https://marketplace.visualstudio.com/items?itemName=detachhead.basedpyright) | [项目](https://github.com/DetachHead/basedpyright) | [文档](https://docs.basedpyright.com/)

   一个基于 Pyright 的、由社区维护的替代性 Python 语言服务器，旨在提供更优的类型检查支持与接近 Pylance 的更好的使用体验。

   相较于 Pylance，BasedPyright 允许配合 VS Code 之外的其他编辑器使用，同时也复刻了部分 Pylance 限定的功能。

   如果您是高级用户，希望尝试 Pylance 的替代方案，或遇到 Pylance 在特定环境下的兼容性问题，可以考虑使用 BasedPyright。

:::caution 提示
为避免 `Pylance` 和 `BasedPyright` 相互冲突导致配置混乱甚至异常，脚手架默认不允许在创建项目时同时配置这两者。

如果确实需要同时使用，请在创建项目时选择 Pylance/Pyright 并根据[相关文档](https://docs.basedpyright.com/latest/installation/ides/#vscode-vscodium)进行手动配置。
:::

### 配置效果

选择上述工具后，NB-CLI 会在您的项目根目录下生成一个 `.vscode/extensions.json` 文件并在 `pyproject.toml` 文件中写入相应的配置项。当您在 VS Code 中打开此项目时，IDE
会自动弹出提示，建议您安装这些推荐的扩展，一键即可完成开发环境的初始化，让您可以立即开始编写代码，无需手动搜索和安装插件。

## 编辑器推荐配置

### Visual Studio Code

在 Visual Studio Code 中，可以使用 Pylance Language Server 并启用 `Type Checking` 配置以达到最佳开发体验。

1. 在 VSCode 插件视图搜索并安装 `Python (ms-python.python)` 和 `Pylance (ms-python.vscode-pylance)` 插件。
2. 修改 VSCode 配置
   在 VSCode 设置视图搜索配置项 `Python: Language Server` 并将其值设置为 `Pylance`，搜索配置项 `Python > Analysis: Type Checking Mode` 并将其值设置为 `basic`。

   或者向项目 `.vscode` 文件夹中配置文件添加以下内容：

   ```json title=settings.json
   {
     "python.languageServer": "Pylance",
     "python.analysis.typeCheckingMode": "basic"
   }
   ```

### 其他

欢迎提交 Pull Request 添加其他编辑器配置推荐。点击左下角 `Edit this page` 前往编辑。
