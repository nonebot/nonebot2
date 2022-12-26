---
sidebar_position: 4
description: 测试适配器
---

# 测试适配器

通常来说，测试适配器需要测试这三项。

1. 测试连接
2. 测试事件转化
3. 测试 API 调用

## 注册适配器

任何的适配器都需要注册才能起作用。

我们可以使用 Pytest 的 Fixtures，在测试开始前初始化 NoneBot 并**注册适配器**。

我们假设适配器为 `nonebot.adapters.test`。

```python {20,21} title=conftest.py
from pathlib import Path

import pytest
from nonebug import App

# 如果适配器采用 nonebot.adapters monospace 则需要使用此hook方法正确添加路径
@pytest.fixture
def import_hook():
    import nonebot.adapters

    nonebot.adapters.__path__.append(  # type: ignore
        str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
    )

@pytest.fixture
async def init_adapter(app: App, import_hook):
    import nonebot
    from nonebot.adapters.test import Adapter

    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)
```

## 测试连接

任何的适配器的连接方式主要有以下 4 种：

1. 反向 HTTP（WebHook）
2. 反向 WebSocket
3. 正向 HTTP
4. 正向 WebSocket

NoneBug 的 `test_server` 方法可以供我们测试反向连接方式。

`test_server` 的 `get_client` 方法可以获取 HTTP/WebSocket 客户端。

我们假设适配器 HTTP 上报地址为 `/test/http`，反向 WebSocket 地址为 `/test/ws`，上报机器人 ID
使用请求头 `Bot-ID` 来演示如何通过 NoneBug 测试适配器。

```python {8,16,17,19-22,26,34,36-39} title=test_connection.py
from pathlib import Path

import pytest
from nonebug import App

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoints", ["/test/http"]
)
async def test_http(app: App, init_adapter, endpoints: str):
    import nonebot

    async with app.test_server() as ctx:
        client = ctx.get_client()

        body = {"post_type": "test"}
        headers = {"Bot-ID": "test"}

        resp = await client.post(endpoints, json=body, headers=headers)
        assert resp.status_code == 204  # 检测状态码是否正确
        bots = nonebot.get_bots()
        assert "test" in bots  # 检测是否连接成功

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoints", ["/test/ws"]
)
async def test_ws(app: App, init_adapter, endpoints: str):
    import nonebot

    async with app.test_server() as ctx:
        client = ctx.get_client()

        headers = {"Bot-ID": "test"}

        async with client.websocket_connect(endpoints, headers=headers) as ws:
            bots = nonebot.get_bots()
            assert "test" in bots  # 检测是否连接成功
```

## 测试事件转化

事件转化就是将原始数据反序列化为 `Event` 对象的过程。

测试事件转化就是测试反序列化是否按照预期转化为对应 `Event` 类型。

下面将以 `dict_to_event` 作为反序列化方法，`type` 为 `test` 的事件类型为 `TestEvent` 来演示如何测试事件转化。

```python {8,9} title=test_event.py
import pytest
from nonebug import App

@pytest.mark.asyncio
async def test_event(app: App, init_adapter):
    from nonebot.adapters.test import Adapter, TestEvent

    event = Adapter.dict_to_event({"post_type": "test"})  # 反序列化原始数据
    assert isinstance(event, TestEvent)  # 断言类型是否与预期一致
```

## 测试 API 调用

将消息序列化为原始数据并由适配器发送到协议端叫做 API 调用。

测试 API 调用就是调用 API 并验证返回与预期返回是否一致。

```python {16-18,23-32} title=test_call_api.py
import asyncio
from pathlib import Path

import pytest
from nonebug import App

@pytest.mark.asyncio
async def test_ws(app: App, init_adapter):
    import nonebot

    async with app.test_server() as ctx:
        client = ctx.get_client()

        headers = {"Bot-ID": "test"}

        async def call_api():
            bot = nonebot.get_bot("test")
            return await bot.test_api()

        async with client.websocket_connect("/test/ws", headers=headers) as ws:
            task = asyncio.create_task(call_api())

            # received = await ws.receive_text()
            # received = await ws.receive_bytes()
            received = await ws.receive_json()
            assert received == {"action": "test_api"}  # 检测调用是否与预期一致
            response = {"result": "test"}
            # await ws.send_text(...)
            # await ws.send_bytes(...)
            await ws.send_json(response, mode="bytes")
            result = await task
            assert result == response  # 检测返回是否与预期一致
```
