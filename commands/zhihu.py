import re
from datetime import date, timedelta

import requests

from little_shit import SkipException
from command import CommandRegistry
from commands import core

__registry__ = cr = CommandRegistry()


@cr.register('zhihu', 'zhihu-daily', '知乎日报')
def zhihu_daily(args_text, ctx_msg):
    param = args_text.strip()
    reply = None
    try:
        if not param:
            sub_url = '/latest'
        elif re.match('\d{8}', param) and param >= '20130519':
            thedate = date(year=int(param[:4]), month=int(param[4:6]), day=int(param[6:]))
            sub_url = '/before/' + (thedate + timedelta(days=1)).strftime('%Y%m%d')
        else:
            reply = '命令格式错误，正确的命令格式：\n' \
                    '/zhihu\n' \
                    '或\n' \
                    '/zhihu 20161129\n' \
                    '注意如果指定日期，格式一定要对，且日期需在 20130519 之后。'
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
        pass
    core.echo(reply, ctx_msg)
