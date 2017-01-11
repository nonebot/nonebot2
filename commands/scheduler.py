import os
import re
from functools import reduce, wraps

import pytz
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.base import JobLookupError

from command import CommandRegistry, hub as cmdhub
from command import CommandNotExistsError, CommandScopeError, CommandPermissionError
from commands import core
from little_shit import get_db_dir, get_command_args_start_flags, get_target

_db_url = 'sqlite:///' + os.path.join(get_db_dir(), 'scheduler.sqlite')

_scheduler = BackgroundScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(url=_db_url)
    },
    executors={
        'default': ProcessPoolExecutor(max_workers=5)
    },
    timezone=pytz.timezone('Asia/Shanghai')
)

_command_args_start_flags = get_command_args_start_flags()

_args_split_sep = '[ \n\t]'


def _init():
    _scheduler.start()


__registry__ = cr = CommandRegistry(init_func=_init)


class _InvalidTriggerArgsError(Exception):
    pass


class _IncompleteArgsError(Exception):
    pass


def _call_commands(job_id, command_list, ctx_msg, internal=False):
    for command in command_list:
        try:
            cmdhub.call(command[0], command[1], ctx_msg)
        except CommandNotExistsError:
            core.echo('没有找到计划任务 %s 中的命令 %s' % (job_id, command[0]), ctx_msg, internal)
        except CommandPermissionError:
            core.echo('你没有权限执行计划任务 %s 中的命令 %s' % (job_id, command[0]), ctx_msg, internal)
        except CommandScopeError as se:
            core.echo(
                '计划任务 %s 中的命令 %s 不支持 %s' % (job_id, command[0], se.msg_type),
                ctx_msg, internal
            )


def _check_target(func):
    @wraps(func)
    def wrapper(args_text, ctx_msg, internal=False, *args, **kwargs):
        target = get_target(ctx_msg)
        if not target:
            _send_fail_to_get_target_msg(ctx_msg, internal)
            return None
        else:
            return func(args_text, ctx_msg, internal, *args, **kwargs)

    return wrapper


@cr.register('cron_check', 'cron-check', 'cron_test', 'cron-test')
def cron_check(args_text, ctx_msg):
    cron = args_text.strip()
    if not cron:
        core.echo('请指定要检查的 Cron 时间表达式', ctx_msg)
        return

    resp = requests.post('http://tool.lu/crontab/ajax.html', data={'expression': cron})
    if resp.status_code == 200:
        data = resp.json()
        if data.get('status') and 'dates' in data:
            reply = '接下来 7 次的执行时间：\n' + '\n'.join(data['dates'])
            core.echo(reply, ctx_msg)
            return

    core.echo('检查失败，可能因为表达式格式错误或服务器连接不上', ctx_msg)


