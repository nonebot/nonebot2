---
sidebar_position: 10
description: 自定义事件响应器存储

options:
  menu:
    - category: advanced
      weight: 110
---

# 事件响应器存储

事件响应器是 NoneBot 处理事件的核心，它们默认存储在一个字典中。在进入会话状态后，事件响应器将会转为临时响应器，作为最高优先级同样存储于该字典中。因此，事件响应器的存储类似于会话存储，它决定了整个 NoneBot 对事件的处理行为。

NoneBot 默认使用 Python 的字典将事件响应器存储于内存中，但是我们也可以自定义事件响应器存储，将事件响应器存储于其他地方，例如 Redis 等。这样我们就可以实现持久化、在多实例间共享会话状态等功能。

## 编写存储提供者

事件响应器的存储提供者 `MatcherProvider` 抽象类继承自 `MutableMapping[int, list[type[Matcher]]]`，即以优先级为键，以事件响应器列表为值的映射。我们可以方便地进行逐优先级事件传播。

编写一个自定义的存储提供者，只需要继承并实现 `MatcherProvider` 抽象类：

```python
from nonebot.matcher import MatcherProvider

class CustomProvider(MatcherProvider):
    ...
```

## 设置存储提供者

我们可以通过 `matchers.set_provider` 方法设置存储提供者：

```python {3}
from nonebot.matcher import matchers

matchers.set_provider(CustomProvider)

assert isinstance(matchers.provider, CustomProvider)
```
