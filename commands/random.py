import re
import random
import string

from command import CommandRegistry, split_arguments
from commands import core

__registry__ = cr = CommandRegistry()


@cr.register('随机数')
@cr.register('number', hidden=True)
@split_arguments()
def number(_, ctx_msg, internal=False, argv=None):
    if len(argv) == 0 or not re.match('x\d+', argv[-1]):
        n = 1
    else:
        n = max(1, int(argv[-1][1:]))
        argv = argv[:-1]

    if len(argv) > 2 or any((not re.match('-?\d+', num) for num in argv)):
        core.echo('参数有错误哦～\n正确的使用方法（主要看参数，你的命令是对的～）：\n\n'
                  '/random.number\n'
                  '/random.number x5\n'
                  '/random.number 100\n'
                  '/random.number 100 x10\n'
                  '/random.number 50 100\n'
                  '/random.number 50 100 x3',
                  ctx_msg, internal)
        return

    if len(argv) == 1:
        argv.append(1)

    start, end = (int(argv[0]), int(argv[1])) if len(argv) == 2 else (None, None)
    start, end = (min(start, end), max(start, end)) if start is not None else (start, end)

    result = []

    for _ in range(n):
        result.append(random.randint(start, end) if start is not None else random.random())

    core.echo(', '.join(str(num) for num in result), ctx_msg, internal)
    return result


@cr.register('随机字符')
@cr.register('char', hidden=True)
@split_arguments()
def char(_, ctx_msg, internal=False, argv=None):
    if len(argv) > 2 or (len(argv) == 2 and not re.match('x\d+', argv[-1])):
        core.echo('参数有错误哦～\n正确的使用方法（主要看参数，你的命令是对的～）：\n\n'
                  '/random.char\n'
                  '/random.char x5\n'
                  '/random.char ABCDEFG\n'
                  '/random.char ABCDEFG x10\n',
                  ctx_msg, internal)
        return

    chars = string.ascii_letters + string.digits
    size = 1
    if len(argv) and re.match('x\d+', argv[-1]):
        size = max(1, int(argv[-1][1:]))
        argv = argv[:-1]
    if len(argv):
        chars = argv[0]

    result = ''.join(random.choice(chars) for _ in range(size))
    core.echo(result, ctx_msg, internal)
    return result


@cr.register('随机化')
@cr.register('shuffle', hidden=True)
@split_arguments()
def char(_, ctx_msg, internal=False, argv=None):
    if len(argv) == 0:
        core.echo('请传入正确的参数哦～', ctx_msg, internal)
        return argv
    random.shuffle(argv)
    core.echo(', '.join(argv), ctx_msg, internal)
    return argv
