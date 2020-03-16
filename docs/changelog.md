---
sidebar: auto
---

# 更新日志

## next

- 弃用 `session.ctx` 属性，请使用 `session.event` 替代，该对象类型为 `aiocqhttp.Event`，可通过 property 访问内容
- 移除 `nonebot.tying.Context_T`，请使用 `aiocqhttp.Event` 替代
- 修复 `@on_command` 装饰后命令处理函数 docstring 丢失问题

## v1.4.2

- 修复 `CommandSession` 的部分方法在多线程条件下出错
- 优化日志输出多行消息的方法

## v1.4.1

- `on_command` 装饰器的 `aliases` 参数现支持字符串类型
- 在命令注册失败时，给出警告信息
- 修复 `helpers.render_expression` 的 bug

## v1.4.0

- 提升 aiocqhttp 依赖版本至 1.2，提升最低 Python 版本至 3.7
- 修复 `command.group` 的 stub 文件问题
- 修复 `helpers.render_expression` 没有转义位置参数的 bug
- 修复 `argparse.ArgumentParser` 在没有必填参数时不能正确使用的 bug

## v1.3.1

- `on_natural_language` 装饰器的 `keywords` 参数现可直接传字符串

## v1.3.0

- 允许机器人昵称和消息主体之间不使用空格或逗号分隔，即支持 `奶茶帮我查下天气` 这种用法
- 在处理命令之前检查机器人昵称，即在不编写自然语言处理器的情况下可以通过 `奶茶，echo 喵` 触发 `echo` 命令，而不再强制需要 at，其它命令同理
- 新增一种命令参数过滤器——控制器，在 `nonebot.command.argfilter.controllers` 模块，用于在过滤命令参数时对命令会话进行控制，内置了 `handle_cancellation()` 控制器允许用户取消正在进行的命令
- 新增命令参数验证失败次数的检查，可通过配置项 `MAX_VALIDATION_FAILURES` 和 `TOO_MANY_VALIDATION_FAILURES_EXPRESSION` 来配置最大失败次数和失败过多后的提示

## v1.2.3

- 修复 `nonebot.scheduler` 过早启动导致使用 Hypercorn 部署时计划任务无法运行的问题

同时使用计划任务功能和 Hypercorn 部署的用户请务必升级到此版本！

## v1.2.2

- 修复 `nonebot.natual_language.IntentCommand` 类 `current_arg` 参数默认为 `None` 导致的 bug
- `nonebot.helpers.render_expression` 函数新增 `*args` 用于向 Expression 传递位置参数

## v1.2.1

- 修复 `nonebot.helpers.context_id` 的 `group` 模式无法正确产生私聊用户 ID 的 bug

## v1.2.0

#### 新增

- 新增 `nonebot.natual_language.IntentCommand` 类，用于替代旧的 `NLPResult`（后者已弃用），使该类的意义更明确，并新增 `current_arg` 属性，可用于设置 `IntentCommand` 被调用时的 `current_arg`
- `nonebot` 模块新增了 `nonebot.helpers.context_id` 的快捷导入，以后可以直接通过 `nonebot.context_id` 使用
- `CommandSession` 类新增 `state` 属性，用于替代旧的 `args`（后者已弃用），明确其用于维持 session 状态的作用，本质上和原来的 `args` 等价
- `CommandSession` 类的 `get()` 方法新增 `arg_filters` 参数，表示正在询问用户的参数的过滤器，用于避免为每个参数编写 `args_parser`（一旦在 `get()` 时使用了 `arg_filters`，命令全局的 `args_parser` 将不会对这个参数运行），具体请参考 API 文档中的示例
- 新增 `nonebot.command.argfilter` 模块，内置了几种常用的参数过滤器，分别在 `extractors`、`validators`、`converters` 子模块
- 新增配置项 `DEFAULT_VALIDATION_FAILURE_EXPRESSION`，用于设置命令参数验证失败时的默认提示消息
- `nonebot.typing` 模块新增 `State_T` 和 `Filter_T`

#### 变更

- `CommandSession` 类的 `current_arg_text` 和 `current_arg_images` 现变更为只读属性
- 当使用 `CommandSession#get()` 方法获取参数后，若没有编写 `args_parser` 也没有传入 `arg_filters`，现在将会默认把用户输入直接当做参数，避免不断重复询问

#### 修复

- 修复交互式对话中，`ctx['to_me']` 没有置为 `True` 的 bug

#### 弃用

下述弃用内容可能会在若干版本后彻底移除，请适当做迁移。

- 弃用 `nonebot.natual_language.NLPResult` 类，请使用 `IntentCommand` 类替代
- 弃用 `CommandSession` 类的 `args` 属性，请使用 `state` 属性替代
- 弃用 `CommandSession` 类的 `get_optional()` 方法，请使用 `state.get()` 替代

#### 例子

以一个例子总结本次更新：

```python
from nonebot import *
from nonebot.command.argfilter import validators, extractors, ValidateError


async def my_custom_validator(value):
    if len(value) < 8:
        raise ValidateError('长度必须至少是 8 哦')
    return value


@on_command('demo')
async def demo(session: CommandSession):
    arg1_derived = session.state.get('arg1_derived')  # 从会话状态里尝试获取
    if arg1_derived is None:
        arg1: int = session.get(
            'arg1',
            prompt='请输入参数1',
            arg_filters=[
                extractors.extract_text,  # 提取纯文本部分
                str.strip,  # 去掉两边的空白
                validators.not_empty(),
                validators.match_regex(r'[0-9a-zA-Z]{6,20}', '必须为6~20位字符'),
                my_custom_validator,  # 自定义验证器
                int,  # 转换成 int
                validators.ensure_true(lambda x: x > 20000000, '必须大于2000000')
            ],
            at_sender=True,
        )
        arg1_derived = arg1 + 42
        session.state['arg1_derived'] = arg1_derived  # 修改会话状态

    arg2 = session.get(
        'arg2',
        prompt='请输入参数2',
        arg_filters=[
            extractors.extract_image_urls,  # 提取图片 URL 列表
            '\n'.join,  # 使用换行符拼接 URL 列表
            validators.not_empty('请至少发送一张图片'),
        ]
    )

    arg3 = session.get('arg3', prompt='你的arg3是什么呢？')

    reply = f'arg1_derived:\n{arg1_derived}\n\narg2:\n{arg2}\n\narg3:\n{arg3}'
    session.finish(reply)


@demo.args_parser
async def _(session: CommandSession):
    if session.is_first_run and session.current_arg_text.strip():
        # 第一次运行，如果有参数，则设置给 arg3
        session.state['arg3'] = session.current_arg_text.strip()

    # 如果不需要对参数进行特殊处理，则不用再手动加入 state，NoneBot 会自动放进去


@on_natural_language(keywords={'demo'})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'demo', current_arg='这是我的arg3')
```

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
