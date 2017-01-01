from filter import add_filter
from commands import core


def _print_help_message(ctx_msg):
    a = ['help', '怎么用', '怎么用啊', '你好', '你好啊', '帮助',
         '用法', '使用帮助', '使用指南', '使用说明', '使用方法',
         '你能做什么', '你能做些什么', '你会做什么', '你会做些什么',
         '你可以做什么', '你可以做些什么']
    if ctx_msg.get('text', '').strip() in a:
        core.help('', ctx_msg)
        return False
    return True


add_filter(_print_help_message, priority=1)
