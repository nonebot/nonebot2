import hashlib

from . import NoneBot, expression
from .exceptions import CQHttpError
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
            ctx_id += f'/group/{ctx["group_id"]}'
        elif ctx.get('discuss_id'):
            ctx_id += f'/discuss/{ctx["discuss_id"]}'
        if ctx.get('user_id'):
            ctx_id += f'/user/{ctx["user_id"]}'
    elif mode == 'group':
        if ctx.get('group_id'):
            ctx_id += f'/group/{ctx["group_id"]}'
        elif ctx.get('discuss_id'):
            ctx_id += f'/discuss/{ctx["discuss_id"]}'
    elif mode == 'user':
        if ctx.get('user_id'):
            ctx_id += f'/user/{ctx["user_id"]}'

    if ctx_id and use_hash:
        ctx_id = hashlib.md5(ctx_id.encode('ascii')).hexdigest()
    return ctx_id


async def send(bot: NoneBot, ctx: Context_T, message: Message_T, *,
               ignore_failure: bool = True) -> None:
    """Send a message ignoring failure by default."""
    try:
        if ctx.get('post_type') == 'message':
            await bot.send(ctx, message)
        else:
            ctx = ctx.copy()
            if 'message' in ctx:
                del ctx['message']
            if 'group_id' in ctx:
                await bot.send_group_msg(**ctx, message=message)
            elif 'discuss_id' in ctx:
                await bot.send_discuss_msg(**ctx, message=message)
            elif 'user_id' in ctx:
                await bot.send_private_msg(**ctx, message=message)
    except CQHttpError:
        if not ignore_failure:
            raise


async def send_expr(bot: NoneBot, ctx: Context_T,
                    expr: Expression_T, **kwargs):
    """Sending a expression message ignoring failure by default."""
    return await send(bot, ctx, expression.render(expr, **kwargs))
