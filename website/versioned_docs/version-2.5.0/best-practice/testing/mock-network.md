---
sidebar_position: 3
description: 模拟网络通信以进行测试
---

# 模拟网络通信

NoneBot 驱动器提供了多种方法来帮助适配器进行网络通信，主要包括客户端和服务端两种类型。模拟网络通信可以帮助我们更加接近实际机器人应用场景，进行更加真实的集成测试。同时，通过这种途径，我们还可以完成对适配器的测试。

NoneBot 中的网络通信主要包括以下几种：

- HTTP 服务端（WebHook）
- WebSocket 服务端
- HTTP 客户端
- WebSocket 客户端

下面我们将分别介绍如何使用 NoneBug 来模拟这几种通信方式。

## 测试 HTTP 服务端

当 NoneBot 作为 ASGI 服务端应用时，我们可以定义一系列的路由来处理 HTTP 请求，适配器同样也可以通过定义路由来响应机器人相关的网络通信。下面假设我们使用了一个适配器 `fake` ，它定义了一个路由 `/fake/http` ，用于接收平台 WebHook 并处理。实际应用测试时，应将该路由地址替换为**真实适配器注册的路由地址**。

我们首先需要获取测试用模拟客户端：

```python {5,6} title=tests/test_http_server.py
from nonebug import App

@pytest.mark.asyncio
async def test_http_server(app: App):
    async with app.test_server() as ctx:
        client = ctx.get_client()
```

默认情况下，`app.test_server()` 会通过 `nonebot.get_asgi` 获取测试对象，我们也可以通过参数指定 ASGI 应用：

```python
async with app.test_server(asgi=asgi_app) as ctx:
    ...
```

获取到模拟客户端后，即可像 `requests`、`httpx` 等库类似的方法进行使用：

```python {3,11-14,16} title=tests/test_http_server.py
import nonebot
from nonebug import App
from nonebot.adapters.fake import Adapter

@pytest.mark.asyncio
async def test_http_server(app: App):
    adapter = nonebot.get_adapter(Adapter)

    async with app.test_server() as ctx:
        client = ctx.get_client()
        response = await client.post("/fake/http", json={"bot_id": "fake"})
        assert response.status_code == 200
        assert response.json() == {"status": "success"}
        assert "fake" in nonebot.get_bots()

    adapter.bot_disconnect(nonebot.get_bot("fake"))
```

在上面的测试中，我们向 `/fake/http` 发送了一个模拟 POST 请求，适配器将会对该请求进行处理，我们可以通过检查请求返回是否正确、Bot 对象是否创建等途径来验证机器人是否正确运行。在完成测试后，我们通常需要对 Bot 对象进行清理，以避免对其他测试产生影响。

## 测试 WebSocket 服务端

当 NoneBot 作为 ASGI 服务端应用时，我们还可以定义一系列的路由来处理 WebSocket 通信。下面假设我们使用了一个适配器 `fake` ，它定义了一个路由 `/fake/ws` ，用于处理平台 WebSocket 连接信息。实际应用测试时，应将该路由地址替换为**真实适配器注册的路由地址**。

我们同样需要通过 `app.test_server()` 获取测试用模拟客户端，这里就不再赘述。在获取到模拟客户端后，我们可以通过 `client.websocket_connect` 方法来模拟 WebSocket 连接：

```python {3,11-15} title=tests/test_ws_server.py
import nonebot
from nonebug import App
from nonebot.adapters.fake import Adapter

@pytest.mark.asyncio
async def test_ws_server(app: App):
    adapter = nonebot.get_adapter(Adapter)

    async with app.test_server() as ctx:
        client = ctx.get_client()
        async with client.websocket_connect("/fake/ws") as ws:
            await ws.send_json({"bot_id": "fake"})
            response = await ws.receive_json()
            assert response == {"status": "success"}
            assert "fake" in nonebot.get_bots()
```

在上面的测试中，我们向 `/fake/ws` 进行了 WebSocket 模拟通信，通过发送消息与机器人进行交互，然后检查机器人发送的信息是否正确。

## 测试 HTTP 客户端

~~暂不支持~~

## 测试 WebSocket 客户端

~~暂不支持~~
