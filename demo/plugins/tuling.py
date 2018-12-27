from nonebot import (
    on_command, CommandSession,
    on_natural_language, NLPSession, NLPResult
)


@on_command('tuling', aliases=('聊天', '对话'))
async def tuling(session: CommandSession):
    message = session.get('message', prompt='我已经准备好啦，来跟我聊天吧~')

    finish = message in ('结束', '拜拜', '再见')
    if finish:
        session.finish('拜拜啦，你忙吧，下次想聊天随时找我哦~')
        return

    # call tuling api
    reply = f'你说了：{message}'

    one_time = session.get_optional('one_time', False)
    if one_time:
        session.finish(reply)
    else:
        session.pause(reply)


@tuling.args_parser
async def _(session: CommandSession):
    if session.current_key == 'message':
        session.args[session.current_key] = session.current_arg_text.strip()


@on_natural_language
async def _(session: NLPSession):
    return NLPResult(60.0, 'tuling', {
        'message': session.msg,
        'one_time': True
    })
