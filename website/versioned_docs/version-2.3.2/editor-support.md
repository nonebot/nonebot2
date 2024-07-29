---
sidebar_position: 2
description: 配置编辑器以获得最佳体验
---

# 编辑器支持

框架基于 [PEP484](https://www.python.org/dev/peps/pep-0484/)、[PEP 561](https://www.python.org/dev/peps/pep-0561/)、[PEP8](https://www.python.org/dev/peps/pep-0008/) 等规范进行开发并且**拥有完整类型注解**。框架使用 Pyright（Pylance）工具进行类型检查，确保代码可以被编辑器正确解析。

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
