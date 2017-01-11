"""
This filter unitize context messages from different platform.
"""

from filter import as_filter


@as_filter(priority=10000)
def _unitize(ctx_msg):
    if 'group_uid' in ctx_msg:
        ctx_msg['group_uid'] = str(ctx_msg['group_uid'])
    if 'sender_uid' in ctx_msg:
        ctx_msg['sender_uid'] = str(ctx_msg['sender_uid'])
    if 'sender_id' in ctx_msg:
        ctx_msg['sender_id'] = str(ctx_msg['sender_id'])
    if 'discuss_id' in ctx_msg:
        ctx_msg['discuss_id'] = str(ctx_msg['discuss_id'])
    if 'group_id' in ctx_msg:
        ctx_msg['group_id'] = str(ctx_msg['group_id'])
    if 'id' in ctx_msg:
        ctx_msg['id'] = str(ctx_msg['id'])

    if ctx_msg.get('via') == 'qq' and not ctx_msg.get('format'):
        # All QQ messages that can be received are text
        ctx_msg['format'] = 'text'
