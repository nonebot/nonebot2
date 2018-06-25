import none
from none.command import Session
from none.expressions import weather as expr


@none.on_command(('weather', 'weather'), aliases=('天气', '天气预报'))
async def weather(session: Session):
    city = session.require_arg('city', prompt_expr=expr.WHICH_CITY)
    await session.send_expr(expr.REPORT, city=city)


@weather.args_parser
async def _(session: Session):
    if session.current_key:
        session.args[session.current_key] = session.current_arg.strip()


@none.on_command(('weather', 'suggestion'),
                 aliases=('生活指数', '生活建议', '生活提示'))
async def suggestion(session: Session):
    await session.send('suggestion')
