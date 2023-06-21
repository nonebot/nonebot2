---
sidebar_position: 0
description: nonebot.drivers 模块
---

# nonebot.drivers

本模块定义了驱动适配器基类。

各驱动请继承以下基类。

## _abstract class_ `Driver(env, config)` {#Driver}

- **说明:** Driver 基类。

- **参数**

  - `env` ([Env](../config.md#Env)): 包含环境信息的 Env 对象

  - `config` ([Config](../config.md#Config)): 包含配置信息的 Config 对象

### _instance-var_ `env` {#Driver-env}

- **类型:** str

- **说明:** 环境名称

### _instance-var_ `config` {#Driver-config}

- **类型:** [Config](../config.md#Config)

- **说明:** 全局配置对象

### _property_ `bots` {#Driver-bots}

- **类型:** dict[str, [Bot](../adapters/index.md#Bot)]

- **说明:** 获取当前所有已连接的 Bot

### _method_ `register_adapter(adapter, **kwargs)` {#Driver-register_adapter}

- **说明:** 注册一个协议适配器

- **参数**

  - `adapter` (type[[Adapter](../adapters/index.md#Adapter)]): 适配器类

  - `**kwargs`: 其他传递给适配器的参数

- **返回**

  - None

### _abstract property_ `type` {#Driver-type}

- **类型:** str

- **说明:** 驱动类型名称

### _abstract property_ `logger` {#Driver-logger}

- **类型:**

- **说明:** 驱动专属 logger 日志记录器

### _abstract method_ `run(*args, **kwargs)` {#Driver-run}

- **说明:** 启动驱动框架

- **参数**

  - `*args`

  - `**kwargs`

- **返回**

  - untyped

### _abstract method_ `on_startup(func)` {#Driver-on_startup}

- **说明:** 注册一个在驱动器启动时执行的函数

- **参数**

  - `func` (Callable)

- **返回**

  - Callable

### _abstract method_ `on_shutdown(func)` {#Driver-on_shutdown}

- **说明:** 注册一个在驱动器停止时执行的函数

- **参数**

  - `func` (Callable)

- **返回**

  - Callable

### _classmethod_ `on_bot_connect(func)` {#Driver-on_bot_connect}

- **说明**

  装饰一个函数使他在 bot 连接成功时执行。

  钩子函数参数:

  - bot: 当前连接上的 Bot 对象

- **参数**

  - `func` ([T_BotConnectionHook](../typing.md#T_BotConnectionHook))

- **返回**

  - [T_BotConnectionHook](../typing.md#T_BotConnectionHook)

### _classmethod_ `on_bot_disconnect(func)` {#Driver-on_bot_disconnect}

- **说明**

  装饰一个函数使他在 bot 连接断开时执行。

  钩子函数参数:

  - bot: 当前连接上的 Bot 对象

- **参数**

  - `func` ([T_BotDisconnectionHook](../typing.md#T_BotDisconnectionHook))

- **返回**

  - [T_BotDisconnectionHook](../typing.md#T_BotDisconnectionHook)

## _class_ `Cookies(cookies=None)` {#Cookies}

- **参数**

  - `cookies` (CookieTypes)

### _method_ `set(name, value, domain="", path="/")` {#Cookies-set}

- **参数**

  - `name` (str)

  - `value` (str)

  - `domain` (str)

  - `path` (str)

- **返回**

  - None

### _method_ `get(name, default=None, domain=None, path=None)` {#Cookies-get}

- **参数**

  - `name` (str)

  - `default` (str | None)

  - `domain` (str | None)

  - `path` (str | None)

- **返回**

  - str | None

### _method_ `delete(name, domain=None, path=None)` {#Cookies-delete}

- **参数**

  - `name` (str)

  - `domain` (str | None)

  - `path` (str | None)

- **返回**

  - None

### _method_ `clear(domain=None, path=None)` {#Cookies-clear}

- **参数**

  - `domain` (str | None)

  - `path` (str | None)

- **返回**

  - None

### _method_ `update(cookies=None)` {#Cookies-update}

- **参数**

  - `cookies` (CookieTypes)

- **返回**

  - None

### _method_ `as_header(request)` {#Cookies-as_header}

- **参数**

  - `request` (Request)

- **返回**

  - dict[str, str]

## _class_ `Request(method, url, *, params=None, headers=None, cookies=None, content=None, data=None, json=None, files=None, version=HTTPVersion.H11, timeout=None, proxy=None)` {#Request}

- **参数**

  - `method` (str | bytes)

  - `url` (URL | str | RawURL)

  - `params` (QueryTypes)

  - `headers` (HeaderTypes)

  - `cookies` (CookieTypes)

  - `content` (ContentTypes)

  - `data` (DataTypes)

  - `json` (Any)

  - `files` (FilesTypes)

  - `version` (str | HTTPVersion)

  - `timeout` (float | None)

  - `proxy` (str | None)

## _class_ `Response(status_code, *, headers=None, content=None, request=None)` {#Response}

- **参数**

  - `status_code` (int)

  - `headers` (HeaderTypes)

  - `content` (ContentTypes)

  - `request` (Request | None)

## _abstract class_ `WebSocket(*, request)` {#WebSocket}

- **参数**

  - `request` (Request)

### _abstract property_ `closed` {#WebSocket-closed}

- **类型:** bool

- **说明:** 连接是否已经关闭

### _abstract async method_ `accept()` {#WebSocket-accept}

- **说明:** 接受 WebSocket 连接请求

- **参数**

  empty

- **返回**

  - None

### _abstract async method_ `close(code=1000, reason="")` {#WebSocket-close}

- **说明:** 关闭 WebSocket 连接请求

- **参数**

  - `code` (int)

  - `reason` (str)

- **返回**

  - None

### _abstract async method_ `receive()` {#WebSocket-receive}

- **说明:** 接收一条 WebSocket text/bytes 信息

- **参数**

  empty

- **返回**

  - str | bytes

### _abstract async method_ `receive_text()` {#WebSocket-receive_text}

- **说明:** 接收一条 WebSocket text 信息

- **参数**

  empty

- **返回**

  - str

### _abstract async method_ `receive_bytes()` {#WebSocket-receive_bytes}

- **说明:** 接收一条 WebSocket binary 信息

- **参数**

  empty

- **返回**

  - bytes

### _async method_ `send(data)` {#WebSocket-send}

- **说明:** 发送一条 WebSocket text/bytes 信息

- **参数**

  - `data` (str | bytes)

- **返回**

  - None

### _abstract async method_ `send_text(data)` {#WebSocket-send_text}

- **说明:** 发送一条 WebSocket text 信息

- **参数**

  - `data` (str)

- **返回**

  - None

### _abstract async method_ `send_bytes(data)` {#WebSocket-send_bytes}

- **说明:** 发送一条 WebSocket binary 信息

- **参数**

  - `data` (bytes)

- **返回**

  - None

## _enum_ `HTTPVersion` {#HTTPVersion}

- **说明:** An enumeration.

- **参数**

  auto

  - `H10: '1.0'`

  - `H11: '1.1'`

  - `H2: '2'`

## _abstract class_ `ForwardMixin(<auto>)` {#ForwardMixin}

- **说明:** 客户端混入基类。

- **参数**

  auto

### _abstract property_ `type` {#ForwardMixin-type}

- **类型:** str

- **说明:** 客户端驱动类型名称

### _abstract async method_ `request(setup)` {#ForwardMixin-request}

- **说明:** 发送一个 HTTP 请求

- **参数**

  - `setup` ([Request](#Request))

- **返回**

  - [Response](#Response)

### _abstract method_ `websocket(setup)` {#ForwardMixin-websocket}

- **说明:** 发起一个 WebSocket 连接

- **参数**

  - `setup` ([Request](#Request))

- **返回**

  - AsyncGenerator[[WebSocket](#WebSocket), None]

## _abstract class_ `ForwardDriver(env, config)` {#ForwardDriver}

- **说明:** 客户端基类。将客户端框架封装，以满足适配器使用。

- **参数**

  - `env` ([Env](../config.md#Env))

  - `config` ([Config](../config.md#Config))

## _abstract class_ `ReverseDriver(env, config)` {#ReverseDriver}

- **说明:** 服务端基类。将后端框架封装，以满足适配器使用。

- **参数**

  - `env` ([Env](../config.md#Env))

  - `config` ([Config](../config.md#Config))

### _abstract property_ `server_app` {#ReverseDriver-server_app}

- **类型:** Any

- **说明:** 驱动 APP 对象

### _abstract property_ `asgi` {#ReverseDriver-asgi}

- **类型:** Any

- **说明:** 驱动 ASGI 对象

### _abstract method_ `setup_http_server(setup)` {#ReverseDriver-setup_http_server}

- **说明:** 设置一个 HTTP 服务器路由配置

- **参数**

  - `setup` ([HTTPServerSetup](#HTTPServerSetup))

- **返回**

  - None

### _abstract method_ `setup_websocket_server(setup)` {#ReverseDriver-setup_websocket_server}

- **说明:** 设置一个 WebSocket 服务器路由配置

- **参数**

  - `setup` ([WebSocketServerSetup](#WebSocketServerSetup))

- **返回**

  - None

## _def_ `combine_driver(driver, *mixins)` {#combine_driver}

- **说明:** 将一个驱动器和多个混入类合并。

- **参数**

  - `driver` (type[Driver])

  - `*mixins` (type[ForwardMixin])

- **返回**

  - type[Driver]

## _class_ `HTTPServerSetup(<auto>)` {#HTTPServerSetup}

- **说明:** HTTP 服务器路由配置。

- **参数**

  auto

## _class_ `WebSocketServerSetup(<auto>)` {#WebSocketServerSetup}

- **说明:** WebSocket 服务器路由配置。

- **参数**

  auto
