---
sidebar_position: 0
description: nonebot 模块
---

# nonebot

本模块主要定义了 NoneBot 启动所需函数，供 bot 入口文件调用。

## 快捷导入

为方便使用，本模块从子模块导入了部分内容，以下内容可以直接通过本模块导入:

- `on` => [`on`](plugin/on.md#on)
- `on_metaevent` => [`on_metaevent`](plugin/on.md#on-metaevent)
- `on_message` => [`on_message`](plugin/on.md#on-message)
- `on_notice` => [`on_notice`](plugin/on.md#on-notice)
- `on_request` => [`on_request`](plugin/on.md#on-request)
- `on_startswith` => [`on_startswith`](plugin/on.md#on-startswith)
- `on_endswith` => [`on_endswith`](plugin/on.md#on-endswith)
- `on_fullmatch` => [`on_fullmatch`](plugin/on.md#on-fullmatch)
- `on_keyword` => [`on_keyword`](plugin/on.md#on-keyword)
- `on_command` => [`on_command`](plugin/on.md#on-command)
- `on_shell_command` => [`on_shell_command`](plugin/on.md#on-shell-command)
- `on_regex` => [`on_regex`](plugin/on.md#on-regex)
- `on_type` => [`on_type`](plugin/on.md#on-type)
- `CommandGroup` => [`CommandGroup`](plugin/on.md#CommandGroup)
- `Matchergroup` => [`MatcherGroup`](plugin/on.md#MatcherGroup)
- `load_plugin` => [`load_plugin`](plugin/load.md#load-plugin)
- `load_plugins` => [`load_plugins`](plugin/load.md#load-plugins)
- `load_all_plugins` => [`load_all_plugins`](plugin/load.md#load-all-plugins)
- `load_from_json` => [`load_from_json`](plugin/load.md#load-from-json)
- `load_from_toml` => [`load_from_toml`](plugin/load.md#load-from-toml)
- `load_builtin_plugin` =>
  [`load_builtin_plugin`](plugin/load.md#load-builtin-plugin)
- `load_builtin_plugins` =>
  [`load_builtin_plugins`](plugin/load.md#load-builtin-plugins)
- `get_plugin` => [`get_plugin`](plugin/index.md#get-plugin)
- `get_plugin_by_module_name` =>
  [`get_plugin_by_module_name`](plugin/index.md#get-plugin-by-module-name)
- `get_loaded_plugins` =>
  [`get_loaded_plugins`](plugin/index.md#get-loaded-plugins)
- `get_available_plugin_names` =>
  [`get_available_plugin_names`](plugin/index.md#get-available-plugin-names)
- `require` => [`require`](plugin/load.md#require)

## _def_ `get_driver()` {#get-driver}

- **说明**

  获取全局 [Driver](drivers/index.md#Driver) 实例。

  可用于在计划任务的回调等情形中获取当前 [Driver](drivers/index.md#Driver) 实例。

- **参数**

  empty

- **返回**

  - [Driver](drivers/index.md#Driver): 全局 [Driver](drivers/index.md#Driver) 对象

- **异常**

  - ValueError: 全局 [Driver](drivers/index.md#Driver) 对象尚未初始化 ([nonebot.init](#init) 尚未调用)

- **用法**

  ```python
  driver = nonebot.get_driver()
  ```

## _def_ `get_adapter(name)` {#get-adapter}

- **说明:** 获取已注册的 [Adapter](adapters/index.md#Adapter) 实例。

- **重载**

  **1.** `(name) -> Adapter`

  - **参数**

    - `name` (str): 适配器名称

  - **返回**

    - [Adapter](adapters/index.md#Adapter): 指定名称的 [Adapter](adapters/index.md#Adapter) 对象

  **2.** `(name) -> A`

  - **参数**

    - `name` (type[A]): 适配器类型

  - **返回**

    - A: 指定类型的 [Adapter](adapters/index.md#Adapter) 对象

- **异常**

  - ValueError: 指定的 [Adapter](adapters/index.md#Adapter) 未注册

  - ValueError: 全局 [Driver](drivers/index.md#Driver) 对象尚未初始化 ([nonebot.init](#init) 尚未调用)

- **用法**

  ```python
  from nonebot.adapters.console import Adapter
  adapter = nonebot.get_adapter(Adapter)
  ```

## _def_ `get_adapters()` {#get-adapters}

- **说明:** 获取所有已注册的 [Adapter](adapters/index.md#Adapter) 实例。

- **参数**

  empty

- **返回**

  - dict[str, [Adapter](adapters/index.md#Adapter)]: 所有 [Adapter](adapters/index.md#Adapter) 实例字典

- **异常**

  - ValueError: 全局 [Driver](drivers/index.md#Driver) 对象尚未初始化 ([nonebot.init](#init) 尚未调用)

- **用法**

  ```python
  adapters = nonebot.get_adapters()
  ```

## _def_ `get_app()` {#get-app}

- **说明:** 获取全局 [ASGIMixin](drivers/index.md#ASGIMixin) 对应的 Server App 对象。

- **参数**

  empty

- **返回**

  - Any: Server App 对象

- **异常**

  - AssertionError: 全局 Driver 对象不是 [ASGIMixin](drivers/index.md#ASGIMixin) 类型

  - ValueError: 全局 [Driver](drivers/index.md#Driver) 对象尚未初始化 ([nonebot.init](#init) 尚未调用)

- **用法**

  ```python
  app = nonebot.get_app()
  ```

## _def_ `get_asgi()` {#get-asgi}

- **说明:** 获取全局 [ASGIMixin](drivers/index.md#ASGIMixin) 对应的 [ASGI](https://asgi.readthedocs.io/) 对象。

- **参数**

  empty

- **返回**

  - Any: ASGI 对象

- **异常**

  - AssertionError: 全局 Driver 对象不是 [ASGIMixin](drivers/index.md#ASGIMixin) 类型

  - ValueError: 全局 [Driver](drivers/index.md#Driver) 对象尚未初始化 ([nonebot.init](#init) 尚未调用)

- **用法**

  ```python
  asgi = nonebot.get_asgi()
  ```

## _def_ `get_bot(self_id=None)` {#get-bot}

- **说明**

  获取一个连接到 NoneBot 的 [Bot](adapters/index.md#Bot) 对象。

  当提供 `self_id` 时，此函数是 `get_bots()[self_id]` 的简写；
  当不提供时，返回一个 [Bot](adapters/index.md#Bot)。

- **参数**

  - `self_id` (str | None): 用来识别 [Bot](adapters/index.md#Bot) 的 [Bot.self_id](adapters/index.md#Bot-self-id) 属性

- **返回**

  - [Bot](adapters/index.md#Bot): [Bot](adapters/index.md#Bot) 对象

- **异常**

  - KeyError: 对应 self_id 的 Bot 不存在

  - ValueError: 没有传入 self_id 且没有 Bot 可用

  - ValueError: 全局 [Driver](drivers/index.md#Driver) 对象尚未初始化 ([nonebot.init](#init) 尚未调用)

- **用法**

  ```python
  assert nonebot.get_bot("12345") == nonebot.get_bots()["12345"]

  another_unspecified_bot = nonebot.get_bot()
  ```

## _def_ `get_bots()` {#get-bots}

- **说明:** 获取所有连接到 NoneBot 的 [Bot](adapters/index.md#Bot) 对象。

- **参数**

  empty

- **返回**

  - dict[str, [Bot](adapters/index.md#Bot)]: 一个以 [Bot.self_id](adapters/index.md#Bot-self-id) 为键

    [Bot](adapters/index.md#Bot) 对象为值的字典

- **异常**

  - ValueError: 全局 [Driver](drivers/index.md#Driver) 对象尚未初始化 ([nonebot.init](#init) 尚未调用)

- **用法**

  ```python
  bots = nonebot.get_bots()
  ```

## _def_ `init(*, _env_file=None, **kwargs)` {#init}

- **说明**

  初始化 NoneBot 以及 全局 [Driver](drivers/index.md#Driver) 对象。

  NoneBot 将会从 .env 文件中读取环境信息，并使用相应的 env 文件配置。

  也可以传入自定义的 `_env_file` 来指定 NoneBot 从该文件读取配置。

- **参数**

  - `_env_file` (DotenvType | None): 配置文件名，默认从 `.env.{env_name}` 中读取配置

  - `**kwargs` (Any): 任意变量，将会存储到 [Driver.config](drivers/index.md#Driver-config) 对象里

- **返回**

  - None

- **用法**

  ```python
  nonebot.init(database=Database(...))
  ```

## _def_ `run(*args, **kwargs)` {#run}

- **说明:** 启动 NoneBot，即运行全局 [Driver](drivers/index.md#Driver) 对象。

- **参数**

  - `*args` (Any): 传入 [Driver.run](drivers/index.md#Driver-run) 的位置参数

  - `**kwargs` (Any): 传入 [Driver.run](drivers/index.md#Driver-run) 的命名参数

- **返回**

  - None

- **用法**

  ```python
  nonebot.run(host="127.0.0.1", port=8080)
  ```
