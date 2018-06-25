from typing import Dict, Any


def context_source(ctx: Dict[str, Any]) -> str:
    src = ''
    if ctx.get('group_id'):
        src += f'/group/{ctx["group_id"]}'
    elif ctx.get('discuss_id'):
        src += f'/discuss/{ctx["discuss_id"]}'
    if ctx.get('user_id'):
        src += f'/user/{ctx["user_id"]}'
    return src
