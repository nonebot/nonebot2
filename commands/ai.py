import os
import requests

from command import CommandRegistry
from commands import core
from little_shit import get_source
from apiclient import client as api

__registry__ = cr = CommandRegistry()


@cr.register('tuling123', 'chat', '聊天')
def tuling123(args_text, ctx_msg, internal=False):
    url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': os.environ.get('TURING123_API_KEY'),
        'info': args_text,
        'userid': get_source(ctx_msg)
    }
    resp = requests.post(url, data=data)
    if resp.status_code == 200:
        json = resp.json()
        if internal:
            return json
        if int(json.get('code', 0)) == 100000:
            reply = json.get('text', '')
        else:
            # Is not text type
            reply = '腊鸡图灵机器人返回了一堆奇怪的东西，就不发出来了'
    else:
        if internal:
            return None
        reply = '腊鸡图灵机器人出问题了，先不管他，过会儿再玩他'
    core.echo(reply, ctx_msg)


@cr.register('xiaoice', '小冰')
def xiaoice(args_text, ctx_msg, internal=False):
    resp = api.wx_consult(account='xiaoice-ms', content=args_text)
    if resp:
        json = resp.json()
        if json and json.get('reply'):
            reply = json['reply']
            core.echo(reply, ctx_msg, internal)
            return reply
    return None
