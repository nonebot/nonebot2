# 编写插件

本章将以一个天气查询插件为例，教学如何编写自己的命令。

## 加载插件

在 [创建一个完整的项目](creating-a-project) 一章节中，我们已经创建了插件目录 `awesome_bot/plugins`，现在我们在机器人入口文件中加载它。当然，你也可以单独加载一个插件。

:::tip 提示
加载插件目录时，目录下以 `_` 下划线开头的插件将不会被加载！
:::

在 `bot.py` 文件中添加以下行：

```python{5,7}
import nonebot

nonebot.init()
# 加载单独的一个插件，参数为合法的python包名
nonebot.load_plugin("nonebot.plugins.base")
# 加载插件目录，该目录下为各插件，以下划线开头的插件将不会被加载
nonebot.load_plugins("awesome_bot/plugins")

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
```

尝试运行 `nb run` 或者 `python bot.py`，可以看到日志输出了类似如下内容：

```plain
09-19 21:51:59 [INFO] nonebot | Succeeded to import "nonebot.plugins.base"
09-19 21:51:59 [INFO] nonebot | Succeeded to import "plugin_in_folder"
```

## 创建插件

现在我们已经有了一个空的插件目录，我们可以开始创建插件了！插件有两种形式

### 单文件形式

在插件目录下创建名为 `weather.py` 的 Python 文件，暂时留空，此时目录结构如下：

<!-- prettier-ignore-start -->
:::vue
AweSome-Bot
├── awesome_bot
│   └── plugins
│      └── `weather.py`
├── .env
├── .env.dev
├── .env.prod
├── .gitignore
├── bot.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
:::
<!-- prettier-ignore-end -->

这个时候它已经可以被称为一个插件了，尽管它还什么都没做。

### 包形式

在插件目录下创建文件夹 `weather`，并在该文件夹下创建文件 `__init__.py`，此时目录结构如下：

<!-- prettier-ignore-start -->
:::vue
AweSome-Bot
├── awesome_bot
│   └── plugins
│      └── `weather`
│         └── `__init__.py`
├── .env
├── .env.dev
├── .env.prod
├── .gitignore
├── bot.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
:::
<!-- prettier-ignore-end -->

这个时候 `weather` 就是一个合法的 Python 包了，同时也是合法的 NoneBot 插件，插件内容可以在 `__init__.py` 中编写。

## 编写真正的内容

好了，现在插件已经可以正确加载，我们可以开始编写命令的实际代码了。在 `weather.py` 中添加如下代码：

```python
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event

weather = on_command("天气", rule=to_me(), priority=5)


@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["city"] = args  # 如果用户发送了参数则直接赋值


@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(bot: Bot, event: Event, state: dict):
    city = state["city"]
    if city not in ["上海", "北京"]:
        await weather.reject("你想查询的城市暂不支持，请重新输入！")
    city_weather = await get_weather(city)
    await weather.finish(city_weather)


async def get_weather(city: str):
    return f"{city}的天气是..."
```

为了简单起见，我们在这里的例子中没有接入真实的天气数据，但要接入也非常简单，你可以使用中国天气网、和风天气等网站提供的 API。

下面我们来说明这段代码是如何工作的。

:::tip 提示
从这里开始，你需要对 Python 的 asyncio 编程有所了解，因为 NoneBot 是完全基于 asyncio 的，具体可以参考 [廖雪峰的 Python 教程](https://www.liaoxuefeng.com/wiki/1016959663602400/1017959540289152)
:::

### 注册一个 [事件响应器](../api/matcher.md)

```python{4}
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.permission import Permission

weather = on_command("天气", rule=to_me(), permission=Permission(), priority=5)
```

在上方代码中，我们注册了一个事件响应器 `Matcher`，它由几个部分组成：

1. `on_command` 注册一个消息类型的命令处理器
2. `"天气"` 指定 command 参数 - 命令名
3. `rule` 补充事件响应器的匹配规则
4. `priority` 事件响应器优先级
5. `block` 是否阻止事件传递

其他详细配置可以参考 API 文档，下面我们详细说明各个部分：

#### 事件响应器类型 type

事件响应器类型其实就是对应 `Event.type` ，NoneBot 提供了一个基础类型事件响应器 `on()` 以及一些内置的事件响应器。

- `on("事件类型")`: 基础事件响应器，第一个参数为事件类型，空字符串表示不限
- `on_metaevent()` ~ `on("meta_event")`: 元事件响应器
- `on_message()` ~ `on("message")`: 消息事件响应器
- `on_request()` ~ `on("request")`: 请求事件响应器
- `on_notice()` ~ `on("notice")`: 通知事件响应器
- `on_startswith(str)` ~ `on("message", startswith(str))`: 消息开头匹配处理器
- `on_endswith(str)` ~ `on("message", endswith(str))`: 消息结尾匹配处理器
- `on_command(str|tuple)` ~ `on("message", command(str|tuple))`: 命令处理器
- `on_regax(pattern_str)` ~ `on("message", regax(pattern_str))`: 正则匹配处理器

#### 匹配规则 rule

事件响应器的匹配规则即 `Rule`，由非负个 `RuleChecker` 组成，当所有 `RuleChecker` 返回 `True` 时匹配成功。这些 `RuleChecker` 的形式如下：

```python
async def check(bot: Bot, event: Event, state: dict) -> bool:
    return True

def check(bot: Bot, event: Event, state: dict) -> bool:
    return True
```

`Rule` 和 `RuleChecker` 之间可以使用 `与 &` 互相组合：

```python
from nonebot.rule import Rule

Rule(async_checker1) & sync_checker & async_checker2
```

:::danger 警告
`Rule(*checkers)` 只接受 async function，或使用 `nonebot.utils.run_sync` 自行包裹 sync function。在使用 `与 &` 时，NoneBot 会自动包裹 sync function
:::

#### 优先级 priority

事件响应器的优先级代表事件响应器的执行顺序，同一优先级的事件响应器会 **同时执行！**

:::tip 提示
使用 `nonebot-test` 可以看到当前所有事件响应器的执行流程，有助理解事件响应流程！

```bash
pip install nonebot2[test]
```

:::

#### 阻断 block

当有任意事件响应器发出了阻止事件传递信号时，该事件将不再会传递给下一优先级，直接结束处理。

NoneBot 内置的事件响应器中，所有 `message` 类的事件响应器默认会阻断事件传递，其他则不会。

### 编写事件处理函数 [Handler](../api/typing.md#Handler)
