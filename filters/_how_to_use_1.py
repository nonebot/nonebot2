import re

from filter import as_filter
from commands import core


@as_filter(priority=1)
def _print_help_message(ctx_msg):
    a = ['help', '怎么用', '怎么用啊', '你好', '你好啊', '你好呀', '帮助',
         '用法', '使用帮助', '使用指南', '使用说明', '使用方法',
         '你能做什么', '你能做些什么', '你会做什么', '你会做些什么',
         '你可以做什么', '你可以做些什么']
    text = ctx_msg.get('text', '').strip()
    sender = ctx_msg.get('sender', '')
    if text in a or re.match('^' + sender + '刚刚把你添加到通讯录，现在可以开始聊天了。$', text):
        core.help('', ctx_msg)
        return False
    elif re.match('^你已添加了' + sender + '，现在可以开始聊天了。$', text):
        return False
    return True
