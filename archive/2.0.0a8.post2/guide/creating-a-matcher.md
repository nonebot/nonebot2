# 注册事件响应器

好了，现在插件已经创建完毕，我们可以开始编写实际代码了，下面将以一个简易单文件天气查询插件为例。

在插件目录下 `weather.py` 中添加如下代码：

```python
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

weather = on_command("天气", rule=to_me(), priority=5)


@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["city"] = args  # 如果用户发送了参数则直接赋值


@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(bot: Bot, event: Event, state: T_State):
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

```python{5}
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

事件响应器类型其实就是对应事件的类型 `Event.get_type()` ，NoneBot 提供了一个基础类型事件响应器 `on()` 以及一些其他内置的事件响应器。

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
使用 `nonebot-plugin-test` 可以在网页端查看当前所有事件响应器的执行流程，有助理解事件响应流程！

```bash
nb plugin install nonebot_plugin_test
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
from nonebot.typing import T_State

async def async_checker(bot: Bot, event: Event, state: T_State) -> bool:
    return True

def sync_checker(bot: Bot, event: Event, state: T_State) -> bool:
    return True

def check(arg1, args2):

    async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
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
