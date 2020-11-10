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

在之前的样例中，我们定义了两个函数，他们被事件响应器的装饰器装饰从而成为事件响应器的事件处理函数。

### 装饰器

事件响应器提供了三种装饰事件处理函数的装饰器，分别是：

1. [handle()](../api/matcher.md#classmethod-handle)
2. [receive()](../api/matcher.md#classmethod-receive)
3. [got(key, prompt, args_parser)](../api/matcher.md#classmethod-got-key-prompt-none-args-parser-none)
