---
sidebar_position: 6
description: 调用机器人平台 API，完成更多的功能

options:
  menu:
    weight: 29
    category: guide
---

# 调用平台 API

在使用机器人功能时，除了发送消息以外，还可能需要调用机器人平台的 API 来完成更多的功能。

NoneBot 提供了两种方式来调用机器人平台 API，两种方式都需要首先获得 Bot 实例，然后调用相应的方法。

例如，如果需要调用机器人平台的 `get_user_info` API，可以这样做：

```python
from nonebot import get_bot

bot = get_bot("bot_id")
result = await bot.get_user_info(user_id=12345678)
await bot.call_api("get_user_info", user_id=12345678)
```

:::tip 提示
API 由平台提供，请参考平台文档。
:::
