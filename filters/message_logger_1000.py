"""
This filter just log message to stdout.
"""

from filter import as_filter


@as_filter(priority=1000)
def _log_message(ctx_msg):
    log = ctx_msg.get('sender') or ctx_msg.get('sender_id') or '未知用户'
    if ctx_msg.get('msg_type') == 'group':
        log += '@' + ctx_msg.get('group') or ctx_msg.get('group_id') or '未知群组'
    if ctx_msg.get('msg_type') == 'discuss':
        log += '@' + ctx_msg.get('discuss') or ctx_msg.get('discuss_id') or '未知讨论组'
    log += ': ' + ctx_msg.get('content', '')
    print(log)
