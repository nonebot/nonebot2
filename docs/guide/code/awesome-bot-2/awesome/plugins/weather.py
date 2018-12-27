from nonebot import on_command, CommandSession


# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    # 获取城市的天气预报
    weather_report = await get_weather_of_city(city)
    # 向用户发送天气预报
    await session.send(weather_report)


# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        # 如果当前正在向用户询问更多信息（本例中只有可能是要查询的城市），则直接赋值
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        # 如果当前没有在询问，但用户已经发送了内容，则理解为要查询的城市
        # 这种情况通常是用户直接将城市名跟在命令名后面，作为参数传入
        session.args['city'] = stripped_arg


async def get_weather_of_city(city: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    return f'{city}的天气是……'
