from collections import namedtuple
from typing import Dict, Any

from aiocqhttp import CQHttp

_nl_processors = set()


class NLProcessor:
    __slots__ = ('func', 'permission', 'only_to_me', 'keywords',
                 'precondition_func')


NLPResult = namedtuple('NLPResult', (
    'confidence',
    'cmd_name',
    'cmd_args',
))


async def handle_natural_language(bot: CQHttp, ctx: Dict[str, Any]) -> None:
    pass
