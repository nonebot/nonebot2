class BlockedException(Exception):
    """Block a message from further handling"""
    pass


class RejectedException(Exception):
    """Reject a message and return current handler back"""
    pass
