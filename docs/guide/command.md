# 编写命令

本章将以一个天气查询插件为例，教你如何编写自己的命令。

:::tip 提示
本章的完整代码可以在 [awesome-bot-2](https://github.com/richardchien/nonebot/tree/master/docs/guide/code/awesome-bot-2) 查看。
:::

## 创建插件目录

首先我们需要创建一个目录来存放插件，这个目录需要满足一些条件才能作为插件目录，首先，我们的代码能够比较容易访问到它，其次，它必须是一个能够以 Python 模块形式导入的路径（后面解释为什么），一个比较好的位置是项目目录中的 `awesome/plugins/`，创建好之后，我们的 `awesome-bot` 项目的目录结构如下：

```
awesome-bot
├── awesome
│   └── plugins
├── bot.py
└── config.py
```

接着在 `plugins` 目录中新建一个名为 `weather.py` 的 Python 文件，暂时留空，此时目录结构如下：

```
awesome-bot
├── awesome
│   └── plugins
│       └── weather.py
├── bot.py
└── config.py
```

## 加载插件

现在我们的插件目录已经有了一个空的 `weather.py`，实际上它已经可以被称为一个插件了，尽管它还什么都没做。下面我们来让 NoneBot 加载这个插件，修改 `bot.py` 如下：

```python {1,9-12}
from os import path

import nonebot

import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'awesome', 'plugins'),
        'awesome.plugins'
    )
    nonebot.run()
```

这里的重点在于 `nonebot.load_plugins()` 函数的两个参数。第一个参数是插件目录的路径，这里根据 `bot.py` 的所在路径和相对路径拼接得到；第二个参数是导入插件模块时使用的模块名前缀，这个前缀要求必须是一个当前 Python 解释器可以导入的模块前缀，NoneBot 会在它后面加上插件的模块名共同组成完整的模块名来让解释器导入，因此这里我们传入 `awesome.plugins`，当运行 `bot.py` 的时候，Python 解释器就能够正确导入 `awesome.plugins.weather` 这个插件模块了。

尝试运行 `python bot.py`，可以看到日志输出了类似如下内容：

```
[2018-08-18 21:46:55,425 nonebot] INFO: Succeeded to import "awesome.plugins.weather"
```

这表示 NoneBot 已经成功加载到了 `weather` 插件。

:::warning 注意
如果你运行时没有输出成功导入插件的日志，请确保你的当前工作目录是在 `awesome-bot` 项目的主目录中。

如果仍然不行，尝试先在 `awesome-bot` 主目录中执行下面的命令：

```bash
export PYTHONPATH=.  # Linux / macOS
set PYTHONPATH=.  # Windows
```
:::

## 编写真正的内容

好了，现在已经确保插件可以正确加载，我们可以开始编写命令的实际代码了。在 `weather.py` 中添加如下代码：

```python
from nonebot import on_command, CommandSession


# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
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

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的城市名称不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def get_weather_of_city(city: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    return f'{city}的天气是……'
```

:::tip 提示
从这里开始，你需要对 Python 的 asyncio 编程有所了解，因为 NoneBot 是完全基于 asyncio 的，具体可以参考 [廖雪峰的 Python 教程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143208573480558080fa77514407cb23834c78c6c7309000)。
:::

为了简单起见，我们在这里的例子中没有接入真实的天气数据，但要接入也非常简单，你可以使用中国天气网、和风天气等网站提供的 API。

上面的代码中基本上每一行做了什么都在注释里写了，下面详细解释几个重要的地方。

要理解这段代码，我们要先单独看这个函数：

```python
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    # 获取城市的天气预报
    weather_report = await get_weather_of_city(city)
    # 向用户发送天气预报
    await session.send(weather_report)
```

首先，`session.get()` 函数调用尝试从当前会话（Session）的状态中获取 `city` 这个参数，**所有的参数和会话中需要暂存的临时数据都被存储在 `session.state` 变量（一个 `dict`）中**，如果发现存在，则直接返回，并赋值给 `city` 变量，而如果 `city` 参数不存在，`session.get()` 会**中断**这次命令处理的流程，并保存当前会话，然后向用户发送 `prompt` 参数的内容。**这里的「中断」，意味着如果当前不存在 `city` 参数，`session.get()` 之后的代码将不会被执行，这是通过抛出异常做到的。**

向用户发送 `prompt` 中的提示之后，会话会进入等待状态，此时我们称之为「当前用户正在 weather 命令的会话中」，当用户再次发送消息时，NoneBot 会唤起这个等待中的会话，并重新执行命令，也就是**从头开始**重新执行上面的这个函数，如果用户在一定时间内（默认 5 分钟，可通过 `SESSION_EXPIRE_TIMEOUT` 配置项来更改）都没有再次跟机器人发消息，则会话因超时被关闭。

你可能想问了，既然是重新执行，那执行到 `session.get()` 的时候不还是会中断吗？实际上，NoneBot 在 1.0.0 及更早版本中确实是这样的，必须手动编写下面要说的参数解析器，才能够让 `session.get()` 正确返回；而从 1.1.0 版本开始，NoneBot 会默认地把用户的完整输入作为当前询问内容的回答放进会话状态。

:::tip 提示
删掉下面这段参数解析器，天气命令也可以正常使用，可以尝试不同的输入，看看行为上有什么不同。
:::

但这里我们还是手动编写参数解析器，以应对更复杂的情况，也就是下面这个函数：

```python
# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的城市名称不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
```

参数解析器的 `session` 参数和命令处理函数一样，都是当前命令的会话对象。并且，参数解析器会在命令处理函数之前执行，以确保正确解析参数以供后者使用。

上面的例子中，参数解析器会判断当前是否是该会话第一次运行（用户刚发送 `/天气`，触发了天气命令）。如果是，则检查用户触发天气命令时有没有附带参数（即 `stripped_arg` 是否有内容），如果带了参数（例如用户发送了 `/天气 南京`），则把附带的参数当做要查询的城市放进会话状态 `session.state`，以 `city` 作为状态的 key——也就是说，如果用户触发命令时就给出了城市，则命令处理函数中的 `session.get('city')` 第一次执行时就能返回结果。

如果不是第一次运行，那就说明命令处理函数中向用户询问了更多信息，导致会话被中断，并等待用户回复（也就是 `session.get()` 的效果）。这时候需要判断用户输入是不是有效，因为我们已经明确地询问了，如果用户此时发送了空白字符，显然这是没有意义的内容，需要提示用户重新发送。相反，如果有效的话，则直接以 `session.current_key` 作为 key（也就是 `session.get()` 的第一个参数，上例中只有可能是 `city`），将输入内容存入会话状态。

:::tip 提示
上面用了 `session.current_arg_text` 来获取用户当前输入的参数，这表示从用户输入中提取纯文本部分，也就是说不包含图片、表情、语音、卡片分享等。

如果需要用户输入的原始内容，请使用 `session.current_arg`，里面可能包含 CQ 码。除此之外，还可以通过 `session.current_arg_images` 获取消息中的图片 URL 列表。
:::


现在我们已经理解完了天气命令的代码，是时候运行一下看看实际效果了，启动 NoneBot 后尝试向它分别发送下面的两个带参数和不带参数的消息：

```
/天气 南京
/天气
```

观察看看有什么不同，以及它的回复是否符合我们对代码的理解。如果成功的话，此时你已经完成了一个**可交互的**天气查询命令的雏形，只需要再接入天气 API 就可以真正投入使用了！
