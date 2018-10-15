---
sidebar: auto
---

# API

## 类型

下面的 API 文档中，「类型」部分使用 Python 的 Type Hint 语法，见 [PEP 484](https://www.python.org/dev/peps/pep-0484/)、[PEP 526](https://www.python.org/dev/peps/pep-0526/) 和 [typing](https://docs.python.org/3/library/typing.html)。

除了 Python 内置的类型，下面还出现了如下 NoneBot 自定类型，实际上它们是 Python 内置类型的别名。

### `Context_T`

- **类型:** `Dict[str, Any]`

- **说明:**

  酷 Q HTTP API 上报的事件数据对象的类型。

### `Message_T`

- **类型:** `Union[str, Dict[str, Any], List[Dict[str, Any]]]`

- **说明:**

  消息对象的类型，通常表示 NoneBot 提供的消息相关接口所支持的类型，`none.message.Message` 也是一个合法的 `Message_T`。

### `Expression_T`

- **类型:** `Union[str, Sequence[str], Callable]`

- **说明:**

  Expression 对象的类型。

### `CommandName_T`

- **类型:** `Tuple[str]`

- **说明:**

  命令名称的类型。

### `CommandArgs_T`

- **类型:** `Dict[str, Any]`

- **说明:**

  命令参数的类型。

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

## none 模块

## `none.message` 模块

### _decorator_ `message_preprocessor`

- **说明:**

  将函数装饰为消息预处理器。

- **要求:**

  被装饰函数必须是一个 async 函数，且必须接收且仅接收两个位置参数，类型分别为 `NoneBot` 和 `Context_T`，即形如：

  ```python
  async def func(bot: NoneBot, ctx: Context_T):
      pass
  ```

- **用法:**

  ```python
  @message_preprocessor
  async def _(bot: NoneBot, ctx: Context_T):
      ctx['preprocessed'] = True
  ```

  在所有消息处理之前，向消息事件上下文对象中加入 `preprocessed` 字段。

### _class_ `MessageSegment`

从 `aiocqhttp.message` 模块导入，继承自 `dict`，用于表示一个消息段。该类型是合法的 `Message_T`。

更多关于消息段的内容，见 [消息格式](https://cqhttp.cc/docs/#/Message)。

#### `type`

- **类型:** `str`

- **说明:**

  消息段类型。

#### `data`

- **类型:** `Dict[str, Any]`

- **说明:**

  消息段数据。

#### `__init__(self, d=None, *, type=None, data=None)`

- **说明:**

  初始化消息段对象。

- **参数:**

  - `d: Dict[str, Any]`: 当有此参数且此参数中有 `type` 字段时，由此参数构造消息段
  - `type: str`: 当没有传入 `d` 参数或 `d` 参数无法识别时，此参数必填，对应消息段的 `type` 字段
  - `data: Dict[str, str]`: 对应消息段的 `data` 字段，若不传入则初始化为 `{}`

- **异常:**

  - `ValueError`: 没有正确传入 `type` 参数

- **用法:**

  ```python
  seg1 = MessageSegment({'type': 'face', 'data': {'id': '123'}})
  seg2 = MessageSegment(type='face', data={'id': '123'})
  ```

#### `__str__()`

- **说明:**

  将消息段转换成字符串格式。

- **返回:**

  - `str`: 字符串格式的消息段

- **用法:**

  ```python
  str(MessageSegment.face(123))
  ```

#### `__eq__(other)`

- **说明:**

  判断两个消息段是否相同。

- **参数:**

  - `other: Any`: 要比较的对象

- **返回:**

  - `bool`: 两个消息段相同

- **用法:**

  ```python
  MessageSegment.face(123) == MessageSegment(type='face', data={'id': '123'})
  ```

#### _staticmethod_ `text(text)`

- **说明:**

  构造纯文本消息段。

- **参数:**

  - `text: str`: 文本内容

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `emoji(id_)`

- **说明:**

  构造 emoji 消息段。

- **参数:**

  - `id_: int`: Emoji ID（Unicode 代码点）

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `face(id_)`

- **说明:**

  构造 QQ 表情消息段。

- **参数:**

  - `id_: int`: QQ 表情 ID

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `image(file)`

- **说明:**

  构造图片消息段。

- **参数:**

  - `file: str`: 图片文件名、路径、URL、或 Base64 编码

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `record(file, magic=False)`

- **说明:**

  构造语音消息段。

- **参数:**

  - `file: str`: 语音文件名、路径、URL、或 Base64 编码
  - `magic: bool`: 是否使用变声

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `at(user_id)`

- **说明:**

  构造 @ 消息段。

- **参数:**

  - `user_id: int`: 要 @ 用户 QQ 号

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `rps()`

- **说明:**

  构造猜拳消息段。

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `dice()`

- **说明:**

  构造掷骰子消息段。

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `shake()`

- **说明:**

  构造窗口抖动消息段。

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `anonymous(ignore_failure=False)`

- **说明:**

  构造匿名消息段。

- **参数:**

  - `ignore_failure: bool`: 是否忽略匿名失败，如果忽略，则匿名失败时仍使用真实身份发送消息

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `share(url, title, content='', image_url='')`

- **说明:**

  构造链接分享消息段。

- **参数:**

  - `url: str`: 链接 URL
  - `title: str`: 卡片标题
  - `content: str`: 卡片内容
  - `image_url: str`: 图片 URL

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `contact_user(id_)`

- **说明:**

  构造好友分享消息段。

- **参数:**

  - `id_: int`: 好友 QQ 号

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `contact_group(id_)`

- **说明:**

  构造群组分享消息段。

- **参数:**

  - `id_: int`: 群号

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `location(latitude, longitude, title='', content='')`

- **说明:**

  构造位置分享消息段。

- **参数:**

  - `latitude: float`: 纬度
  - `longitude: float`: 经度
  - `title: str`: 卡片标题
  - `content: str`: 卡片内容

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `music(type_, id_)`

- **说明:**

  构造音乐分享消息段。

- **参数:**

  - `type_: str`: 分享类型
  - `id_: int`: 音乐 ID

- **返回:**

  - `MessageSegment`: 消息段对象

#### _staticmethod_ `music_custom(url, audio_url, title, content='', image_url='')`

- **说明:**

  构造自定义音乐分享消息段。

- **参数:**

  - `url: str`: 链接 URL
  - `audio_url: str`: 音频 URL
  - `title: str`: 卡片标题
  - `content: str`: 卡片内容
  - `image_url: str`: 图片 URL

- **返回:**

  - `MessageSegment`: 消息段对象

### _class_ `Message`

从 `aiocqhttp.message` 模块导入，继承自 `list`，用于表示一个消息。该类型是合法的 `Message_T`。

#### `__init__(self, msg=None)`

- **说明:**

  初始化消息对象。

- **参数:**

  - `msg: Optional[Message_T]`: 消息内容，若不传入则构造空消息

- **异常:**

  - `ValueError`: `msg` 参数不是一个合法的 `Message_T`

- **用法:**

  ```python
  msg = Message('你好')
  ```

#### `__str__()`

- **说明:**

  将消息转换成字符串格式。

- **返回:**

  - `str`: 字符串格式的消息

- **用法:**

  ```python
  str(ctx['message'])
  ```

#### `__add__(other)`

- **说明:**

  将两个消息对象拼接。

- **参数:**

  - `other: Message_T`: 任何符合 `Message_T` 类型的对象

- **返回:**

  - `Message`: 两个消息拼接的结果

- **异常:**

  - `ValueError`: `other` 参数不是一个合法的 `Message_T`

- **用法:**

  ```python
  msg = Message('你好') + '，世界！'
  ```

#### `append(obj)`

- **说明:**

  将一个消息段拼接到当前消息的尾部。

- **参数:**

  - `obj: Any`: `MessageSegment` 对象，或任何可以传入 `MessageSegment` 构造函数的对象

- **返回:**

  - `None`

- **异常:**

  - `ValueError`: `obj` 参数不是一个能够被识别的消息段

- **用法:**

  ```python
  msg = Message('你好')
  msg.append(MessageSegment.face(14))
  ```

#### `extend(msg)`

- **说明:**

  将一个消息拼接到当前消息的尾部。

- **参数:**

  - `msg: Any`: 字符串，或任何元素能够传入 `append()` 的 `Iterable`

- **返回:**

  - `None`

- **异常:**

  - `ValueError`: `msg` 参数不是一个能够被识别的消息

- **用法:**

  ```python
  msg = Message('你好')
  msg.extend('[CQ:face,id=14]')
  ```

### `escape(s, *, escape_comma=True)`

- **说明:**

  从 `aiocqhttp.message` 模块导入，对字符串进行转义。

- **参数:**

  - `s: str`: 要转义的字符串
  - `escape_comma: bool`: 是否转义英文逗号 `,`

- **返回:**

  - `str`: 转义后的字符串

### `unescape(s)`

- **说明:**

  从 `aiocqhttp.message` 模块导入，对字符串进行去转义。

- **参数:**

  - `s: str`: 要去转义的字符串

- **返回:**

  - `str`: 去转义后的字符串

## `none.command` 模块

### _decorator_ `on_command(name, *, aliases=(), permission=perm.EVERYBODY, only_to_me=True, privileged=False)`

- **说明:**

  将函数装饰为命令处理器。

  被装饰的函数将会获得一个 `args_parser` 属性，是一个装饰器，下面会有详细说明。

- **参数:**

  - `name: Union[str, CommandName_T]`: 命令名，如果传入的是字符串则会自动转为元组
  - `aliases: Iterable[str]`: 命令别名
  - `permission: int`: 命令所需要的权限，不满足权限的用户将无法触发该命令
  - `only_to_me: bool`: 是否只响应确定是在和「我」（机器人）说话的命令
  - `privileged: bool`: 是否特权命令，若是，则无论当前是否有命令会话正在运行，都会运行该命令，但运行后不会保留 Session

- **要求:**

  被装饰函数必须是一个 async 函数，且必须接收且仅接收一个位置参数，类型为 `CommandSession`，即形如：

  ```python
  async def func(session: CommandSession):
      pass
  ```

- **用法:**

  ```python
  @on_command('echo')
  async def _(session: CommandSession):
      await session.send(session.current_arg)
  ```

  一个简单的复读命令。

### _decorator_ _command_func._`args_parser`

- **说明:**

  将函数装饰为命令参数解析器。

- **要求:**

  对被装饰函数的要求同 `on_command` 装饰器。

- **用法:**

  ```python
  @my_cmd.args_parser
  async def _(session: CommandSession):
      stripped_text = session.current_arg_text.strip()
      if not session.current_key and stripped_text:
          session.current_key = 'initial_arg'
      session.args[session.current_key] = stripped_text
  ```

  一个典型的命令参数解析器。

### _class_ `CommandGroup`

命令组，用于声明一组有相同名称前缀的命令。

#### `basename`

- **类型:** `CommandName_T`

- **说明:**

  命令名前缀。

#### `permission`

- **类型:** `Optional[int]`

- **说明:**

  命令组内命令的默认 `permission` 属性。

#### `only_to_me`

- **类型:** `Optional[bool]`

- **说明:**

  命令组内命令的默认 `only_to_me` 属性。

#### `privileged`

- **类型:** `Optional[bool]`

- **说明:**

  命令组内命令的默认 `privileged` 属性。

#### `__init__(name, permission=None, *, only_to_me=None, privileged=None)`

- **说明:**

  初始化命令组，参数即为上面的三个属性。

- **参数:**

  - `name: Union[str, CommandName_T]`: 命令名前缀，若传入字符串，则会自动转换成元组
  - `permission: Optional[int]`: 对应 `permission` 属性
  - `only_to_me: Optional[bool]`: 对应 `only_to_me` 属性
  - `privileged: Optional[bool]`: 对应 `privileged` 属性

#### _decorator_ `command(name, *, aliases=None, permission=None, only_to_me=None, privileged=None)`

- **说明:**

  将函数装饰为命令组中的命令处理器。使用方法和 `on_command` 装饰器完全相同。

- **参数:**

  - `name: Union[str, CommandName_T]`: 命令名，注册命令处理器时会加上命令组的前缀
  - `aliases: Optional[Iterable[str]]`: 和 `on_command` 装饰器含义相同，若不传入则使用命令组默认值，若命令组没有默认值，则使用 `on_command` 装饰器的默认值
  - `permission: Optional[int]`: 同上
  - `only_to_me: Optional[bool]`: 同上
  - `privileged: Optional[bool]`: 同上

- **用法:**

  ```python
  sched = CommandGroup('scheduler')

  @sched.command('add', permission=PRIVATE)
  async def _(session: CommandSession)
      pass
  ```

  注册 `('scheduler', 'add')` 命令。

## `none.natural_language` 模块

### _decorator_ `on_natural_language(keywords=None, *, permission=EVERYBODY, only_to_me=True, only_short_message=True)`

- **说明:**

  将函数装饰为自然语言处理器。

- **参数:**

  - `keywords: Optional[Iterable]`: 要响应的关键词，若传入 `None`，则响应所有消息
  - `permission: int`: 自然语言处理器所需要的权限，不满足权限的用户将无法触发该处理器
  - `only_to_me: bool`: 是否只响应确定是在和「我」（机器人）说话的消息
  - `only_short_message: bool`: 是否只响应短消息

- **要求:**

  被装饰函数必须是一个 async 函数，且必须接收且仅接收一个位置参数，类型为 `NLPSession`，即形如：

  ```python
  async def func(session: NLPSession):
      pass
  ```

- **用法:**

  ```python
  @on_natural_language({'天气'}, only_to_me=False)
  async def _(session: NLPSession):
      return NLPResult(100.0, ('weather',), None)
  ```

  响应所有带有「天气」关键词的消息，当做 `weather` 命令处理。

### _class_ `NLPSession`

继承自 `BaseSession` 类，表示自然语言处理 Session。

#### `msg`

- **类型:** `str`

- **说明:**

  以字符串形式表示的消息内容，已去除开头的 @ 和机器人称呼。

#### `msg_text`

- **类型:** `str`

- **说明:**

  消息内容的纯文本部分，已去除所有 CQ 码／非 `text` 类型的消息段。各纯文本消息段之间使用空格连接。

#### `msg_images`

- **类型:** `List[str]`

- **说明:**

  消息内容中所有图片的 URL 的列表，如果消息中没有图片，则为 `[]`。

### _class_ `NLPResult`

用于表示自然语言处理的结果，是一个 namedtuple，由自然语言处理器返回。

#### `confidence`

- **类型:** `float`

- **说明:**

  自然语言处理结果的置信度，即消息意图确实符合此 `NLPResult` 的概率。

#### `cmd_name`

- **类型:** `Union[str, CommandName_T]`

- **说明:**

  消息所对应的命令的名称。

#### `cmd_args`

- **类型:** `Optional[CommandArgs_T]`

- **说明:**

  消息所对应的命令的参数。

#### `__init__(confidence, cmd_name, cmd_args=None)`

- **说明:**

  初始化 `NLPResult` 对象，参数即为上面的三个属性。

## `none.notice_request` 模块

### _decorator_ `on_notice(*events)`

- **说明:**

  将函数装饰为通知处理器。

- **参数:**

  - `*events: str`: 要处理的通知类型（`notice_type`），若不传入，则处理所有通知

- **要求:**

  被装饰函数必须是一个 async 函数，且必须接收且仅接收一个位置参数，类型为 `NoticeSession`，即形如：

  ```python
  async def func(session: NoticeSession):
      pass
  ```

- **用法:**

  ```python
  @on_notice
  async def _(session: NoticeSession):
      logger.info('有新的通知事件：%s', session.ctx)

  @on_notice('group_increase')
  async def _(session: NoticeSession):
      await session.send('欢迎新朋友～')
  ```

  收到所有通知时打日志，收到新成员进群通知时除了打日志还发送欢迎信息。

### _decorator_ `on_request(*events)`

- **说明:**

  将函数装饰为请求处理器。

- **参数:**

  - `*events: str`: 要处理的请求类型（`request_type`），若不传入，则处理所有请求

- **要求:**

  被装饰函数必须是一个 async 函数，且必须接收且仅接收一个位置参数，类型为 `RequestSession`，即形如：

  ```python
  async def func(session: RequestSession):
      pass
  ```

- **用法:**

  ```python
  @on_request
  async def _(session: RequestSession):
      logger.info('有新的请求事件：%s', session.ctx)

  @on_request('group')
  async def _(session: RequestSession):
      await session.approve()
  ```

  收到所有请求时打日志，收到群请求时除了打日志还同意请求。

### _class_ `NoticeSession`

继承自 `BaseSession` 类，表示通知类事件的 Session。

### _class_ `RequestSession`

继承自 `BaseSession` 类，表示请求类事件的 Session。

#### _coroutine_ `approve(remark='')`

- **说明:**

  同意当前请求。

- **参数:**
  - `remark: str`: 好友备注，只在好友请求时有效

- **返回:**

  - `None`

- **异常:**

  - `CQHttpError`: 发送失败时抛出，实际由 [aiocqhttp] 抛出，等价于 `aiocqhttp.Error`

- **用法:**

  ```python
  await session.approve()
  ```

#### _coroutine_ `reject(reason='')`

- **说明:**

  拒绝当前请求。

- **参数:**

  - `reason: str`: 拒绝理由，只在群请求时有效

- **返回:**

  - `None`

- **异常:**

  - `CQHttpError`: 发送失败时抛出，实际由 [aiocqhttp] 抛出，等价于 `aiocqhttp.Error`

- **用法:**

  ```python
  await session.reject()
  ```

## `none.session` 模块

### _class_ `BaseSession`

基础 session 类，`CommandSession` 等均继承自此类。

#### `bot`

- **类型:** `NoneBot`

- **说明:**

  Session 对应的 NoneBot 对象。

- **用法:**

  ```python
  await session.bot.send('hello')
  ```

  在当前 Session 对应的上下文中发送 `hello`。

#### `ctx`

- **类型:** `Context_T`

- **说明:**

  酷 Q HTTP API 上报的事件数据对象，或称事件上下文。

- **用法:**

  ```python
  user_id = session.ctx['user_id']
  ```

  获取当前事件上下文的 `user_id` 字段。

#### _coroutine_ `send(message, *, ignore_failure=True)`

- **说明:**

  发送消息到 Session 对应的上下文中。

- **参数:**
  - `message: Message_T`: 要发送的消息内容
  - `ignore_failure: bool`: 发送失败时忽略 `CQHttpError` 异常

- **返回:**

  - `None`

- **异常:**

  - `CQHttpError`: 发送失败时抛出，实际由 [aiocqhttp] 抛出，等价于 `aiocqhttp.Error`

- **用法:**

  ```python
  await session.send('hello')
  ```

  在当前 Session 对应的上下文中发送 `hello`。

#### _coroutine_ `send_expr(expr, **kwargs)`

- **说明:**

  渲染 Expression，并发送生成的消息到 Session 对应的上下文中。

- **参数:**

  - `expr: Expression_T`: 要发送的 Expression
  - `**kwargs: Any`: 传入 `none.expression.render()` 的命名参数

- **返回:**

  - `None`

- **异常:**

  - `CQHttpError`: 发送失败时抛出，实际由 [aiocqhttp] 抛出，等价于 `aiocqhttp.Error`

- **用法:**

  ```python
  await session.send_expr(
      expr=['你好，{username}！',
            '欢迎回来，{username}～'],
      username=username
  )
  ```

## `none.expression` 模块

### `render(expr, *, escape_args=True, **kwargs)`

- **说明:**

  渲染 Expression。

- **参数:**

  - `expr: Expression_T`: 要渲染的 Expression
  - `escape_args: bool`: 是否对渲染参数进行转义
  - `**kwargs: Any`: 渲染参数，用于 `str.format()` 或 Expression 函数调用传参

- **返回:**

  - `str`: 渲染出的消息字符串

- **用法:**

  ```python
  msg = render(
      expr=['你好，{username}！',
            '欢迎回来，{username}～'],
      username=username
  )
  ```

## `none.permission` 模块

### 权限声明常量

- `PRIVATE_FRIEND`: 好友私聊
- `PRIVATE_GROUP`: 群临时私聊
- `PRIVATE_DISCUSS`: 讨论组临时私聊
- `PRIVATE_OTHER`: 其它私聊
- `PRIVATE`: 任何私聊
- `DISCUSS`: 讨论组
- `GROUP_MEMBER`: 群成员
- `GROUP_ADMIN`: 群管理员
- `GROUP_OWNER`: 群主
- `GROUP`: 任何群成员
- `SUPERUSER`: 超级用户
- `EVERYBODY`: 任何人

用于权限声明的常量可通过 `|` 合并，在命令或自然语言处理器装饰器的 `permission` 参数中传入，表示允许触发相应命令或自然语言处理器的用户类型。

例如下面的代码中，只有私聊和群管理员可以访问 `hello` 命令：

```python
@none.on_command('hello', permission=PRIVATE | GROUP_ADMIN)
async def _(session):
    pass
```

需要注意的是，当一个用户是「群管理员」时，ta 同时也是「群成员」；当 ta 是「群主」时，ta 同时也是「群管理员」和「群成员」。

### _coroutine_ `check_permission(bot, ctx, permission_required)`

- **说明:**

  检查用户是否具有所要求的权限。

- **参数:**

  - `bot: NoneBot`: NoneBot 对象
  - `ctx: Context_T`: 消息事件上下文对象
  - `permission_required: int`: 要求的权限值

- **返回:**

  - `bool`: 消息事件上下文所对应的用户是否具有所要求的权限

- **用法:**

  ```python
  has_perm = await check_permission(bot, ctx, cmd.permission)
  ```

## `none.log` 模块

### `logger`

- **类型:** `logging.Logger`

- **说明:**

  NoneBot 全局的 logger。

- **用法:**

  ```python
  logger.debug('Some log message here')
  ```

## `none.helpers` 模块

### `context_id(ctx, *, mode='default', use_hash=False)`

- **说明:**

  获取事件上下文的唯一 ID。

- **参数:**

  - `ctx: Context_T`: 事件上下文对象
  - `mode: str`: ID 的计算模式
    - `'default'`: 默认模式，任何一个上下文都有其唯一 ID
    - `'group'`: 群组模式，同一个群组或讨论组的上下文（即使是不同用户）具有相同 ID
    - `'user'`: 用户模式，同一个用户的上下文（即使在不同群组）具有相同 ID
  - `use_hash: bool`: 是否将计算出的 ID 使用 MD5 进行哈希

- **返回:**

  - `str`: 事件上下文的唯一 ID

- **用法:**

  ```python
  ctx_id = context_id(session.ctx, use_hash=True)
  ```

  获取当前 Session 的事件上下文对应的唯一 ID，并进行 MD5 哈希，得到的结果可用于图灵机器人等 API 的调用。

### _coroutine_ `send(bot, ctx, message, *, ignore_failure=True)`

- **说明:**

  发送消息到指定事件上下文中。

- **参数:**

  - `bot: NoneBot`: NoneBot 对象
  - `ctx: Context_T`: 事件上下文对象
  - `message: Message_T`: 要发送的消息内容
  - `ignore_failure: bool`: 发送失败时忽略 `CQHttpError` 异常

- **返回:**

  - `None`

- **异常:**

  - `CQHttpError`: 发送失败时抛出，实际由 [aiocqhttp] 抛出，等价于 `aiocqhttp.Error`

- **用法:**

  ```python
  await send(bot, ctx, 'hello')
  ```

### _coroutine_ `send_expr(bot, ctx, expr, **kwargs)`

- **说明:**

  渲染 Expression，并发送生成的消息到指定事件上下文中。

- **参数:**

  - `bot: NoneBot`: NoneBot 对象
  - `ctx: Context_T`: 事件上下文对象
  - `expr: Expression_T`: 要发送的 Expression
  - `**kwargs: Any`: 传入 `none.expression.render()` 的命名参数

- **返回:**

  - `None`

- **异常:**

  - `CQHttpError`: 发送失败时抛出，实际由 [aiocqhttp] 抛出，等价于 `aiocqhttp.Error`

- **用法:**

  ```python
  await send_expr(
      bot, ctx,
      expr=['你好，{username}！',
            '欢迎回来，{username}～'],
      username=username
  )
  ```

## `none.argparse` 模块

### _class_ `ArgumentParser`

继承自 `argparse.ArgumentParser` 类，修改部分函数实现使其不再打印文本到标准输出、并且不再在参数错误时直接退出程序。

此类可用于命令参数的解析。基本用法和 Python 内置的 `argparse.ArgumentParser` 类一致，区别是当它需要导致程序退出时，行为改变为抛出 `none.argparse.ParserExit` 异常。

- **用法:**

  ```python
  parser = ArgumentParser()
  parser.add_argument('-S', '--second')
  parser.add_argument('-M', '--minute')
  parser.add_argument('-H', '--hour')
  parser.add_argument('-d', '--day')
  parser.add_argument('-m', '--month')
  parser.add_argument('-w', '--day-of-week')
  parser.add_argument('-f', '--force', action='store_true', default=False)
  parser.add_argument('-v', '--verbose', action='store_true', default=False)
  parser.add_argument('--name', required=True)
  parser.add_argument('commands', nargs='+')

  argv = ['-S', '*/10', '-v', '--force', '--name', 'test', 'echo wow']

  try:
      return parser.parse_args(argv)
  except ParserExit as e:
      if e.status == 0:
          # --help
          await session.send(help_msg)
      else:
          await session.send('参数不足或不正确，请使用 --help 参数查询使用帮助')
  ```

### _class_ `ParserExit`

继承自 `RuntimeError` 类，在 `ArgumentParser` 解析出错时抛出。

#### `status`

- **说明:**

  `argparse.ArgumentParser` 类的 `exit()` 方法的 `status` 参数。

#### `message`

- **说明:**

  `argparse.ArgumentParser` 类的 `exit()` 方法的 `message` 参数。

## `none.sched` 模块

### _class_ `Scheduler`

继承自 `apscheduler.schedulers.asyncio.AsyncIOScheduler` 类，功能不变。

当 Python 环境中没有安装 APScheduler 包时，此类不存在，`Scheduler` 为 `None`。

<!-- 链接 -->

[aiocqhttp]: https://github.com/richardchien/python-aiocqhttp/
