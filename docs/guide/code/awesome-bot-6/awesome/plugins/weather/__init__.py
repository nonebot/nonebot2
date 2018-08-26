from none import on_command, CommandSession
from none import on_natural_language, NLPSession, NLPResult
from jieba import posseg

from .data_source import get_weather_of_city


@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    weather_report = await get_weather_of_city(city)
    await session.send(weather_report)


@weather.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['city'] = stripped_arg


# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language(keywords=('天气',))
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg_text = session.msg_text.strip()
    # 对消息进行分词和词性标注
    words = posseg.lcut(stripped_msg_text)

    city = None
    # 遍历 posseg.lcut 返回的列表
    for word in words:
        # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
        if word.flag == 'ns':
            # ns 词性表示地名
            city = word.word

    # 返回处理结果，三个参数分别为置信度、命令名、命令会话的参数
    return NLPResult(90.0, 'weather', {'city': city})
