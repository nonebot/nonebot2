"""
Default configurations.

Any derived configurations must import everything from this module
at the very beginning of their code, and then set their own value
to override the default one.

For example:

>>> from nonebot.default_config import *
>>> PORT = 9090
>>> DEBUG = False
>>> SUPERUSERS.add(123456)
>>> NICKNAME = '小明'
"""

from datetime import timedelta
from typing import Container, Union, Iterable, Pattern, Optional, Dict, Any

from .typing import Expression_T

API_ROOT: str = ''
ACCESS_TOKEN: str = ''
SECRET: str = ''
HOST: str = '127.0.0.1'
PORT: int = 8080
DEBUG: bool = True

SUPERUSERS: Container[int] = set()
NICKNAME: Union[str, Iterable[str]] = ''
COMMAND_START: Iterable[Union[str, Pattern]] = {'/', '!', '／', '！'}
COMMAND_SEP: Iterable[Union[str, Pattern]] = {'/', '.'}
SESSION_EXPIRE_TIMEOUT: Optional[timedelta] = timedelta(minutes=5)
SESSION_RUN_TIMEOUT: Optional[timedelta] = None
SESSION_RUNNING_EXPRESSION: Expression_T = '您有命令正在执行，请稍后再试'
SHORT_MESSAGE_MAX_LENGTH: int = 50

APSCHEDULER_CONFIG: Dict[str, Any] = {
    'apscheduler.timezone': 'Asia/Shanghai'
}
