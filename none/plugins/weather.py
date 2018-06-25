import none
from none.command import Session, CommandGroup
from none.expressions import weather as expr

w = CommandGroup('weather')


@w.command('weather', aliases=('天气', '天气预报'))
async def weather(session: Session):
    city = session.require_arg('city', prompt_expr=expr.WHICH_CITY)
    await session.send_expr(expr.REPORT, city=city)


@weather.args_parser
async def _(session: Session):
    if session.current_key:
        session.args[session.current_key] = session.current_arg.strip()


@w.command('suggestion', aliases=('生活指数', '生活建议', '生活提示'))
async def suggestion(session: Session):
    await session.send('suggestion')
