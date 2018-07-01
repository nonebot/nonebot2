from none import CommandSession, CommandGroup

from . import expressions as expr

w = CommandGroup('weather')


@w.command('weather', aliases=('天气', '天气预报'))
async def weather(session: CommandSession):
    city = session.require_arg('city', prompt_expr=expr.WHICH_CITY)
    await session.send_expr(expr.REPORT, city=city)


@weather.args_parser
async def _(session: CommandSession):
    if session.current_key:
        session.args[session.current_key] = session.current_arg_text.strip()


# @on_natural_language(keywords={'天气', '雨', '雪', '晴', '阴', '多云', '冰雹'},
#                      only_to_me=False)
# async def weather_nlp(session: NaturalLanguageSession):
#     return NLPResult(89.5, ('weather', 'weather'), {'city': '南京'})
#
#
# @weather_nlp.condition
# async def _(session: NaturalLanguageSession):
#     keywords = {'天气', '雨', '雪', '晴', '阴', '多云', '冰雹'}
#     for kw in keywords:
#         if kw in session.text:
#             keyword_hit = True
#             break
#     else:
#         keyword_hit = False
#     if session.ctx['to_me'] and keyword_hit:
#         return True
#     return False


@w.command('suggestion', aliases=('生活指数', '生活建议', '生活提示'))
async def suggestion(session: CommandSession):
    await session.send('suggestion')
