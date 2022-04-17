---
sidebar_position: 5
description: 测试适配器

options:
menu:
weight: 54
category: advanced
---

# 测试适配器

通常来说，测试适配器需要测试这三项。

1. 测试连接
2. 测试事件转化
3. 测试 API 调用

接下来，我们将假设适配器名称为 `hello_world`，HTTP POST 地址为 `/hello_world/http`，反向 WebSocket 地址为 `/hello_world/ws`，上报机器人 ID
使用请求头 `Bot-ID` 来演示如何通过 NoneBug 测试框架测试适配器。

## 注册适配器

任何的适配器都需要注册才能起作用。

我们可以使用 Pytest 的夹具，在测试开始前初始化 NoneBot 并注册适配器。

```python title=conftest.py {20} {23}
from pathlib import Path

import pytest
from nonebug import App


@pytest.fixture
def import_hook():
    import nonebot.adapters

    # 由于这时包 `nonebot.adapters` 并不存在包 `hello_world`，这里通过 `__path__.append` 将包路径添加到包内
    nonebot.adapters.__path__.append(  # type: ignore
        str((Path(__file__).parent.parent / "nonebot" / "hello_world").resolve())
    )


@pytest.fixture
async def init_adapter(app: App, import_hook):
    import nonebot
    from nonebot.adapters.hello_world import Adapter

    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)
```

## 测试连接

任何的适配器的连接方式均为以下几种：

1. HTTP POST
2. 正向 WebSocket
3. 反向 WebSocket

NoneBug 的 `test_server` 方法可以供我们测试这 3 种连接方式。

`test_server` 的 `get_client` 方法可以获取 HTTP POST 客户端和 WebSocket 客户端。

下面是一个 HTTP POST 和反向 WebSocket 的测试的示例。

```python title=test_connection.py {14-23} {33-38}
from pathlib import Path

import pytest
from nonebug import App


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoints", ["/hello_world/http"]
)
async def test_http(app: App, init_adapter, endpoints: str):
    import nonebot

    async with app.test_server() as ctx:
        client = ctx.get_client()
        event = {
          "post_type": "test"
        }
        headers = {"Bot-ID": "test"}
        resp = await client.post(endpoints, json=event, headers=headers)  # 上报事件，请求头包含 `self-id`
        assert resp.status_code == 204  # 检测状态码是否正确
        bots = nonebot.get_bots()
        assert "test" in bots  # 检测是否连接成功


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoints", ["/hello_world/ws"]
)
async def test_ws(app: App, init_adapter, endpoints: str):
    import nonebot

    async with app.test_server() as ctx:
        client = ctx.get_client()
        headers = {"Bot-ID": "test"}
        async with client.websocket_connect(endpoints, headers=headers) as ws:  # 连接 WebSocket 服务器，请求头包含 `self-id`
            bots = nonebot.get_bots()
            assert "test" in bots  # 检测是否连接成功
```

## 测试事件转化

事件转化就是将原始数据反序列化为 `Event` 的过程。

测试事件转化就是测试反序列化是否按照预期输出。

需要调用适配器的相关实现。

下面将以 `json_to_event` 作为反序列化方法，`type=test` 的事件为 `TestEvent` 来演示如何测试事件转化。

```python {13-14}
import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_event(app: App, init_adapter):
    from nonebot.adapters.hello_world import Adapter

    model_name = "TestEvent"
    event = Adapter.json_to_event({
      "post_type": "test"
    })  # 反序列化原始数据
    assert model_name == event.__class__.__name__  # 检测类型是否与预期一致
    assert event.post_type == "test"  # 测试属性是否一致
```

## 测试 API 调用

将消息序列化为原始文本并由适配器发送到协议端叫做 API 调用。

测试 API 调用就是调用 API 并验证返回与预期返回是否一致。

需要调用适配器的相关实现。

下面我们将以 `ResultStore` 类为序列化类，通过其中的 `fetch` 方法发送请求，并预期返回 `{"test":True}` 的字典来演示如何测试 API 调用。

```python title=test_call_api.py {13-14}
import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_api_reply(app: App, init_adapter):
    from nonebot.adapters.hello_world import ResultStore

    seq = ResultStore()
    self_id = "test"
    response_data = {"test": True}

    resp = await seq.fetch(self_id, seq, response_data, 10.0)  # 序列化消息并发送
    assert resp == response_data  # 测试预期返回内容
```
