---
sidebar: auto
---

# 更新日志

## next

- 修复交互式对话中，`ctx['to_me']` 没有置为 `True` 的 bug

## v1.1.0

- 插件模块现可通过 `__plugin_name__` 和 `__plugin_usage__` 来分别指定插件名称和插件使用方法（两者均不强制，若不设置则默认为 `None`）
- 新增 `nonebot.plugin.get_loaded_plugins()` 函数用于获取所有已加载的插件集合
- `BaseSession.send()` 方法和 `nonebot.helpers.send()` 函数现返回 API 调用返回值（即 CQHTTP 插件的返回结果的 `data` 字段）
- `BaseSession` 新增 `self_id` 属性，可通过 `session.self_id` 代替 `session.ctx['self_id']` 来获取当前机器人账号
- `only_to_me` 的命令现可以通过在消息结尾 @ 机器人触发，而不必在开头

## v1.0.0

- 更改包名为 `nonebot`，请注意修改导入语句，原先 `import none` 改为 `import nonebot`，`from none import something` 改为 `from nonebot import something`，`none.something` 改为 `nonebot.something`，如果代码量比较大，可以使用 `import nonebot as none`，以避免过多更改
- `nonebot.command.kill_current_session()` 方法去掉了 `bot` 参数，现只需传入 `ctx`

## v0.5.3

- 修复使用多级命令时，命令查找会出现异常的情况
- 调整 `none.load_plugins()` 等方法，返回加载成功的插件数量，并新增 `none.load_plugin()` 方法用于加载单个插件模块

## v0.5.2

- 修复自然语言处理器匹配机器人昵称时的 bug
- 修复一些与异常处理有关的小问题

## v0.5.1

- 给所有发送消息的函数和方法（`BaseSession.send()`、`CommandSession.pause()`、`CommandSession.finish()` 等）新增了 `**kwargs`，并将此参数继续传递给 python-aiocqhttp 的 `CQHttp.send()` 方法，从而支持 `at_sender` 参数（默认 `False`），**注意，此功能需要安装 `aiocqhttp>=0.6.7`**
- `BaseSession.send()` 方法新增 `ensure_private` 参数，类型 `bool`，默认 `False`，可用于确保发送消息到私聊（对于群消息，会私聊发送给发送人）

## v0.5.0

- 修复调用不存在的多级命令（例如 `/echo/nonexist`）时，抛出异常导致 WebSocket 连接断开的问题
- 调整 Expression 相关接口：移除了所有 `send_expr()` 函数和方法，移除了 `CommandSession.get()` 方法的 `prompt_expr` 参数，移除了 `none.expression` 模块，原 `render()` 函数移动到 `none.helpers` 模块并改名为 `render_expression()`
- 修改 `none.argparse.ArgumentParser` 类的构造方法和 `parse_args()` 方法：构造方法新增 `session` 参数，可传入 `CommandSession` 对象；`parse_args()` 方法可直接用于解析参数，用户输入的参数错误，会发送错误提示或使用帮助
- `on_command` 装饰器新增 `shell_like` 参数，设为 `True`（默认 `False`）将自动以类 shell 语法分割命令参数 `current_arg`（不再需要自行编写 args parser），并将分割后的参数列表放入 `session.args['argv']`
- `CommandSession` 类新增 `argv` 只读属性，用于获取 `session.args['argv']`，如不存在，则返回空列表

## v0.4.3

- 自然语言处理器支持响应只有机器人昵称而没有实际内容的消息，通过 `on_natural_language` 的 `allow_empty_message` 参数开启（默认关闭）

## v0.4.2

- 修复命令处理器中抛出异常导致运行超时 `SESSION_RUN_TIMEOUT` 不生效的问题

## v0.4.1

- `load_plugins()` 导入模块失败时打印错误信息，且日志级别从 warning 改为 error
- 修复 `CommandName_T` 的问题
- 修复特权命令在不满足 `to_me` 条件时没有被当做现有 session 的新参数的问题

## v0.4.0

- `message_preprocessor` 装饰器现要求被装饰函数接收 `bot` 和 `ctx` 两个参数
- 调整了 Type Hint，使其更准确，并新增 `none.typing` 模块，提供部分常用类型
- 规范部分模块的导入，现可通过 `none.Message` 访问 `aiocqhttp.Message`，通过 `none.CQHttpError` 访问 `aiocqhttp.Error`

## v0.3.2

- `none.message` 模块现已导入所有 `aiocqhttp.message` 中的内容，因此不必再从后者导入 `Message`、`escape` 等类和函数
- 命令的运行加入了超时机制，可通过 `SESSION_RUN_TIMEOUT` 配置，类型为 `datetime.timedelta`，默认为 `None` 表示永不超时
- `on_command` 装饰器新增 `privileged` 参数，可将命令设置为特权命令，特权命令即使在已存在其它 CommandSession 的情况下也会运行，但它不会覆盖当前 CommandSession
- 新增 `none.command.kill_current_session()` 函数用于杀死当前已存在的 CommandSession（不会终止已经在运行的命令，但会移除 session 对象）

## v0.3.1

- 调整计划任务的启动时间，修复创建任务后无法立即获取下次运行时间的 bug

## v0.3.0

- 内置可选的计划任务功能（需要安装 APScheduler）

## v0.2.2

- 修复快速的连续消息导致报错问题 [#5](https://github.com/richardchien/nonebot/issues/5)
