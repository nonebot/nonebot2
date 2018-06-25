import none
from none.command import Session
from none.helpers import send


@none.on_command('weather', aliases=('天气',))
async def weather(bot, session: Session):
    city = session.require_arg('city', prompt='你想知道哪个城市的天气呢？')
    other = session.require_arg('other')
    await send(bot, session.ctx, f'你查询了{city}的天气，{other}')


@weather.args_parser
def _(session: Session):
    if session.current_key:
        session.args[session.current_key] = session.current_arg.strip()
