import atexit
import re
import shlex
from typing import Iterable, Tuple, Dict, Any

from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from none import get_bot, CommandGroup, CommandSession, permission as perm
from none.argparse import ArgumentParser, ParserExit
from none.command import parse_command, call_command
from none.helpers import context_id, send

sched = CommandGroup('schedule', permission=perm.PRIVATE | perm.GROUP_ADMIN,
                     only_to_me=False)

_bot = get_bot()

_scheduler = AsyncIOScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(
            url='sqlite:///' + _bot.get_data_file('db', 'schedule.sqlite'))
    },
    timezone='Asia/Shanghai'
)

if not _scheduler.running:
    _scheduler.start()


@atexit.register
def _():
    if _scheduler.running:
        _scheduler.shutdown()


async def _schedule_callback(ctx: Dict[str, Any], name: str,
                             commands: Iterable[Tuple[Tuple[str], str]],
                             verbose: bool = False):
    if verbose:
        await send(_bot, ctx, f'开始执行计划任务 {name}……')
    for cmd_name, current_arg in commands:
        await call_command(_bot, ctx, cmd_name,
                           current_arg=current_arg,
                           check_perm=True,
                           disable_interaction=True)


@sched.command('add', aliases=('schedule',))
async def sched_add(session: CommandSession):
    parser = ArgumentParser('schedule.add')
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

    argv = session.get_optional('argv')
    if not argv:
        await session.send(_sched_add_help)
        return

    try:
        args = parser.parse_args(argv)
    except ParserExit as e:
        if e.status == 0:
            # --help
            await session.send(_sched_add_help)
        else:
            await session.send('参数不足或不正确，请使用 --help 参数查询使用帮助')
        return

    if not re.match(r'[_a-zA-Z][_\w]*', args.name):
        await session.send(
            '计划任务名必须仅包含字母、数字、下划线，且以字母或下划线开头')
        return

    parsed_commands = []
    invalid_commands = []
    for cmd_str in args.commands:
        cmd, current_arg = parse_command(session.bot, cmd_str)
        if cmd:
            tmp_session = CommandSession(session.bot, session.ctx, cmd,
                                         current_arg=current_arg)
            if await cmd.run(tmp_session, dry=True):
                parsed_commands.append((cmd.name, current_arg))
            else:
                invalid_commands.append(cmd_str)
    if invalid_commands:
        invalid_commands_joined = '\r\n'.join(
            [f'{i+1}: {c}' for i, c in enumerate(invalid_commands)])
        await session.send(f'计划任务添加失败，'
                           f'因为下面的 {len(invalid_commands)} 个命令无法被运行'
                           f'（命令不存在或权限不够）：\r\n\r\n'
                           f'{invalid_commands_joined}')
        return

    job_id = f'{context_id(session.ctx)}/job/{args.name}'
    trigger_args = {k: v for k, v in args.__dict__.items()
                    if k in {'second', 'minute', 'hour',
                             'day', 'month', 'day_of_week'}}
    try:
        job = _scheduler.add_job(
            _schedule_callback,
            trigger='cron', **trigger_args,
            id=job_id,
            kwargs={
                'ctx': session.ctx,
                'name': args.name,
                'commands': parsed_commands,
                'verbose': args.verbose,
            },
            replace_existing=args.force,
            misfire_grace_time=30
        )
    except ConflictingIdError:
        # a job with same name exists
        await session.send(f'计划任务 {args.name} 已存在，'
                           f'若要覆盖请使用 --force 参数')
        return

    await session.send(f'计划任务 {args.name} 添加成功，下次运行时间：'
                       f'{job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")}')


@sched.command('list')
async def sched_list(session: CommandSession):
    pass


@sched.command('remove')
async def sched_remove(session: CommandSession):
    pass


@sched_add.args_parser
@sched_list.args_parser
@sched_remove.args_parser
async def _(session: CommandSession):
    session.args['argv'] = shlex.split(session.current_arg_text)


_sched_add_help = r"""
使用方法：schedule.add
""".strip()
