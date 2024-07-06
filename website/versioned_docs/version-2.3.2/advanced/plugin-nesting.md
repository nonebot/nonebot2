---
sidebar_position: 3
description: 编写与加载嵌套插件

options:
  menu:
    - category: advanced
      weight: 40
---

# 嵌套插件

NoneBot 支持嵌套插件，即一个插件可以包含其他插件。通过这种方式，我们可以将一个大型插件拆分成多个功能子插件，使得插件更加清晰、易于维护。我们可以直接在插件中使用 NoneBot 加载插件的方法来加载子插件。

## 创建嵌套插件

我们可以在使用 `nb-cli` 命令[创建插件](../tutorial/create-plugin.md#创建插件)时，选择直接通过模板创建一个嵌套插件：

```bash
$ nb plugin create
[?] 插件名称: parent
[?] 使用嵌套插件? (y/N) Y
[?] 输出目录: awesome_bot/plugins
```

或者使用 `nb plugin create --sub-plugin` 选项直接创建一个嵌套插件。

## 已有插件

如果你已经有一个插件，想要在其中嵌套加载子插件，可以在插件的 `__init__.py` 中添加如下代码：

```python title=parent/__init__.py
import nonebot
from pathlib import Path

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)
```

这样，`parent` 插件就会加载 `parent/plugins` 目录下的所有插件。NoneBot 会正确识别这些插件的父子关系，你可以在 `parent` 的插件信息中看到这些子插件的信息，也可以在子插件信息中看到它们的父插件信息。
