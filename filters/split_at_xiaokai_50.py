"""
This filter intercepts messages not intended to the bot and removes the beginning "@xxx".
"""

from filter import as_filter
from apiclient import client as api


@as_filter(priority=50)
def _split_at_xiaokai(ctx_msg):
    if ctx_msg.get('type') == 'group_message' or ctx_msg.get('type') == 'discuss_message':
        text = ctx_msg.get('text', '')
        if text.startswith('@'):
            my_group_nick = ctx_msg.get('receiver')
            if not my_group_nick:
                return False
            at_me = '@' + my_group_nick
            if not text.startswith(at_me):
                user_info = api.get_user_info().json()
                if not user_info:
                    return False
                my_nick = user_info.get('nick')
                if not my_nick:
                    return False
                at_me = '@' + my_nick
                if not text.startswith(at_me):
                    return False
            text = text[len(at_me):]
        else:
            # Not starts with '@'
            return False
        ctx_msg['text'] = text.lstrip()
    return True
