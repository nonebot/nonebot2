# 编写自然语言处理器

<!-- 本章将教你如何编写自己的自然语言处理器，使上一章的天气查询功能不再局限于固定格式的命令，而是能够处理自然的句子。

除此之外，还会教你如何单独使用自然语言处理器，而不必编写与之配套的命令。 -->

在上一章中我们编写了一个天气查询命令，但它还具有非常强的局限性，用户必须发送固定格式的消息，它才能理解，即使它可以交互式地询问用户要查询的城市，用户仍然需要记住命令的名字。

本章将会介绍如何让插件能够理解用户的自然语言消息，例如：

```
今天南京天气怎么样？
```

::: tip 提示
本章的完整代码可以在 [awesome-bot-3](https://github.com/richardchien/none-bot/tree/master/docs/guide/code/awesome-bot-3) 查看。
:::

## 调整项目结构

在开始下一步之前，首先对项目结构再做一个调整，以方便后面的代码编写。

到目前为止 `weather.py` 中只有三个函数，看起来还比较简单，不过当我们再往里面添加更多功能之后，它可能会变得比较杂乱。幸运的是，NoneBot 除了支持加载 `.py` 文件（Python 模块）形式的插件，还支持加载包含 `__init__.py` 的目录（Python 包）。

下面我们对 `weather` 插件做一个调整，将 `get_weather_of_city()` 提取到单独的模块中（这个函数在实际应用中可能比较长，并且可能需要多个函数组合）。

首先创建 `weather` 目录，并将原来 `weather.py` 中的代码移动到 `weather/__init__.py` 文件（如果你使用 PyCharm 或 IDEA + Python 插件，可以右击 `weather.py` 并选择 Refactor - Convert to Python Package），然后在 `weather` 目录中再创建 `data_source.py` 文件，将 `get_weather_of_city()` 函数移动进去。

经过这些步骤后，目录结构如下：

```
awesome-bot
├── awesome
│   └── plugins
│       └── weather
│           ├── __init__.py
│           └── data_source.py
├── bot.py
└── config.py
```

`weather/__init__.py` 内容如下：

```python
from none import on_command, CommandSession

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
```

`weather/data_source.py` 内容如下：

```python
async def get_weather_of_city(city: str) -> str:
    return f'{city}的天气是……'
```

## 编写雏形

在 `weather/__init__.py` 文件添加内容如下：

```python {2,23-29}
from none import on_command, CommandSession
from none import on_natural_language, NLPSession, NLPResult

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
    # 返回处理结果，3 个参数分别为置信度、命令名、命令会话的参数
    return NLPResult(90.0, 'weather', {})
```

代码中的注释已经进行了大部分解释，这里再详细介绍一下 `NLPResult` 这个类。

在 NoneBot 中，自然语言处理器的工作方式就是将用户的自然语言消息解析成一个命令和命令所需的参数，由于自然语言消息的模糊性，在解析时不可能完全确定用户的意图，因此还需要返回一个置信度作为这个命令的确定程度。

::: tip 提示
置信度的计算需要自然语言处理器的编写者进行恰当的设计，以确保各插件之间的功能不会互相冲突。
:::

在实际项目中，很多插件都会注册有自然语言处理器，其中每个都按照它的解析情况返回 `NLPResult` 对象，NoneBot 会将所有自然语言处理器返回的 `NLPResult` 对象按置信度排序，取置信度最高的结果中的命令来执行，`NLPResult` 的第三个参数（上面代码中的 `{}`）会被赋值给命令的 `session.args`（还记得上一章中用到这个属性吗）。

目前的代码中，直接根据关键词 `天气` 做出响应，无论消息其它部分是什么，只要包含关键词 `天气`，就会理解为 `weather` 命令。

现在运行 NoneBot，尝试向机器人发送任何包含 `天气` 二字的消息，例如：

```
今天天气怎么样？
```

一切正常的话，它会询问你要查询的城市，这表示它正确的进入了 `weather` 命令的会话中。

## 安装结巴分词

下面我们将允许用户在消息中直接给出要查询的城市，要做到这一点，我们需要能够对消息进行分词和词性标注，以判断哪个词是城市名称。

到这里是真正的自然语言处理的领域了，我们为了简单起见，使用 [结巴分词](https://github.com/fxsjy/jieba) 来进行词性标注。

使用如下命令安装结巴分词：

```bash
pip install jieba
```

::: tip 提示
如果你没有使用过结巴分词，建议先前往它的 [项目主页](https://github.com/fxsjy/jieba) 查看代码示例以了解基本用法。
:::

## 完善自然语言处理器

有了结巴分词之后，扩充 `weather/__init__.py` 如下：

```python {3,29-43}
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

    # 返回处理结果，3 个参数分别为置信度、命令名、命令会话的参数
    return NLPResult(90.0, 'weather', {'city': city})
```

我们使用结巴分词的 posseg 模块进行词性标注，然后找出第一个标记为 `ns`（表示地名，其它词性见 [ICTCLAS 汉语词性标注集](https://gist.github.com/luw2007/6016931#ictclas-%E6%B1%89%E8%AF%AD%E8%AF%8D%E6%80%A7%E6%A0%87%E6%B3%A8%E9%9B%86)）的词，赋值给 `city`，进而作为 `weather` 命令的参数传入 `NLPResult`。

现在运行 NoneBot，尝试向机器人分别发送下面两句话：

```
今天天气怎么样？
今天南京天气怎么样？
```

如果一切顺利，第一句它会问你要查询哪个城市，第二句会直接识别到城市。

## 更精确的自然语言理解

如果你是一位自然语言处理领域的爱好者或从业人员，你可以在 NoneBot 中很方便的将你的理论研究应用到实例中，在自然语言处理器中使用更高级的 NLP 技术，并且，可以通过增加命令的参数，将自然语言的理解更加细化，以向用户提供更加顺畅的使用体验。
