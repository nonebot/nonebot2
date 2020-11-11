# 注册事件响应器

好了，现在插件已经创建完毕，我们可以开始编写实际代码了，下面将以一个简易单文件天气查询插件为例。

在插件目录下 `weather.py` 中添加如下代码：

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

接下来我们来说明这段代码是如何工作的。

:::tip 提示
从这里开始，你需要对 Python 的 asyncio 编程有所了解，因为 NoneBot 是完全基于 asyncio 的，具体可以参考 [廖雪峰的 Python 教程](https://www.liaoxuefeng.com/wiki/1016959663602400/1017959540289152)
:::

## [事件响应器](../api/matcher.md)

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

### 事件响应器类型 type

事件响应器类型其实就是对应事件的类型 `Event.type` ，NoneBot 提供了一个基础类型事件响应器 `on()` 以及一些其他内置的事件响应器。

以下所有类型的事件响应器都是由 `on(type, rule)` 的形式进行了简化封装。

- `on("事件类型")`: 基础事件响应器，第一个参数为事件类型，空字符串表示不限
- `on_metaevent()` ~ `on("meta_event")`: 元事件响应器
- `on_message()` ~ `on("message")`: 消息事件响应器
- `on_request()` ~ `on("request")`: 请求事件响应器
- `on_notice()` ~ `on("notice")`: 通知事件响应器
- `on_startswith(str)` ~ `on("message", startswith(str))`: 消息开头匹配响应器，参考 [startswith](../api/rule.md#startswith-msg)
- `on_endswith(str)` ~ `on("message", endswith(str))`: 消息结尾匹配响应器，参考 [endswith](../api/rule.md#endswith-msg)
- `on_keyword(set)` ~ `on("message", keyword(str))`: 消息关键词匹配响应器，参考 [keyword](../api/rule.md#keyword-keywords)
- `on_command(str|tuple)` ~ `on("message", command(str|tuple))`: 命令响应器，参考 [command](../api/rule.md#command-cmds)
- `on_regex(pattern_str)` ~ `on("message", regex(pattern_str))`: 正则匹配处理器，参考 [regex](../api/rule.md#regex-regex-flags-0)

### 匹配规则 rule

事件响应器的匹配规则即 `Rule`，详细内容在下方介绍。[直达](#自定义-rule)

### 优先级 priority

事件响应器的优先级代表事件响应器的执行顺序，同一优先级的事件响应器会 **同时执行！**，优先级数字**越小**越先响应！优先级请从 `1` 开始排序！

:::tip 提示
使用 `nonebot-test` 可以看到当前所有事件响应器的执行流程，有助理解事件响应流程！

```bash
pip install nonebot2[test]
```

:::

### 阻断 block

当有任意事件响应器发出了阻止事件传递信号时，该事件将不再会传递给下一优先级，直接结束处理。

NoneBot 内置的事件响应器中，所有 `message` 类的事件响应器默认会阻断事件传递，其他则不会。

## 自定义 rule

rule 的出现使得 nonebot 对事件的响应可以非常自由，nonebot 内置了一些规则：

- [startswith(msg)](../api/rule.md#startswith-msg)
- [endswith(msg)](../api/rule.md#endswith-msg)
- [keyword(\*keywords)](../api/rule.md#keyword-keywords)
- [command(\*cmds)](../api/rule.md#command-cmds)
- [regex(regex, flag)](../api/rule.md#regex-regex-flags-0)

以上规则都是返回类型为 `Rule` 的函数，`Rule` 由非负个 `RuleChecker` 组成，当所有 `RuleChecker` 返回 `True` 时匹配成功。这些 `Rule`, `RuleChecker` 的形式如下：

```python
from nonebot.rule import Rule

async def async_checker(bot: Bot, event: Event, state: dict) -> bool:
    return True

def sync_checker(bot: Bot, event: Event, state: dict) -> bool:
    return True

def check(arg1, args2):

    async def _checker(bot: Bot, event: Event, state: dict) -> bool:
        return bool(arg1 + arg2)

    return Rule(_check)
```

`Rule` 和 `RuleChecker` 之间可以使用 `与 &` 互相组合：

```python
from nonebot.rule import Rule

Rule(async_checker1) & sync_checker & async_checker2
```

**_请勿将事件处理的逻辑写入 `rule` 中，这会使得事件处理返回奇怪的响应。_**

:::danger 警告
`Rule(*checkers)` 只接受 async function，或使用 `nonebot.utils.run_sync` 自行包裹 sync function。在使用 `与 &` 时，NoneBot 会自动包裹 sync function
:::

### 编写事件处理函数 [Handler](../api/typing.md#handler)

```python{1,2,8,9}
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
```

在上面的代码中，我们给 `weather` 事件响应器添加了两个事件处理函数：`handle_first_receive`, `handle_city`

其中有几个要点，我们一一解释：

#### 添加一个事件处理函数

在事件响应器响应事件时，事件处理函数会依次顺序执行，也就是说，与添加顺序一致。

我们可以使用 `@matcher.handle()` 装饰器来简单地为该事件响应器添加一个处理函数。

同时，NoneBot 内置了几种添加事件处理函数方式以方便处理：

- `@matcher.receive()`: 指示 NoneBot 接收一条新的用户消息以继续执行后续处理函数。
- `@matcher.got(key, [prompt="请输入key"], [args_parser=function])`: 指示 NoneBot 当 `state` 中不存在 `key` 时向用户发送 `prompt` 等待用户回复并赋值给 `state[key]`

这些装饰器可以套娃使用！例如：

```python
@matcher.got("key1")
@matcher.got("key2")
async def handle(bot: Bot, event: Event, state: dict):
    pass
```

#### 事件处理函数参数

事件处理函数类型为 `Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]` 。

参数分别为：

1. [nonebot.typing.Bot](../api/typing.md#bot): 即事件上报连接对应的 Bot 对象，为 BaseBot 的子类。特别注意，此处的类型注释可以替换为指定的 Bot 类型，例如：`nonebot.adapters.cqhttp.Bot`，只有在上报事件的 Bot 类型与类型注释相符时才会执行该处理函数！可用于多平台进行不同的处理。
2. [nonebot.typing.Event](../api/typing.md#event): 即上报事件对象，可以获取到上报的所有信息。
3. `state`: 状态字典，可以存储任意的信息

#### 处理事件

在事件处理函数中，我们只需要对 `event` 做出相应的处理，存入状态字典 `state` 中，或者向用户发送消息、调用某个机器人 API 等等。

在 NoneBot 中，提供了几种特殊的处理函数：

##### `@matcher.args_parser`

这是一个装饰器，装饰一个函数来使它成为参数的默认解析函数，当使用 `matcher.got(xxx, [args_parser])` 获取到一条消息时，会运行 `matcher.got` 的 `args_parser` ，如果不存在则运行 `@matcher.args_parser`。

##### `matcher.pause`

这个函数用于结束当前事件处理函数，强制接收一条新的消息再运行**下一个消息处理函数**。

##### `matcher.reject`

这个函数用于结束当前事件处理函数，强制接收一条新的消息再**再次运行当前消息处理函数**。

##### `matcher.finish`

这个函数用于直接结束当前事件处理。

以上三个函数都拥有一个参数 `prompt`，用于向用户发送一条消息。

## 结语

至此，相信你已经能够写出一个基础的插件了，更多的用法将会在 进阶 部分进行介绍，这里给出几个小提示：

- 请千万注意事件处理器的优先级设定
- 在匹配规则中请勿使用耗时极长的函数
- 同一个用户可以跨群（私聊）继续他的事件处理（除非做出权限限制，将在后续介绍）
