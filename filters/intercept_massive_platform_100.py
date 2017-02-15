"""
This filter intercepts messages that are from massive platforms.
"""

from filter import as_filter


@as_filter(priority=100)
def _filter(ctx_msg):
    return not ctx_msg.get('is_massive_platform', False)
