---
sidebar_position: 9

options:
  menu:
    weight: 90
    category: guide
---

# 事件处理

在上一章中，我们已经注册了事件响应器，现在我们可以正式编写事件处理逻辑了！

## [事件处理函数](../api/typing.md#handler)

```python{1,2,8,9}
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
```

在之前的样例中，我们定义了两个函数 `handle_first_receive`, `handle_city`，他们被事件响应器的装饰器装饰从而成为事件响应器的事件处理函数。

:::tip 提示
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

特别地，当装饰的函数前没有其他事件处理函数，那么 `receive()` 不会接收一条新的消息而是直接使用第一条接收到的消息。

#### got(key, prompt, args_parser)

指示 NoneBot 当 `state` 中不存在 `key` 时向用户发送 `prompt` 等待用户回复并赋值给 `state[key]`。

`prompt` 可以为 `str`, `Message`, `MessageSegment`，若为空则不会向用户发送，若不为空则会在 format 之后发送，即 `prompt.format(**state)`，注意对 `{}` 进行转义。示例：

```python
@matcher.receive()
async def handle(bot: Bot, event: Event, state: T_State):
    state["key"] = "hello"


@matcher.got("key2", prompt="{key}!")
async def handle2(bot: Bot, event: Event, state: T_State):
    pass
```

`args_parser` 为参数处理函数，在这里传入一个新的函数以覆盖默认的参数处理。详情参照 [args_parser](#参数处理函数-args-parser)

特别的，这些装饰器都可以套娃使用：

```python
@matcher.got("key1")
@matcher.got("key2")
async def handle(bot: Bot, event: Event, state: T_State):
    pass
```

### 事件处理函数参数

事件处理函数类型为：

- `Callable[[Bot, Event, T_State, Matcher], Union[Awaitable[None], Awaitable[NoReturn]]]`
- `Callable[[Bot, Event, T_State], Union[Awaitable[None], Awaitable[NoReturn]]]`
- `Callable[[Bot, Event, Matcher], Union[Awaitable[None], Awaitable[NoReturn]]]`
- `Callable[[Bot, T_State, Matcher], Union[Awaitable[None], Awaitable[NoReturn]]]`
- `Callable[[Bot, Event], Union[Awaitable[None], Awaitable[NoReturn]]]`
- `Callable[[Bot, T_State], Union[Awaitable[None], Awaitable[NoReturn]]]`
- `Callable[[Bot, Matcher], Union[Awaitable[None], Awaitable[NoReturn]]]`
- `Callable[[Bot], Union[Awaitable[None], Awaitable[NoReturn]]]`

简单说就是：除了 `bot` 参数，其他都是可选的。

以下函数都是合法的事件处理函数（仅列举常用的）：

```python
async def handle(bot: Bot, event: Event, state: T_State):
    pass

async def handle(bot: Bot, event: Event, state: T_State, matcher: Matcher):
    pass

async def handle(bot: Bot, event: Event):
    pass

async def handle(bot: Bot, state: T_State):
    pass

async def handle(bot: Bot):
    pass
```

:::danger 警告
函数的参数名固定不能修改！
:::

参数分别为：

1. [nonebot.adapters.Bot](../api/adapters/README.md#class-bot): 即事件上报连接对应的 Bot 对象，为 BaseBot 的子类。特别注意，此处的类型注释可以替换为指定的 Bot 类型，例如：`nonebot.adapters.cqhttp.Bot`，只有在上报事件的 Bot 类型与类型注释相符时才会执行该处理函数！可用于多平台进行不同的处理。
2. [nonebot.adapters.Event](../api/adapters/README.md#class-event): 即上报事件对象，可以获取到上报的所有信息。
3. [state](../api/typing.md#t-state): 状态字典，可以存储任意的信息，其中还包含一些特殊的值以获取 NoneBot 内部处理时的一些信息，如：

- `state["_current_key"]`: 存储当前 `got` 获取的参数名
- `state["_prefix"]`, `state["_suffix"]`: 存储当前 TRIE 匹配的前缀/后缀，可以通过该值获取用户命令的原始命令

:::tip 提示
NoneBot 会对不同类型的参数进行不同的操作，详情查看 [事件处理函数重载](../advanced/handler/overload.md)
:::

### 参数处理函数 args_parser

在使用 `got` 获取用户输入参数时，需要对用户的消息进行处理以转换为我们所需要的信息。在默认情况下，NoneBot 会把用户的消息字符串原封不动的赋值给 `state[key]` 。可以通过以下两种方式修改默认处理逻辑：

- `@matcher.args_parser` 装饰器：直接装饰一个函数作为参数处理器
- `got(key, prompt, args_parser)`：直接把函数作为参数传入

参数处理函数类型为：`Callable[[Bot, Event, T_State], Union[Awaitable[None], Awaitable[NoReturn]]]`，即：

```python
async def parser(bot: Bot, event: Event, state: T_State):
    state[state["_current_key"]] = str(event.get_message())
```

特别的，`state["_current_key"]` 中存储了当前获取的参数名

### 逻辑控制

NoneBot 也为事件处理函数提供了一些便捷的逻辑控制函数：

#### `matcher.send`

这个函数用于发送一条消息给当前交互的用户。~~其实这并不是一个逻辑控制函数，只是不知道放在哪里……~~

#### `matcher.pause`

这个函数用于结束当前事件处理函数，强制接收一条新的消息再运行**下一个消息处理函数**。

#### `matcher.reject`

这个函数用于结束当前事件处理函数，强制接收一条新的消息再**再次运行当前消息处理函数**。常用于用户输入信息不符合预期。

#### `matcher.finish`

这个函数用于直接结束当前事件处理。

以上三个函数都拥有一个参数 `message` / `prompt`，用于向用户发送一条消息。以及 `**kwargs` 直接传递给 `bot.send` 的额外参数。

## 常用事件处理结构

```python
matcher = on_command("test")

# 修改默认参数处理
@matcher.args_parser
async def parse(bot: Bot, event: Event, state: T_State):
    print(state["_current_key"], ":", str(event.get_message()))
    state[state["_current_key"]] = str(event.get_message())

@matcher.handle()
async def first_receive(bot: Bot, event: Event, state: T_State):
    # 获取用户原始命令，如：/test
    print(state["_prefix"]["raw_command"])
    # 处理用户输入参数，如：/test arg1 arg2
    raw_args = str(event.get_message()).strip()
    if raw_args:
        arg_list = raw_args.split()
        # 将参数存入state以阻止后续再向用户询问参数
        state["arg1"] = arg_list[0]


@matcher.got("arg1", prompt="参数？")
async def arg_handle(bot: Bot, event: Event, state: T_State):
    # 在这里对参数进行验证
    if state["arg1"] not in ["allow", "list"]:
        await matcher.reject("参数不正确！请重新输入")
    # 发送一些信息
    await bot.send(event, "message")
    await matcher.send("message")
    await matcher.finish("message")
```
