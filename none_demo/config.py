import re

from none.default_config import *

SECRET = 'abc'

SUPERUSERS = {1002647525}
COMMAND_START = {'', '/', '!', '／', '！', re.compile(r'^>+\s*')}
COMMAND_SEP = {'/', '.', re.compile(r'#|::?')}
