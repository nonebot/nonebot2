"""
This filter intercepts messages that contains content not allowed and move text content to 'text' field.
"""

from filter import add_filter


def _filter(ctx_msg):
    if ctx_msg.get('via') == 'wx':
        msg_format = ctx_msg.get('format')
        if msg_format != 'text' and ctx_msg.get('type') != 'friend_message':
            return False
        if msg_format not in ('text', 'media'):
            return False
        if msg_format == 'text':
            ctx_msg['text'] = ctx_msg.get('content')
    elif ctx_msg.get('via') == 'qq':
        ctx_msg['text'] = ctx_msg.get('content')
    return True


add_filter(_filter, 100)
