"""
This filter intercepts messages not intended to the bot and removes the beginning "@xxx".
"""

from filter import add_filter


def _split_at_xiaokai(ctx_msg):
    if ctx_msg.get('type') == 'group_message' or ctx_msg.get('type') == 'discuss_message':
        text = ctx_msg.get('text', '')
        if text.startswith('@'):
            my_group_nick = ctx_msg.get('receiver')
            if not my_group_nick:
                return False
            at_me = '@' + my_group_nick
            if not text.startswith(at_me):
                return False
            text = text[len(at_me):]
        else:
            # Not starts with '@'
            return False
        ctx_msg['text'] = text.lstrip()
    return True


add_filter(_split_at_xiaokai, priority=50)
