import none
from none.command import Session


@none.on_command('weather', aliases=('天气',))
async def weather(session: Session):
    city = session.require_arg('city', prompt='你想知道哪个城市的天气呢？')
    other = session.require_arg('other', prompt='其他信息？')
    await session.send(f'你查询了{city}的天气，{other}')


@weather.args_parser
async def _(session: Session):
    if session.current_key:
        session.args[session.current_key] = session.current_arg.strip()
