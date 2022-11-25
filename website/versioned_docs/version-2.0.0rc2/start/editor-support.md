---
sidebar_position: 80
description: 编辑器支持
---

# 编辑器支持

框架基于 [PEP484](https://www.python.org/dev/peps/pep-0484/)、[PEP 561](https://www.python.org/dev/peps/pep-0517/)、[PEP8](https://www.python.org/dev/peps/pep-0008/) 等规范进行开发并且是 **Fully Typed**。框架使用 `pyright`（`pylance`）工具进行类型检查，确保代码可以被编辑器正确解析。

## 编辑器推荐配置

### Visual Studio Code

在 Visual Studio Code 中，可以使用 `pylance` Language Server 并启用 `Type Checking` 以达到最佳开发体验。

向 `.vscode` 文件夹中对应文件添加以下配置并在 VSCode 插件面板安装推荐插件：

```json title=extensions.json
{
  "recommendations": ["ms-python.python", "ms-python.vscode-pylance"]
}
```

```json title=settings.json
{
  "python.languageServer": "Pylance",
  "python.analysis.typeCheckingMode": "basic"
}
```

### 其他

欢迎提交 Pull Request 添加其他编辑器配置推荐。点击左下角 `Edit this page` 前往编辑。
