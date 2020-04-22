import hashlib
import random
from typing import Sequence, Callable, Any

from aiocqhttp.message import escape
from aiocqhttp import Event as CQEvent

from . import NoneBot
from .exceptions import CQHttpError
from .typing import Message_T, Expression_T


def context_id(event: CQEvent, *, mode: str = 'default',
               use_hash: bool = False) -> str:
    """
    Calculate a unique id representing the context of the given event.

    mode:
      default: one id for one context
      group: one id for one group or discuss
      user: one id for one user

    :param event: the event object
    :param mode: unique id mode: "default", "group", or "user"
    :param use_hash: use md5 to hash the id or not
    """
    ctx_id = ''
    if mode == 'default':
        if event.group_id:
            ctx_id = f'/group/{event.group_id}'
        elif event.discuss_id:
            ctx_id = f'/discuss/{event.discuss_id}'
        if event.user_id:
            ctx_id += f'/user/{event.user_id}'
    elif mode == 'group':
        if event.group_id:
            ctx_id = f'/group/{event.group_id}'
        elif event.discuss_id:
            ctx_id = f'/discuss/{event.discuss_id}'
        elif event.user_id:
            ctx_id = f'/user/{event.user_id}'
    elif mode == 'user':
        if event.user_id:
            ctx_id = f'/user/{event.user_id}'

    if ctx_id and use_hash:
        ctx_id = hashlib.md5(ctx_id.encode('ascii')).hexdigest()
    return ctx_id


async def send(bot: NoneBot,
               event: CQEvent,
               message: Message_T,
               *,
               ensure_private: bool = False,
               ignore_failure: bool = True,
               **kwargs) -> Any:
    """Send a message ignoring failure by default."""
    try:
        if ensure_private:
            event = event.copy()
            event['message_type'] = 'private'
        return await bot.send(event, message, **kwargs)
    except CQHttpError:
        if not ignore_failure:
            raise
        return None


def render_expression(expr: Expression_T,
                      *args,
                      escape_args: bool = True,
                      **kwargs) -> str:
    """
    Render an expression to message string.

    :param expr: expression to render
    :param escape_args: should escape arguments or not
    :param args: positional arguments used in str.format()
    :param kwargs: keyword arguments used in str.format()
    :return: the rendered message
    """
    if isinstance(expr, Callable):
        expr = expr(*args, **kwargs)
    elif isinstance(expr, Sequence) and not isinstance(expr, str):
        expr = random.choice(expr)
    if escape_args:
        return expr.format(
            *[escape(s) if isinstance(s, str) else s for s in args], **{
                k: escape(v) if isinstance(v, str) else v
                for k, v in kwargs.items()
            })
    return expr.format(*args, **kwargs)
