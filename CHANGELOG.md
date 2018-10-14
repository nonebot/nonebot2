# 更新日志

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
