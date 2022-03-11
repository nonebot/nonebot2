---
sidebar_position: 6
description: 协议适配器的功能与使用

options:
  menu:
    weight: 23
    category: guide
---

# 使用适配器

:::tip 提示
如何**安装**协议适配器请参考[安装协议适配器](../start/install-adapter.mdx)。
:::

## 协议适配器的功能

由于 NoneBot2 的跨平台特性，需要支持不同的协议，因此需要对特定的平台协议编写一个转换器。

协议适配器即是充当中间人的转换器，它将驱动器所收到的数据转换为可以被 NoneBot2 处理的事件 Event，并将事件传递给 NoneBot2。

同时，协议适配器还会处理 API 调用，转换为可以被驱动器处理的数据发送出去。

## 注册协议适配器

NoneBot2 在默认情况下并不会加载任何协议适配器，需要自己手动注册。下方是个加载协议适配器的例子：

```python title=bot.py
import nonebot
from your_adapter_package import Adapter

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

nonebot.run()
```

加载步骤如下：

### 导入协议适配器

首先从你需要的协议适配器的包中导入适配器类，通常为 `Adapter`

```python title=bot.py {2}
import nonebot
from your_adapter_package import Adapter

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

nonebot.run()
```

### 获得驱动器实例

加载协议适配器需要通过驱动器来进行，因此，你需要先初始化 NoneBot2，并获得驱动器实例。

```python title=bot.py {4,5}
import nonebot
from your_adapter_package import Adapter

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

nonebot.run()
```

### 注册

获得驱动器实例后，你需要调用 `register_adapter` 方法来注册协议适配器。NoneBot 会通过协议适配器的 `get_name` 方法来获得协议适配器的名字。

:::warning 注意
你可以多次调用来注册多个协议适配器，但不能注册多次相同的协议适配器，发生这种情况时 NoneBot 会给出一个警告并忽略这次注册。
:::

```python title=bot.py {6}
import nonebot
from your_adapter_package import Adapter

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

nonebot.run()
```

:::danger 警告
协议适配器需要在 NoneBot 启动前进行注册，即 `nonebot.run()` 之前，否则会出现未知的错误。
:::

各适配器的具体配置与说明请跳转至 [商店页“适配器”一栏](https://v2.nonebot.dev/store
) 中各适配器的主页或文档进行查看。
