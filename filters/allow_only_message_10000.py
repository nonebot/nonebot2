"""
This filter intercepts all post data except ones of which 'post_type' is 'message'.
"""

from filter import as_filter


@as_filter(priority=10000)
def _filter(ctx_msg):
    return ctx_msg.get('post_type') == 'message'
