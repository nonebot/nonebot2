from typing import Dict, Any


def context_source(ctx: Dict[str, Any]) -> str:
    src = ''
    if ctx.get('group_id'):
        src += 'g%s' % ctx['group_id']
    elif ctx.get('discuss_id'):
        src += 'd%s' % ctx['discuss_id']
    if ctx.get('user_id'):
        src += 'p%s' % ctx['user_id']
    return src