@cr.register('add_job', 'add-job', 'add')
@cr.restrict(full_command_only=True, group_admin_only=True)
@_check_target
def add_job(args_text, ctx_msg, internal=False):
    if args_text.strip() in ('', 'help', '-h', '--help') and not internal:
        _send_add_job_help_msg(ctx_msg, internal)
        return

    args_text = args_text.lstrip()
    try:
        # Parse trigger args
        trigger_args = {}
        if args_text.startswith('-'):
            # options mode
            key_dict = {
                '-M': 'minute',
                '-H': 'hour',
                '-d': 'day',
                '-m': 'month',
                '-w': 'day_of_week'
            }
            while args_text.startswith('-') and not args_text.startswith('--'):
                try:
                    option, value, args_text = re.split(_args_split_sep, args_text, 2)
                    trigger_args[key_dict[option]] = value
                    args_text = args_text.lstrip()
                except (ValueError, KeyError):
                    # Split failed or get key failed, which means format is not correct
                    raise _InvalidTriggerArgsError
        else:
            # cron mode
            try:
                trigger_args['minute'], \
                trigger_args['hour'], \
                trigger_args['day'], \
                trigger_args['month'], \
                trigger_args['day_of_week'], \
                args_text = re.split(_args_split_sep, args_text, 5)
                args_text = args_text.lstrip()
            except ValueError:
                # Split failed, which means format is not correct
                raise _InvalidTriggerArgsError

        # Parse '--multi' option
        multi = False
        if args_text.startswith('--multi '):
            multi = True
            tmp = re.split(_args_split_sep, args_text, 1)
            if len(tmp) < 2:
                raise _IncompleteArgsError
            args_text = tmp[1].lstrip()

        tmp = re.split(_args_split_sep, args_text, 1)
        if len(tmp) < 2:
            raise _IncompleteArgsError
        job_id_without_suffix, command_raw = tmp
        job_id = job_id_without_suffix + '_' + get_target(ctx_msg)
        command_list = []
        if multi:
            command_raw_list = command_raw.split('\n')
            for cmd_raw in command_raw_list:
                cmd_raw = cmd_raw.lstrip()
                if not cmd_raw:
                    continue
                tmp = re.split('|'.join(_command_args_start_flags), cmd_raw, 1)
                if len(tmp) < 2:
                    tmp.append('')
                command_list.append(tuple(tmp))
        else:
            command_raw = command_raw.lstrip()
            tmp = re.split('|'.join(_command_args_start_flags), command_raw, 1)
            if len(tmp) < 2:
                tmp.append('')
            command_list.append(tuple(tmp))

        job_args = {
            'job_id': job_id_without_suffix,
            'command_list': command_list,
            'ctx_msg': ctx_msg
        }
        job = _scheduler.add_job(_call_commands, kwargs=job_args, trigger='cron', **trigger_args,
                                 id=job_id, replace_existing=True, misfire_grace_time=30)
        _send_text('成功添加计划任务 ' + job_id_without_suffix, ctx_msg, internal)
        return job
    except _InvalidTriggerArgsError:
        _send_add_job_trigger_args_invalid_msg(ctx_msg, internal)
    except _IncompleteArgsError:
        _send_add_job_incomplete_args_msg(ctx_msg, internal)


@cr.register('remove_job', 'remove-job', 'remove')
@cr.restrict(full_command_only=True, group_admin_only=True)
@_check_target
def remove_job(args_text, ctx_msg, internal=False):
    job_id_without_suffix = args_text.strip()
    if not job_id_without_suffix:
        _send_text('请指定计划任务的 ID', ctx_msg, internal)
        return False
    job_id = job_id_without_suffix + '_' + get_target(ctx_msg)
    try:
        _scheduler.remove_job(job_id, 'default')
        _send_text('成功删除计划任务 ' + job_id_without_suffix, ctx_msg, internal)
        return True
    except JobLookupError:
        _send_text('没有找到计划任务 ' + job_id_without_suffix, ctx_msg, internal)
        return False


@cr.register('get_job', 'get-job', 'get')
@cr.restrict(full_command_only=True)
@_check_target
def get_job(args_text, ctx_msg, internal=False):
    job_id_without_suffix = args_text.strip()
    if not job_id_without_suffix:
        _send_text('请指定计划任务的 ID', ctx_msg, internal)
        return None
    job_id = job_id_without_suffix + '_' + get_target(ctx_msg)
    job = _scheduler.get_job(job_id, 'default')
    if internal:
        return job
    if not job:
        core.echo('没有找到该计划任务，请指定正确的计划任务 ID', ctx_msg, internal)
        return
    reply = '找到计划任务如下：\n'
    reply += 'ID：' + job_id_without_suffix + '\n'
    reply += '下次触发时间：\n%s\n' % job.next_run_time.strftime('%Y-%m-%d %H:%M')
    reply += '命令：\n'
    command_list = job.kwargs['command_list']
    reply += _convert_command_list_to_str(command_list)
    _send_text(reply, ctx_msg, internal)


@cr.register('list_jobs', 'list-jobs', 'list')
@cr.restrict(full_command_only=True)
@_check_target
def list_jobs(_, ctx_msg, internal=False):
    target = get_target(ctx_msg)
    job_id_suffix = '_' + target
    jobs = list(filter(lambda j: j.id.endswith(job_id_suffix), _scheduler.get_jobs('default')))
    if internal:
        return jobs

    for job in jobs:
        job_id = job.id[:-len(job_id_suffix)]
        command_list = job.kwargs['command_list']
        reply = 'ID：' + job_id + '\n'
        reply += '下次触发时间：\n%s\n' % job.next_run_time.strftime('%Y-%m-%d %H:%M')
        reply += '命令：\n'
        reply += _convert_command_list_to_str(command_list)
        _send_text(reply, ctx_msg, internal)
    if len(jobs):
        _send_text('以上', ctx_msg, internal)
    else:
        _send_text('还没有添加计划任务', ctx_msg, internal)


