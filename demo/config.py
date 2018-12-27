import re

from nonebot.default_config import *

HOST = '0.0.0.0'
SECRET = 'abc'

SUPERUSERS = {1002647525}
NICKNAME = {'奶茶', '小奶茶'}
COMMAND_START = {'', '/', '!', '／', '！', re.compile(r'^>+\s*')}
COMMAND_SEP = {'/', '.', re.compile(r'#|::?')}
