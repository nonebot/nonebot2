---
sidebar_position: 0
description: 选择合适的驱动器运行机器人

options:
  menu:
    - category: advanced
      weight: 10
---

# 选择驱动器

驱动器 (Driver) 是机器人运行的基石，它是机器人初始化的第一步，主要负责数据收发。

:::important 提示
驱动器的选择通常与机器人所使用的协议适配器相关，如果不知道该选择哪个驱动器，可以先阅读相关协议适配器文档说明。
:::

:::tip 提示
如何**安装**驱动器请参考[安装驱动器](../tutorial/store.mdx#安装驱动器)。
:::

## 驱动器类型

驱动器类型大体上可以分为两种：

- `Forward`：即客户端型驱动器，多用于使用 HTTP 轮询，连接 WebSocket 服务器等情形。
- `Reverse`：即服务端型驱动器，多用于使用 WebHook，接收 WebSocket 客户端连接等情形。

客户端型驱动器可以分为以下两种：

1. 异步发送 HTTP 请求，自定义 `HTTP Method`、`URL`、`Header`、`Body`、`Cookie`、`Proxy`、`Timeout` 等。
2. 异步建立 WebSocket 连接上下文，自定义 `WebSocket URL`、`Header`、`Cookie`、`Proxy`、`Timeout` 等。

服务端型驱动器目前有：

1. ASGI 应用框架，具有以下功能：
   - 协议适配器自定义 HTTP 上报地址以及对上报数据处理的回调函数。
   - 协议适配器自定义 WebSocket 连接请求地址以及对 WebSocket 请求处理的回调函数。
   - 用户可以向 ASGI 应用添加任何服务端相关功能，如：[添加自定义路由](./routing.md)。

## 配置驱动器

驱动器的配置方法已经在[配置](../appendices/config.mdx)章节中简单进行了介绍，这里将详细介绍驱动器配置的格式。

NoneBot 中的客户端和服务端型驱动器可以相互配合使用，但服务端型驱动器**仅能选择一个**。所有驱动器模块都会包含一个 `Driver` 子类，即驱动器类，他可以作为驱动器单独运行。同时，客户端驱动器模块中还会提供一个 `Mixin` 子类，用于在与其他驱动器配合使用时加载。因此，驱动器配置格式采用特殊语法：`<module>[:<Driver>][+<module>[:<Mixin>]]*`。

其中，`<module>` 代表**驱动器模块路径**；`<Driver>` 代表**驱动器类名**，默认为 `Driver`；`<Mixin>` 代表**驱动器混入类名**，默认为 `Mixin`。即，我们需要选择一个主要驱动器，然后在其基础上配合使用其他驱动器的功能。主要驱动器可以为客户端或服务端类型，但混入类驱动器只能为客户端类型。

特别的，为了简化内置驱动器模块路径，我们可以使用 `~` 符号作为内置驱动器模块路径的前缀，如 `~fastapi` 代表使用内置驱动器 `fastapi`。NoneBot 内置了多个驱动器适配，但需要安装额外依赖才能使用，具体请参考[安装驱动器](../tutorial/store.mdx#安装驱动器)。常见的驱动器配置如下：

```dotenv
DRIVER=~fastapi
DRIVER=~aiohttp
DRIVER=~httpx+~websockets
DRIVER=~fastapi+~httpx+~websockets
```

## 获取驱动器

在 NoneBot 框架初始化完成后，我们就可以通过 `get_driver()` 方法获取全局驱动器实例：

```python
from nonebot import get_driver

driver = get_driver()
```

## 内置驱动器

### None

**类型：**服务端驱动器

NoneBot 内置的空驱动器，不提供任何收发数据功能，可以在不需要外部网络连接时使用。

```env
DRIVER=~none
```

### FastAPI（默认）

**类型：**ASGI 服务端驱动器

> FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

[FastAPI](https://fastapi.tiangolo.com/) 是一个易上手、高性能的异步 Web 框架，具有极佳的编写体验。 FastAPI 可以通过类型注解、依赖注入等方式实现输入参数校验、自动生成 API 文档等功能，也可以挂载其他 ASGI、WSGI 应用。

```env
DRIVER=~fastapi
```

#### FastAPI 配置项

##### `fastapi_openapi_url`

类型：`str | None`  
默认值：`None`  
说明：`FastAPI` 提供的 `OpenAPI` JSON 定义地址，如果为 `None`，则不提供 `OpenAPI` JSON 定义。

##### `fastapi_docs_url`

类型：`str | None`  
默认值：`None`  
说明：`FastAPI` 提供的 `Swagger` 文档地址，如果为 `None`，则不提供 `Swagger` 文档。

##### `fastapi_redoc_url`

类型：`str | None`  
默认值：`None`  
说明：`FastAPI` 提供的 `ReDoc` 文档地址，如果为 `None`，则不提供 `ReDoc` 文档。

##### `fastapi_include_adapter_schema`

类型：`bool`  
默认值：`True`  
说明：`FastAPI` 提供的 `OpenAPI` JSON 定义中是否包含适配器路由的 `Schema`。

##### `fastapi_reload`

:::caution 警告
不推荐开启该配置项，在 Windows 平台上开启该功能有可能会造成预料之外的影响！替代方案：使用 `nb-cli` 命令行工具以及参数 `--reload` 启动 NoneBot。

```bash
nb run --reload
```

开启该功能后，在 uvicorn 运行时（FastAPI 提供的 ASGI 底层，即 reload 功能的实际来源），asyncio 使用的事件循环会被 uvicorn 从默认的 `ProactorEventLoop` 强制切换到 `SelectorEventLoop`。

> 相关信息参考 [uvicorn#529](https://github.com/encode/uvicorn/issues/529)，[uvicorn#1070](https://github.com/encode/uvicorn/pull/1070)，[uvicorn#1257](https://github.com/encode/uvicorn/pull/1257)

后者（`SelectorEventLoop`）在 Windows 平台的可使用性不如前者（`ProactorEventLoop`），包括但不限于

1. 不支持创建子进程
2. 最多只支持 512 个套接字
3. ...

> 具体信息参考 [Python 文档](https://docs.python.org/zh-cn/3/library/asyncio-platforms.html#windows)

所以，一些使用了 asyncio 的库因此可能无法正常工作，如：

1. [playwright](https://playwright.dev/python/docs/library#incompatible-with-selectoreventloop-of-asyncio-on-windows)

如果在开启该功能后，原本**正常运行**的代码报错，且打印的异常堆栈信息和 asyncio 有关（异常一般为 `NotImplementedError`），
你可能就需要考虑相关库对事件循环的支持，以及是否启用该功能。
:::

类型：`bool`  
默认值：`False`  
说明：是否开启 `uvicorn` 的 `reload` 功能，需要在机器人入口文件提供 ASGI 应用路径。

```python title=bot.py
app = nonebot.get_asgi()
nonebot.run(app="bot:app")
```

##### `fastapi_reload_dirs`

类型：`List[str] | None`  
默认值：`None`  
说明：重载监控文件夹列表，默认为 uvicorn 默认值

##### `fastapi_reload_delay`

类型：`float | None`  
默认值：`None`  
说明：重载延迟，默认为 uvicorn 默认值

##### `fastapi_reload_includes`

类型：`List[str] | None`  
默认值：`None`  
说明：要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

##### `fastapi_reload_excludes`

类型：`List[str] | None`  
默认值：`None`  
说明：不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

##### `fastapi_extra`

类型：`Dist[str, Any]`  
默认值：`{}`  
说明：传递给 `FastAPI` 的其他参数

### Quart

**类型：**ASGI 服务端驱动器

> Quart is an asyncio reimplementation of the popular Flask microframework API.

[Quart](https://quart.palletsprojects.com/) 是一个类 Flask 的异步版本，拥有与 Flask 非常相似的接口和使用方法。

```env
DRIVER=~quart
```

#### Quart 配置项

##### `quart_reload`

:::caution 警告
不推荐开启该配置项，在 Windows 平台上开启该功能有可能会造成预料之外的影响！替代方案：使用 `nb-cli` 命令行工具以及参数 `--reload` 启动 NoneBot。

```bash
nb run --reload
```

:::

类型：`bool`  
默认值：`False`  
说明：是否开启 `uvicorn` 的 `reload` 功能，需要在机器人入口文件提供 ASGI 应用路径。

```python title=bot.py
app = nonebot.get_asgi()
nonebot.run(app="bot:app")
```

##### `quart_reload_dirs`

类型：`List[str] | None`  
默认值：`None`  
说明：重载监控文件夹列表，默认为 uvicorn 默认值

##### `quart_reload_delay`

类型：`float | None`  
默认值：`None`  
说明：重载延迟，默认为 uvicorn 默认值

##### `quart_reload_includes`

类型：`List[str] | None`  
默认值：`None`  
说明：要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

##### `quart_reload_excludes`

类型：`List[str] | None`  
默认值：`None`  
说明：不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值

##### `quart_extra`

类型：`Dist[str, Any]`  
默认值：`{}`  
说明：传递给 `Quart` 的其他参数

### HTTPX

**类型：**HTTP 客户端驱动器

:::caution 注意
本驱动器仅支持 HTTP 请求，不支持 WebSocket 连接请求。
:::

> [HTTPX](https://www.python-httpx.org/) is a fully featured HTTP client for Python 3, which provides sync and async APIs, and support for both HTTP/1.1 and HTTP/2.

```env
DRIVER=~httpx
```

### websockets

**类型：**WebSocket 客户端驱动器

:::caution 注意
本驱动器仅支持 WebSocket 连接请求，不支持 HTTP 请求。
:::

> [websockets](https://websockets.readthedocs.io/) is a library for building WebSocket servers and clients in Python with a focus on correctness, simplicity, robustness, and performance.

```env
DRIVER=~websockets
```

### AIOHTTP

**类型：**HTTP/WebSocket 客户端驱动器

> [AIOHTTP](https://docs.aiohttp.org/): Asynchronous HTTP Client/Server for asyncio and Python.

```env
DRIVER=~aiohttp
```
