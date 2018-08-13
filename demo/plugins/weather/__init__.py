from none import (
    CommandSession, CommandGroup,
    on_natural_language, NLPSession, NLPResult
)

from . import expressions as expr

w = CommandGroup('weather')


@w.command('weather', aliases=('天气', '天气预报'))
async def weather(session: CommandSession):
    city = session.get('city', prompt_expr=expr.WHICH_CITY)
    await session.send_expr(expr.REPORT, city=city)


@weather.args_parser
async def _(session: CommandSession):
    striped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = striped_arg
    elif striped_arg:
        session.args['city'] = striped_arg


@on_natural_language({'天气', '雨', '雪', '晴', '阴'}, only_to_me=False)
async def _(session: NLPSession):
    if not ('?' in session.msg_text or '？' in session.msg_text):
        return None
    return NLPResult(90.0, ('weather', 'weather'), {})


@w.command('suggestion', aliases=('生活指数', '生活建议', '生活提示'))
async def suggestion(session: CommandSession):
    await session.send('suggestion')
