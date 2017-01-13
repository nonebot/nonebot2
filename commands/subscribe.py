import re
from datetime import datetime

from command import CommandRegistry, split_arguments
from commands import core, scheduler
from interactive import *
from little_shit import get_source, check_target

__registry__ = cr = CommandRegistry()

_cmd_subscribe = 'subscribe.subscribe'
_scheduler_job_id_prefix = _cmd_subscribe + '_'


@cr.register('subscribe', '订阅')
@cr.restrict(group_admin_only=True)
@split_arguments(maxsplit=1)
@check_target
def subscribe(args_text, ctx_msg, argv=None, internal=False, allow_interactive=True):
    source = get_source(ctx_msg)
    if not internal and allow_interactive and has_session(source, _cmd_subscribe):
        # Already in a session, no need to pass in data,
        # because the interactive version of this command will take care of it
        return _subscribe_interactively(args_text, ctx_msg, source, None)

    data = {}
    if argv:
        m = re.match('([0-1]\d|[2][0-3])(?::|：)?([0-5]\d)', argv[0])
        if not m:
            # Got command but no time
            data['command'] = args_text
        else:
            # Got time
            data['hour'], data['minute'] = m.group(1), m.group(2)
            if len(argv) == 2:
                # Got command
                data['command'] = argv[1]

    if not internal and allow_interactive:
        if data.keys() != {'command', 'hour', 'minute'}:
            # First visit and data is not enough
            return _subscribe_interactively(args_text, ctx_msg, source, data)

    # Got both time and command, do the job!
    hour, minute = data['hour'], data['minute']
    command = data['command']
    job = scheduler.add_job(
        '-H %s -M %s %s %s' % (hour, minute, _scheduler_job_id_prefix + str(int(datetime.now().timestamp())), command),
        ctx_msg, internal=True
    )
    if internal:
        return job
    if job:
        # Succeeded to add a job
        reply = '订阅成功，我会在每天 %s 推送哦～' % ':'.join((hour, minute))
    else:
        reply = '订阅失败，可能后台出了点小问题～'

    core.echo(reply, ctx_msg, internal)


@cr.register('subscribe_list', 'subscribe-list', '订阅列表', '查看订阅', '查看所有订阅', '所有订阅')
@cr.restrict(group_admin_only=True)
@check_target
def subscribe_list(_, ctx_msg, internal=False):
    jobs = sorted(filter(
        lambda j: j.id.startswith(_scheduler_job_id_prefix),
        scheduler.list_jobs('', ctx_msg, internal=True)
    ), key=lambda j: j.id)

    if internal:
        return jobs

    if not jobs:
        core.echo('暂时还没有订阅哦～', ctx_msg)
        return

    for index, job in enumerate(jobs):
        command_list = job.kwargs['command_list']
        reply = 'ID：' + job.id[len(_scheduler_job_id_prefix):] + '\n'
        reply += '下次推送时间：\n%s\n' % job.next_run_time.strftime('%Y-%m-%d %H:%M')
        reply += '命令：\n'
        reply += scheduler.convert_command_list_to_str(command_list)
        core.echo(reply, ctx_msg)
    core.echo('以上～', ctx_msg)


@cr.register('unsubscribe', '取消订阅')
@cr.restrict(group_admin_only=True)
@split_arguments()
@check_target
def unsubscribe(_, ctx_msg, argv=None, internal=False):
    if not argv:
        core.echo('请在命令名后指定要取消订阅的 ID（多个 ID、ID 和命令名之间用空格隔开）哦～\n\n'
                  '你可以通过「查看所有订阅」命令来查看所有订阅项目的 ID', ctx_msg, internal)
        return

    result = []
    for job_id_without_prefix in argv:
        result.append(scheduler.remove_job(_scheduler_job_id_prefix + job_id_without_prefix, ctx_msg, internal=True))

    if internal:
        return result[0] if len(result) == 1 else result

    if all(result):
        core.echo('取消订阅成功～', ctx_msg, internal)
    else:
        core.echo('可能有订阅 ID 没有找到，请使用「查看所有订阅」命令来检查哦～',
                  ctx_msg, internal)


def _subscribe_interactively(args_text, ctx_msg, source, data):
    sess = get_session(source, _cmd_subscribe)
    if data:
        sess.data.update(data)

    state_command = 1
    state_time = 2
    state_finish = -1
    if sess.state == state_command:
        if not args_text.strip():
            core.echo('你输入的命令不正确，请重新发送订阅命令哦～', ctx_msg)
            sess.state = state_finish
        else:
            sess.data['command'] = args_text
    elif sess.state == state_time:
        m = re.match('([0-1]\d|[2][0-3])(?::|：)?([0-5]\d)', args_text.strip())
        if not m:
            core.echo('你输入的时间格式不正确，请重新发送订阅命令哦～', ctx_msg)
            sess.state = state_finish
        else:
            sess.data['hour'], sess.data['minute'] = m.group(1), m.group(2)

    if sess.state == state_finish:
        remove_session(source, _cmd_subscribe)
        return

    if 'command' not in sess.data:
        # Ask for command
        core.echo(
            '请输入你需要订阅的命令（包括所需的参数），不需要加开头的斜杠哦～\n\n'
            '例如（序号后的）：\n'
            '(1) 天气 南京\n'
            '(2) 知乎日报\n'
            '(3) 历史上的今天',
            ctx_msg
        )
        sess.state = state_command
        return

    if 'hour' not in sess.data or 'minute' not in sess.data:
        # Ask for time
        core.echo('请输入你需要推送的时间，格式如 22:00', ctx_msg)
        sess.state = state_time
        return

    subscribe(
        '', ctx_msg,
        argv=[':'.join((sess.data['hour'], sess.data['minute'])), sess.data['command']],
        allow_interactive=False
    )
    remove_session(source, _cmd_subscribe)
