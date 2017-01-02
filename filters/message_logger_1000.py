"""
This filter just log message to stdout.
"""

from filter import as_filter


@as_filter(priority=1000)
def _log_message(ctx_msg):
    print(ctx_msg.get('sender', '')
          + (('@' + ctx_msg.get('group')) if ctx_msg.get('type') == 'group_message' else '')
          + (('@' + ctx_msg.get('discuss')) if ctx_msg.get('type') == 'discuss_message' else '')
          + ': ' + ctx_msg.get('content'))
