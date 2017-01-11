"""
This filter intercepts messages that contains content not allowed and move text content to 'text' field.
"""

from filter import as_filter


@as_filter(priority=100)
def _filter(ctx_msg):
    msg_format = ctx_msg.get('format')
    if msg_format != 'text' and ctx_msg.get('type') != 'friend_message':
        return False
    if msg_format not in ('text', 'media'):
        return False
    if msg_format == 'text':
        # Directly use the text in content as the 'text'
        ctx_msg['text'] = ctx_msg.get('content')
    return True
