"""
This filter intercepts messages not intended to the bot and removes the beginning "@xxx".
"""

from filter import as_filter
from msg_src_adapter import get_adapter_by_ctx


@as_filter(priority=50)
def _split_at_xiaokai(ctx_msg):
    if ctx_msg.get('is_at_me'):
        # Directly return because it has been confirmed by previous processes
        return True

    if ctx_msg.get('msg_type') == 'group' or ctx_msg.get('msg_type') == 'discuss':
        text = ctx_msg.get('text', '')
        if text.startswith('@'):
            my_group_nick = ctx_msg.get('receiver')
            if not my_group_nick:
                return False
            at_me = '@' + my_group_nick
            if not text.startswith(at_me):
                user_info = get_adapter_by_ctx(ctx_msg).get_login_info(ctx_msg)
                my_nick = user_info.get('nickname')
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
