import os
import requests

from command import CommandRegistry
from apiclient import client as api

__registry__ = cr = CommandRegistry()


@cr.register('echo', '重复', '跟我念')
def echo(args_text, ctx_msg, internal=False):
    if internal:
        return None
    else:
        return api.send_message(args_text, ctx_msg)


@cr.register('tuling123', 'chat', '聊天')
def tuling123(args_text, ctx_msg, internal=False):
    url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': os.environ.get('TURING123_API_KEY'),
        'info': args_text
    }
    if ctx_msg.get('sender_uid'):
        data['userid'] = ctx_msg.get('sender_uid')
    elif ctx_msg.get('sender_id'):
        data['userid'] = ctx_msg.get('sender_id').strip('@')[-32:]
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
    echo(reply, ctx_msg)


@cr.register('help', '帮助', '用法', '使用帮助', '使用指南', '使用说明', '使用方法', '怎么用')
def help(_, ctx_msg):
    echo(
        '你好！我是 CCZU 小开机器人，由常州大学开发者协会开发。\n'
        '我可以为你做一些简单的事情，如发送知乎日报内容、翻译一段文字等。\n'
        '下面是我现在能做的一些事情：\n\n'
        '(1)／查天气 常州\n'
        '(2)／翻译 こんにちは\n'
        '(3)／翻译到 英语 你好\n'
        '(4)／历史上的今天\n'
        '(5)／知乎日报\n'
        '(6)／记笔记 笔记内容\n'
        '(7)／查看所有笔记\n'
        '(8)／查百科 常州大学\n'
        '(9)／说个笑话\n'
        '(10)／聊天 你好啊\n\n'
        '把以上内容之一（包括斜杠，不包括序号，某些部分替换成你需要的内容）发给我，我就会按你的要求去做啦。\n'
        '上面只给出了 10 条功能，还有更多功能和使用方法，请查看 http://t.cn/RIr177e\n\n'
        '祝你使用愉快～',
        ctx_msg
    )
