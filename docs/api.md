---
sidebar: auto
---

# API

## 类型

下面的 API 文档中，「类型」部分使用 Python 的 Type Hint 语法，见 [PEP 484](https://www.python.org/dev/peps/pep-0484/)、[PEP 526](https://www.python.org/dev/peps/pep-0526/) 和 [typing](https://docs.python.org/3/library/typing.html)。

除了 Python 内置的类型，下面还出现了如下 NoneBot 自定类型，实际上它们是 Python 内置类型的别名。

### `Expression_T`

Expression 对象的类型，等价于 `Union[str, Sequence[str], Callable]`。

## 配置

### `API_ROOT`

- **类型:** `str`

- **默认值:** `''`

- **说明:**

  酷 Q HTTP API 插件的 HTTP 接口地址，如果不使用 HTTP 通信，则无需设置。

- **用法:**

  ```python
  API_ROOT = 'http://127.0.0.1:5700'
  ```

  告诉 NoneBot 酷 Q HTTP API 插件的 HTTP 服务运行在 `http://127.0.0.1:5700`。

### `ACCESS_TOKEN`

- **类型:** `str`

- **默认值:** `''`

- **说明:**

  需要和酷 Q HTTP API 插件的配置中的 `access_token` 相同。

### `SECRET`

- **类型:** `str`

- **默认值:** `''`

- **说明:**

  需要和酷 Q HTTP API 插件的配置中的 `secret` 相同。

### `HOST`

- **类型:** `str`

- **默认值:** `'127.0.0.1'`

- **说明:**

  NoneBot 的 HTTP 和 WebSocket 服务端监听的 IP／主机名。

- **用法:**

  ```python
  HOST = '0.0.0.0'
  ```

  监听服务器的所有 IP。

### `PORT`

- **类型:** `int`

- **默认值:** `8080`

- **说明:**

  NoneBot 的 HTTP 和 WebSocket 服务端监听的端口。

- **用法:**

  ```python
  PORT = 9876
  ```

  监听 9876 端口。

### `DEBUG`

- **类型:** `bool`

- **默认值:** `True`

- **说明:**

  是否以调试模式运行，生产环境需要设置为 `False` 以提高性能。

- **用法:**

  ```python
  DEBUG = False
  ```

  不使用调试模式运行。

### `SUPERUSERS`

- **类型:** `Container[int]`

- **默认值:** `set()`

- **说明:**

  超级用户的 QQ 号，用于命令的权限检查。

- **用法:**

  ```python
  SUPERUSERS = {12345678, 87654321}
  ```

  设置 `12345678` 和 `87654321` 为超级用户。

### `NICKNAME`

- **类型:** `Union[str, Iterable[str]]`

- **默认值:** `''`

- **说明:**

  超级用户的 QQ 号，用于命令的权限检查。

- **用法:**

  ```python
  SUPERUSERS = {12345678, 87654321}
  ```

  设置 `12345678` 和 `87654321` 为超级用户。

### `COMMAND_START`

- **类型:** `Iterable[Union[str, Pattern]]`

- **默认值:** `{'/', '!', '／', '！'}`

- **说明:**

  命令的起始标记，用于判断一条消息是不是命令。

- **用法:**

  ```python
  COMMAND_START = {'', '/', '!'}
  ```

  允许使用 `/`、`!` 作为命令起始符，或不用发送起始符。

### `COMMAND_SEP`

- **类型:** `Iterable[Union[str, Pattern]]`

- **默认值:** `{'/', '.'}`

- **说明:**

  命令的分隔标记，用于将文本形式的命令切分为元组（实际的命令名）。

- **用法:**

  ```python
  COMMAND_SEP = {'.'}
  ```

  将 `note.add` 这样的命令解析为 `('note', 'add')`。

### `SESSION_EXPIRE_TIMEOUT`

- **类型:** `Optional[datetime.timedelta]`

- **默认值:** `datetime.timedelta(minutes=5)`

- **说明:**

  命令会话的过期超时时长，超时后会话将被移除。`None` 表示不超时。

- **用法:**

  ```python
  from datetime import timedelta
  SESSION_EXPIRE_TIMEOUT = timedelta(minutes=2)
  ```

  设置过期超时为 2 分钟，即用户 2 分钟不发消息后，会话将被关闭。

### `SESSION_RUN_TIMEOUT`

- **类型:** `Optional[datetime.timedelta]`

- **默认值:** `None`

- **说明:**

  命令会话的运行超时时长，超时后会话将被移除，但不会停止此会话已经在运行的函数，它仍然会继续在后台执行。此时用户可以调用新的命令，开启新的会话。`None` 表示不超时。

- **用法:**

  ```python
  from datetime import timedelta
  SESSION_RUN_TIMEOUT = timedelta(seconds=10)
  ```

  设置运行超时为 10 秒，即命令会话运行达到 10 秒，NoneBot 将认为它已经结束。

### `SESSION_RUNNING_EXPRESSION`

- **类型:** `Expression_T`

- **默认值:** `'您有命令正在执行，请稍后再试'`

- **说明:**

  当有命令会话正在运行时，给用户新消息的回复。

- **用法:**

  ```python
  SESSION_RUNNING_EXPRESSION = ''
  ```

  设置为空，表示当有命令会话正在运行时，不回复用户的新消息。

### `SHORT_MESSAGE_MAX_LENGTH`

- **类型:** `int`

- **默认值:** `50`

- **说明:**

  短消息的最大长度。默认情况下（`only_short_message` 为 `True`），自然语言处理器只会响应消息中纯文本部分的长度总和小于等于此值的消息。

- **用法:**

  ```python
  SHORT_MESSAGE_MAX_LENGTH = 100
  ```

  设置最大长度为 100。

### `APSCHEDULER_CONFIG`

- **类型:** `Dict[str, Any]`

- **默认值:** `{'apscheduler.timezone': 'Asia/Shanghai'}`

- **说明:**

  APScheduler 的配置对象，见 [Configuring the scheduler](https://apscheduler.readthedocs.io/en/latest/userguide.html#configuring-the-scheduler)。
