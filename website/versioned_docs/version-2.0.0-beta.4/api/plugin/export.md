---
sidebar_position: 4
description: nonebot.plugin.export 模块
---

# nonebot.plugin.export

本模块定义了插件导出的内容对象。

在新版插件系统中，推荐优先使用直接 import 所需要的插件内容。

## _class_ `Export()` {#Export}

- **说明**

  插件导出内容以使得其他插件可以获得。

- **用法**

  ```python
  nonebot.export().default = "bar"

  @nonebot.export()
  def some_function():
      pass

  # this doesn't work before python 3.9
  # use
  # export = nonebot.export(); @export.sub
  # instead
  # See also PEP-614: https://www.python.org/dev/peps/pep-0614/
  @nonebot.export().sub
  def something_else():
      pass
  ```

## _def_ `export()` {#export}

- **说明**

  获取当前插件的导出内容对象

- **返回**

  - [Export](#Export)
