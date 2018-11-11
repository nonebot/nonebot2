---
sidebar: auto
---

# 更新日志

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

- 修复快速的连续消息导致报错问题 [#5](https://github.com/richardchien/none-bot/issues/5)
