from typing import Dict, Any, Union, List

from aiocqhttp import CQHttp, Error as CQHttpError


def context_source(ctx: Dict[str, Any]) -> str:
    src = ''
    if ctx.get('group_id'):
        src += 'g%s' % ctx['group_id']
    elif ctx.get('discuss_id'):
        src += 'd%s' % ctx['discuss_id']
    if ctx.get('user_id'):
        src += 'p%s' % ctx['user_id']
    return src


async def send(bot: CQHttp, ctx: Dict[str, Any],
               message: Union[str, Dict[str, Any], List[Dict[str, Any]]],
               *, ignore_failure: bool = True) -> None:
    try:
        await bot.send(ctx, message)
    except CQHttpError:
        if not ignore_failure:
            raise
