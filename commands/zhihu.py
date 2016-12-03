import re
from datetime import date, timedelta

import requests

from command import CommandRegistry
from commands import core
from commands import scheduler
from interactive import *
from little_shit import SkipException, get_source

__registry__ = cr = CommandRegistry()


@cr.register('zhihu-daily', 'zhihu', '知乎日报')
def zhihu_daily(args_text, ctx_msg):
    arg = args_text.strip()
    reply = None
    try:
        if not arg:
            sub_url = '/latest'
        else:
            m = re.match('(\d{4})-(\d{2})-(\d{2})', arg)
            if m and ''.join(m.groups()) >= '20130519':
                thedate = date(year=int(m.group(1)), month=int(m.group(2)), day=int(m.group(3)))
                sub_url = '/before/' + (thedate + timedelta(days=1)).strftime('%Y%m%d')
            else:
                reply = '命令格式错误，正确的命令格式：\n' \
                        '/zhihu\n' \
                        '或\n' \
                        '/zhihu 2016-11-29\n' \
                        '注意如果指定日期，格式一定要对，且日期需在 2013-05-19 之后（这一天知乎日报诞生）。'
                raise SkipException
        full_url = 'https://news-at.zhihu.com/api/4/news' + sub_url
        resp = requests.get(
            full_url,
            headers={
                'Host': 'news-at.zhihu.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36'
                              ' (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
            }
        )
        if resp.status_code == 200:
            json = resp.json()
            if 'stories' not in json:
                reply = '获取知乎日报数据失败，知乎返回了一堆迷之数据'
                raise SkipException
            reply = ('今天' if sub_url == '/latest' else '这天') + '的知乎日报内容如下：'
            core.echo(reply, ctx_msg)
            step = 6  # Send 8 items per time
            items = list(reversed(json.get('stories')))
            for start in range(0, len(items), step):
                reply = ''
                for item in items[start:min(start + step, len(items))]:
                    reply += item.get('title') + '\n' + \
                             'https://daily.zhihu.com/story/' + str(item.get('id')) + '\n\n'
                reply = reply.rstrip()
                core.echo(reply, ctx_msg)
            return
        else:
            reply = '获取知乎日报数据失败，可能知乎服务器又宕机了（（'
            raise SkipException
    except SkipException:
        reply = reply if reply else '发生了未知错误……'
    core.echo(reply, ctx_msg)


_cmd_subscribe = 'zhihu.subscribe'
_scheduler_job_id = _cmd_subscribe


@cr.register('订阅知乎日报')
@cr.register('subscribe', hidden=True)
@cr.restrict(group_admin_only=True)
def subscribe(args_text, ctx_msg, allow_interactive=True):
    arg = args_text.strip()
    source = get_source(ctx_msg)
    if allow_interactive and (not arg or has_session(source, _cmd_subscribe)):
        # Be interactive
        return _subscribe_interactively(args_text, ctx_msg, source)

    force = False
    if arg.startswith('-f '):
        force = True
        arg = arg.split(' ', 1)[1].strip()
    reply = None
    try:
        m = re.match('([0-1]\d|[2][0-3])(?::|：)?([0-5]\d)', arg)
        if m:
            job = scheduler.get_job(_scheduler_job_id, ctx_msg, internal=True)
            if job and not force:
                reply = '已经订阅过了哦～\n' \
                        + '下次推送时间：\n' \
                        + job.next_run_time.strftime('%Y-%m-%d %H:%M') + '\n' \
                        + '如果需要更改推送时间，请先取消订阅再重新订阅，' \
                        + '或在订阅命令的时间参数前面加 -f 来强制更新推送时间'
                raise SkipException
            job = scheduler.add_job(
                '-M %s -H %s %s zhihu.zhihu-daily' % (m.group(2), m.group(1), _scheduler_job_id),
                ctx_msg,
                internal=True
            )
            if job:
                # Succeeded to add a job
                reply = '订阅成功，我会在每天 %s 推送哦～' % ':'.join((m.group(1), m.group(2)))
            else:
                reply = '订阅失败，可能后台出了点问题呢～'
        else:
            reply = '命令格式错误，正确的命令格式：\n' \
                    '/zhihu.subscribe\n' \
                    '或\n' \
                    '/zhihu.subscribe [-f] 20:30\n'
    except SkipException:
        reply = reply if reply else '发生了未知错误……'
    core.echo(reply, ctx_msg)


@cr.register('取消订阅知乎日报')
@cr.register('unsubscribe', hidden=True)
@cr.restrict(group_admin_only=True)
def unsubscribe(_, ctx_msg):
    if scheduler.remove_job(_scheduler_job_id, ctx_msg, internal=True):
        core.echo('取消订阅成功～', ctx_msg)
    else:
        core.echo('还没有订阅过哦～', ctx_msg)


_state_machines = {}


def _subscribe_interactively(args_text, ctx_msg, source):
    def confirm_override(s, a, c):
        job = scheduler.get_job(_scheduler_job_id, c, internal=True)
        if job:
            core.echo('先前已经订阅过了哦～\n'
                      + '下次推送时间：\n'
                      + job.next_run_time.strftime('%Y-%m-%d %H:%M') + '\n'
                      + '要更改推送时间吗？\n'
                      + '回复 1 继续，回复 0 放弃', c)
            s.data['need_confirm'] = True
        else:
            s.data['need_confirm'] = False
            wait_for_time(s, a, c)
        s.state += 1

    def wait_for_time(s, a, c):
        if s.data['need_confirm']:
            if a.strip() != '1':
                # Cancel
                core.echo('已放弃更改～', c)
                return True
        core.echo('请发送想要获取推送的时间（格式如 20:05）：', c)
        s.state += 1

    def save(s, a, c):
        subscribe('-f ' + a, c, allow_interactive=False)
        return True

    if _cmd_subscribe not in _state_machines:
        _state_machines[_cmd_subscribe] = (
            confirm_override,  # 0
            wait_for_time,  # 1
            save  # 2
        )

    sess = get_session(source, _cmd_subscribe)
    if _state_machines[_cmd_subscribe][sess.state](sess, args_text, ctx_msg):
        # Done
        remove_session(source, _cmd_subscribe)
