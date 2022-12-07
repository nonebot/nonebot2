---
sidebar_position: 8
description: 调用机器人平台 API，完成更多的功能

options:
  menu:
    weight: 29
    category: guide
---

# 调用平台 API

在使用机器人功能时，除了发送消息以外，还可能需要调用机器人平台的 API 来完成更多的功能。

NoneBot 提供了两种方式来调用机器人平台 API，两种方式都需要首先获得 Bot 实例，然后调用相应的方法。

## 获取 Bot 实例

```python
from nonebot import get_bot

bot = get_bot()  # 获取第一个已连接的 bot 实例
bot = get_bot("bot_id")  # 获取指定 bot_id 的 bot 实例
```

在事件处理依赖中，我们可以使用更为简便的办法来获取 bot 实例，详情可以参考 [获取上下文信息-Bot](https://v2.nonebot.dev/docs/tutorial/plugin/create-handler#bot)

```python
from nonebot.adapters import Bot

async def handle_func(bot: Bot):  # 通过依赖注入获取 bot 实例
    ......
```

## 调用 API

如果需要调用某个机器人平台的 `get_user_info` API，我们可以使用以下任意一种方式：

```python
# 通过 bot 实例上的魔术方法直接使用.操作符调用 API
result = await bot.get_user_info(user_id=12345678)

# 通过 bot 实例上的 call_api 方法调用 API
result = await bot.call_api("get_user_info", user_id=12345678)
```

:::tip 提示
实际可用的 API 由平台提供，请参考平台文档。
:::
