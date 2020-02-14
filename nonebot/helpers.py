import hashlib
import random
from typing import Sequence, Callable, Any

from . import NoneBot
from .exceptions import CQHttpError
from .message import escape
from .typing import Context_T, Message_T, Expression_T


def context_id(ctx: Context_T, *,
               mode: str = 'default', use_hash: bool = False) -> str:
    """
    Calculate a unique id representing the current context.

    mode:
      default: one id for one context
      group: one id for one group or discuss
      user: one id for one user

    :param ctx: the context dict
    :param mode: unique id mode: "default", "group", or "user"
    :param use_hash: use md5 to hash the id or not
    """
    ctx_id = ''
    if mode == 'default':
        if ctx.get('group_id'):
            ctx_id = f'/group/{ctx["group_id"]}'
        elif ctx.get('discuss_id'):
            ctx_id = f'/discuss/{ctx["discuss_id"]}'
        if ctx.get('user_id'):
            ctx_id += f'/user/{ctx["user_id"]}'
    elif mode == 'group':
        if ctx.get('group_id'):
            ctx_id = f'/group/{ctx["group_id"]}'
        elif ctx.get('discuss_id'):
            ctx_id = f'/discuss/{ctx["discuss_id"]}'
        elif ctx.get('user_id'):
            ctx_id = f'/user/{ctx["user_id"]}'
    elif mode == 'user':
        if ctx.get('user_id'):
            ctx_id = f'/user/{ctx["user_id"]}'

    if ctx_id and use_hash:
        ctx_id = hashlib.md5(ctx_id.encode('ascii')).hexdigest()
    return ctx_id


async def send(bot: NoneBot, ctx: Context_T,
               message: Message_T, *,
               ensure_private: bool = False,
               ignore_failure: bool = True,
               **kwargs) -> Any:
    """Send a message ignoring failure by default."""
    try:
        if ensure_private:
            ctx = ctx.copy()
            ctx['message_type'] = 'private'
        return await bot.send(ctx, message, **kwargs)
    except CQHttpError:
        if not ignore_failure:
            raise
        return None


def render_expression(expr: Expression_T, *args,
                      escape_args: bool = True, **kwargs) -> str:
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
            *[escape(s) if isinstance(s, str) else s for s in args],
            **{k: escape(v) if isinstance(v, str) else v
               for k, v in kwargs.items()}
        )
    return expr.format(*args, **kwargs)