@cr.register('execute_job', 'execute-job', 'execute', 'exec', 'trigger', 'do')
@cr.restrict(full_command_only=True, group_admin_only=True)
@_check_target
def execute_job(args_text, ctx_msg, internal=False):
    job = get_job(args_text, ctx_msg, internal=True)
    if not job:
        core.echo('没有找到该计划任务，请指定正确的计划任务 ID', ctx_msg, internal)
        return
    job_id_suffix = '_' + get_target(ctx_msg)
    job_id = job.id[:-len(job_id_suffix)]
    _call_commands(job_id, job.kwargs['command_list'], job.kwargs['ctx_msg'], internal)


def _convert_command_list_to_str(command_list):
    s = ''
    if len(command_list) > 1:
        for c in command_list:
            s += c[0] + (' ' + c[1] if c[1] else '') + '\n'
        s = s.rstrip('\n')
    else:
        s = command_list[0][0] + ' ' + command_list[0][1]
    return s


def _send_text(text, ctx_msg, internal):
    if not internal:
        core.echo(text, ctx_msg)


def _send_fail_to_get_target_msg(ctx_msg, internal):
    _send_text(
        '无法获取 target，可能因为不支持当前消息类型（如，不支持微信群组消息）'
        '或由于延迟还没能加载到用户的固定 ID（如，微信号）',
        ctx_msg,
        internal
    )


def _send_add_job_help_msg(ctx_msg, internal):
    _send_text(
        '此为高级命令！如果你不知道自己在做什么，请不要使用此命令。\n\n'
        '使用方法：\n'
        '/scheduler.add_job options|cron [--multi] job_id command\n'
        '说明：\n'
        'options 和 cron 用来表示触发参数，有且只能有其一，格式分别如下：\n'
        'options：\n'
        '  -M 分，0 到 59\n'
        '  -H 时，0 到 23\n'
        '  -d 日，1 到 31\n'
        '  -m 月，1 到 12\n'
        '  -w 星期，0 到 6，其中 0 表示星期一，6 表示星期天\n'
        '  以上选项的值的表示法和下面的 cron 模式相同\n'
        'cron：\n'
        '  此模式和 Linux 的 crontab 文件的格式、顺序相同（除了星期是从 0 到 6），一共 5 个用空格隔开的参数\n'
        '\n'
        '剩下三个参数见下一条',
        ctx_msg,
        internal
    )
    _send_text(
        '--multi 为可选项，表示读取多条命令\n'
        'job_id 为必填项，允许使用符合正则 [_\-a-zA-Z0-9] 的字符，作为计划任务的唯一标识，如果指定重复的 ID，则会覆盖原先已有的\n'
        'command 为必填项，从 job_id 之后第一个非空白字符开始，如果加了 --multi 选项，则每行算一条命令，否则一直到消息结束算作一整条命令（注意这里的命令不要加 / 前缀）\n'
        '\n'
        '例 1：\n'
        '以下命令将添加计划在每天晚上 10 点推送当天的知乎日报，并发送一条鼓励的消息：\n'
        '/scheduler.add_job 0 22 * * * --multi zhihu-daily-job\n'
        'zhihu\n'
        'echo 今天又是很棒的一天哦！\n'
        '例 2：\n'
        '以下命令将每 5 分钟发送一条提示：\n'
        '/scheduler.add_job -M */5 tip-job echo 提示内容',
        ctx_msg,
        internal
    )


def _send_add_job_trigger_args_invalid_msg(ctx_msg, internal):
    _send_text(
        '触发参数的格式不正确\n'
        '如需帮助，请发送如下命令：\n'
        '/scheduler.add_job --help',
        ctx_msg,
        internal
    )


def _send_add_job_incomplete_args_msg(ctx_msg, internal):
    _send_text(
        '缺少必须的参数\n'
        '如需帮助，请发送如下命令：\n'
        '/scheduler.add_job --help',
        ctx_msg,
        internal
    )
