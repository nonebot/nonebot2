from none import on_natural_language, NLPSession, NLPResult

_last_session = None


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    if session.ctx.get('group_id') != 672076603:
        return None

    global _last_session
    result = None
    if _last_session and \
            _last_session.ctx['user_id'] != session.ctx['user_id'] and \
            _last_session.msg == session.msg:
        result = NLPResult(61.0, 'echo', {'message': _last_session.msg})
        _last_session = None
    else:
        _last_session = session
    return result
