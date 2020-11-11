# 事件处理

在上一章中，我们已经注册了事件响应器，现在我们可以正式编写事件处理逻辑了！

## [事件处理函数](../api/typing.md#handler)

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

在之前的样例中，我们定义了两个函数 `handle_first_receive`, `handle_city`，他们被事件响应器的装饰器装饰从而成为事件响应器的事件处理函数。

:::tips 提示
在事件响应器中，事件处理函数是**顺序**执行的！
:::

### 添加一个事件处理函数

事件响应器提供了三种装饰事件处理函数的装饰器，分别是：

1. [handle()](../api/matcher.md#classmethod-handle)
2. [receive()](../api/matcher.md#classmethod-receive)
3. [got(key, prompt, args_parser)](../api/matcher.md#classmethod-got-key-prompt-none-args-parser-none)

#### handle()

简单的为事件响应器添加一个事件处理函数，这个函数将会在上一个处理函数正常返回执行完毕后立即执行。

#### receive()

指示 NoneBot 接收一条新的用户消息后继续执行该处理函数。此时函数将会接收到新的消息而非前一条消息，之前相关信息可以存储在 state 中。

特别的，当装饰的函数前没有其他事件处理函数，那么 `receive()` 不会接收一条新的消息而是直接使用第一条接收到的消息。

#### got(key, prompt, args_parser)

### 事件处理函数参数

事件处理函数类型为 `Callable[[Bot, Event, dict], Union[Awaitable[None], Awaitable[NoReturn]]]` 。

参数分别为：

1. [nonebot.typing.Bot](../api/typing.md#bot): 即事件上报连接对应的 Bot 对象，为 BaseBot 的子类。特别注意，此处的类型注释可以替换为指定的 Bot 类型，例如：`nonebot.adapters.cqhttp.Bot`，只有在上报事件的 Bot 类型与类型注释相符时才会执行该处理函数！可用于多平台进行不同的处理。
2. [nonebot.typing.Event](../api/typing.md#event): 即上报事件对象，可以获取到上报的所有信息。
3. `state`: 状态字典，可以存储任意的信息

### 参数处理函数 args_parser

### 逻辑控制
