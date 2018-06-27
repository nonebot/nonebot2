from none.command import CommandSession, CommandGroup

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


@w.command('suggestion', aliases=('生活指数', '生活建议', '生活提示'))
async def suggestion(session: CommandSession):
    await session.send('suggestion')
