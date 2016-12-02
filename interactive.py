from cachetools import TTLCache as TTLDict


class _Session:
    __dict__ = ('cmd', 'state', 'data')

    def __init__(self, cmd):
        self.cmd = cmd
        self.state = 0
        self.data = {}


_sessions = TTLDict(maxsize=10000, ttl=5 * 60)


def get_session(source, cmd=None):
    if cmd:
        if source in _sessions and _sessions[source].cmd == cmd:
            # It's already in a session of this command
            return _sessions[source]
        sess = _Session(cmd)
        _sessions[source] = sess
        return sess
    else:
        return _sessions.get(source)


def has_session(source, cmd=None):
    return source in _sessions and (not cmd or _sessions[source].cmd == cmd)


def remove_session(source, cmd=None):
    if source in _sessions:
        if not cmd or _sessions[source].cmd == cmd:
            del _sessions[source]
