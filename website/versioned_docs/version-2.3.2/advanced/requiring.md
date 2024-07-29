---
sidebar_position: 4
description: 使用其他插件提供的功能

options:
  menu:
    - category: advanced
      weight: 50
---

# 跨插件访问

NoneBot 插件化系统的设计使得插件之间可以功能独立、各司其职，我们可以更好地维护和扩展插件。但是，有时候我们可能需要在不同插件之间调用功能。NoneBot 生态中就有一类插件，它们专为其他插件提供功能支持，如：[定时任务插件](../best-practice/scheduler.md)、[数据存储插件](../best-practice/data-storing.md)等。这时候我们就需要在插件之间进行跨插件访问。

## 插件跟踪

由于 NoneBot 插件系统通过 [Import Hooks](https://docs.python.org/3/reference/import.html#import-hooks) 的方式实现插件加载与跟踪管理，因此我们**不能**在 NoneBot 跟踪插件前进行模块 import，这会导致插件加载失败。即，我们不能在使用 NoneBot 提供的加载插件方法前，直接使用 `import` 语句导入插件。

对于在项目目录下的插件，我们通常直接使用 `load_from_toml` 等方法一次性加载所有插件。由于这些插件已经被声明，即便插件导入顺序不同，NoneBot 也能正确跟踪插件。此时，我们不需要对跨插件访问进行特殊处理。但当我们使用了外部插件，如果没有事先声明或加载插件，NoneBot 并不会将其当作插件进行跟踪，可能会出现意料之外的错误出现。

简单来说，我们必须在 `import` 外部插件之前，确保依赖的外部插件已经被声明或加载。

## 插件依赖声明

NoneBot 提供了一种方法来确保我们依赖的插件已经被正确加载，即使用 `require` 函数。通过 `require` 函数，我们可以在当前插件中声明依赖的插件，NoneBot 会在加载当前插件时，检查依赖的插件是否已经被加载，如果没有，会尝试优先加载依赖的插件。

假设我们有一个插件 `a` 依赖于插件 `b`，我们可以在插件 `a` 中使用 `require` 函数声明其依赖于插件 `b`：

```python {3} title=a/__init__.py
from nonebot import require

require("b")

from b import some_function
```

其中，`require` 函数的参数为插件索引名称或者外部插件的模块名称。在完成依赖声明后，我们可以在插件 `a` 中直接导入插件 `b` 所提供的功能。
