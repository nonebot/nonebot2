# 类 Shell 的参数解析

`nonebot.argparse` 模块主要继承自 Python 内置的同名模块（`argparse`），用于解析命令的参数。在需要编写类 shell 语法的命令的时候，使用此模块可以大大提高开发效率。

「类 shell 语法」指的是形如 `some-command --verbose -n 3 --name=some-name argument1 argument2` 的类似于 shell 命令的语法。

下面给出一个使用 `argparse` 模块的实际例子：

```python {1-15}
@on_command('schedule', shell_like=True)
async def _(session: CommandSession):
    parser = ArgumentParser(session=session, usage=USAGE)
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

    args = parser.parse_args(session.argv)

    if not re.match(r'[_a-zA-Z][_a-zA-Z0-9]*', args.name):
        await session.send('计划任务名必须仅包含字母、数字、下划线，且以字母或下划线开头')
        return

    parsed_commands: List[ScheduledCommand] = []
    invalid_commands: List[str] = []

    if args.verbose:
        parsed_commands.append(
            ScheduledCommand(('echo',), f'开始执行计划任务 {args.name}……'))

    for cmd_str in args.commands:
        cmd, current_arg = parse_command(session.bot, cmd_str)
        if cmd:
            tmp_session = CommandSession(session.bot, session.ctx, cmd,
                                         current_arg=current_arg)
            if await cmd.run(tmp_session, dry=True):
                parsed_commands.append(ScheduledCommand(cmd.name, current_arg))
                continue
        invalid_commands.append(cmd_str)
    if invalid_commands:
        invalid_commands_joined = '\n'.join(
            [f'- {c}' for c in invalid_commands])
        await session.send(f'计划任务添加失败，'
                           f'因为下面的 {len(invalid_commands)} 个命令无法被运行'
                           f'（命令不存在或权限不够）：\n'
                           f'{invalid_commands_joined}')
        return

    trigger_args = {k: v for k, v in args.__dict__.items()
                    if k in {'second', 'minute', 'hour', 'day', 'month', 'day_of_week'}}
    try:
        job = await scheduler.add_scheduled_commands(
            parsed_commands,
            job_id=scheduler.make_job_id(PLUGIN_NAME, context_id(session.ctx), args.name),
            ctx=session.ctx,
            trigger='cron', **trigger_args,
            replace_existing=args.force
        )
    except scheduler.JobIdConflictError:
        # a job with same name exists
        await session.send(f'计划任务 {args.name} 已存在，'
                           f'若要覆盖请使用 --force 参数')
        return

    await session.send(f'计划任务 {args.name} 添加成功')
    await session.send(format_job(args.name, job))


USAGE = r"""
添加计划任务

使用方法：
    schedule.add [OPTIONS] --name NAME COMMAND [COMMAND ...]

OPTIONS：
    -h, --help  显示本使用帮助
    -S SECOND, --second SECOND  定时器的秒参数
    -M MINUTE, --minute MINUTE  定时器的分参数
    -H HOUR, --hour HOUR  定时器的时参数
    -d DAY, --day DAY  定时器  的日参数
    -m MONTH, --month MONTH  定时器的月参数
    -w DAY_OF_WEEK, --day-of-week DAY_OF_WEEK  定时器的星期参数
    -f, --force  强制覆盖已有的同名计划任务
    -v, --verbose  在执行计划任务时输出更多信息

NAME：
    计划任务名称

COMMAND：
    要计划执行的命令，如果有空格或特殊字符，需使用引号括起来
""".strip()
```

上面的例子出自 [cczu-osa/amadeus](https://github.com/cczu-osa/amadeus) 项目的计划任务插件，这里我们只关注前 15 行。

`on_command` 的 `shell_like=True` 参数告诉 NoneBot 这个命令需要使用类 shell 语法，NoneBot 会自动添加命令参数解析器来使用 Python 内置的 `shlex` 包分割参数。分割后的参数被放在 `session.args['argv']`，可通过 `session.argv` 属性来快速获得。

命令处理函数中，使用 `nonebot.argparse` 模块包装后的 `ArgumentParser` 类来解析参数，具体 `ArgumentParser` 添加参数的方法，请参考 [`argparse`](https://docs.python.org/3/library/argparse.html)。在使用 `add_argument()` 方法添加需要解析的参数后，使用 `parse_args()` 方法最终将 `argv` 解析为 `argparse.Namespace` 对象。

特别地，`parse_args()` 方法如果遇到需要打印帮助或报错并退出程序的情况（具体可以通过使用 Python 内置的 `argparse.ArgumentParser` 来体验），行为会更改为发送消息给当前 session 对应的上下文。注意到，`ArgumentParser` 类初始化时传入了 `session` 和 `usage` 参数，分别用于发送消息和使用帮助的内容。
