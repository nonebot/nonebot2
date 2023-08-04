---
sidebar_position: 3
description: 响应规则的使用
---

# Alconna 响应规则

以下为一个简单的使用示例：

```python
from nonebot_plugin_alconna.adapters import At
from nonebot.adapters.onebot.v12 import Message
from nonebot_plugin_alconna.adapters.onebot12 import Image
from nonebot_plugin_alconna import AlconnaMatches, on_alconna
from nonebot.adapters.onebot.v12 import MessageSegment as Ob12MS
from arclet.alconna import Args, Option, Alconna, Arparma, MultiVar, Subcommand

alc = Alconna(
    ["/", "!"],
    "role-group",
    Subcommand(
        "add",
        Args["name", str],
        Option("member", Args["target", MultiVar(At)]),
    ),
    Option("list"),
)
rg = on_alconna(alc, auto_send_output=True)


@rg.handle()
async def _(result: Arparma = AlconnaMatches()):
    if result.find("list"):
        img = await gen_role_group_list_image()
        await rg.finish(Message([Image(img)]))
    if result.find("add"):
        group = await create_role_group(result["add.name"])
        if result.find("add.member"):
            ats: tuple[Ob12MS, ...] = result["add.member.target"]
            group.extend(member.data["user_id"] for member in ats)
        await rg.finish("添加成功")
```

## 响应器使用

`on_alconna` 的所有参数如下：

- `command: Alconna | str`: Alconna 命令
- `skip_for_unmatch: bool = True`: 是否在命令不匹配时跳过该响应
- `auto_send_output: bool = False`: 是否自动发送输出信息并跳过响应
- `output_converter: TConvert | None = None`: 输出信息字符串转换为消息序列方法
- `aliases: set[str | tuple[str, ...]] | None = None`: 命令别名， 作用类似于 `on_command` 中的 aliases
- `comp_config: CompConfig | None = None`: 补全会话配置， 不传入则不启用补全会话
- `use_origin: bool = False`: 是否使用未经 to_me 等处理过的消息

`on_alconna` 返回的是 `Matcher` 的子类 `AlconnaMatcher`，其拓展了四类方法：

- `.assign(path, value, or_not)`: 用于对包含多个选项/子命令的命令的分派处理
- `.got_path(path, prompt)`: 在 `got` 方法的基础上，会以 path 对应的参数为准，读取传入 message 的最后一个消息段并验证转换
- `.set_path_arg(key, value)`, `.get_path_arg(key)`: 类似 `set_arg` 和 `got_arg`，为 `got_path` 的特化版本

用例：

```python
from arclet.alconna import Alconna, Option, Args
from nonebot_plugin_alconna import on_alconna, AlconnaMatch, Match, AlconnaMatcher, AlconnaArg

login = on_alconna(Alconna(["/"], "login", Args["password?", str], Option("-r|--recall")))

@login.assign("recall")
async def login_exit():
    await login.finish("已退出")

@login.assign("password")
async def login_handle(matcher: AlconnaMatcher, pw: Match[str] = AlconnaMatch("password")):
    matcher.set_path_arg("password", pw.result)

@login.got_path("password", prompt="请输入密码")
async def login_got(password: str = AlconnaArg("password")):
    assert password
    await login.send("登录成功")
```

## 依赖注入

`Alconna` 的解析结果会放入 `Arparma` 类中，或用户指定的 `Duplication` 类。


`nonebot_plugin_alconna` 提供了一系列的依赖注入函数，他们包括：

- `AlconnaResult`: `CommandResult` 类型的依赖注入函数
- `AlconnaMatches`: `Arparma` 类型的依赖注入函数
- `AlconnaDuplication`: `Duplication` 类型的依赖注入函数
- `AlconnaMatch`: `Match` 类型的依赖注入函数
- `AlconnaQuery`: `Query` 类型的依赖注入函数
- `AlconnaExecResult`: 提供挂载在命令上的 callback 的返回结果 (`Dict[str, Any]`) 的依赖注入函数

可以看到，本插件提供了几类额外的模型：
- `CommandResult`: 解析结果，包括了源命令 `command: Alconna` ，解析结果 `result: Arparma`，以及可能的输出信息 `output: str | None` 字段
- `Match`: 匹配项，表示参数是否存在于 `all_matched_args` 内，可用 `Match.available` 判断是否匹配，`Match.result` 获取匹配的值
- `Query`: 查询项，表示参数是否可由 `Arparma.query` 查询并获得结果，可用 `Query.available` 判断是否查询成功，`Query.result` 获取查询结果

同时，基于 [`Annotated` 支持](https://github.com/nonebot/nonebot2/pull/1832), 添加了两类注解:

- `AlcMatches`：同 `AlconnaMatches`
- `AlcResult`：同 `AlconnaResult`
- `AlcExecResult`: 同 `AlconnaExecResult`

实例:
```python
...
from nonebot import require
require("nonebot_plugin_alconna")
...

from nonebot_plugin_alconna import (
    on_alconna, 
    Match,
    Query,
    AlconnaMatch, 
    AlconnaQuery,
    AlconnaMatches,
    AlcResult
)
from arclet.alconna import Alconna, Args, Option, Arparma

test = on_alconna(
    Alconna(
        "test",
        Option("foo", Args["bar", int]),
        Option("baz", Args["qux", bool, False])
    ),
    auto_send_output=True
)


@test.handle()
async def handle_test1(result: AlcResult):
    await test.send(f"matched: {result.matched}")
    await test.send(f"maybe output: {result.output}")

@test.handle()
async def handle_test2(result: Arparma = AlconnaMatches()):
    await test.send(f"head result: {result.header_result}")
    await test.send(f"args: {result.all_matched_args}")

@test.handle()
async def handle_test3(bar: Match[int] = AlconnaMatch("bar")):
    if bar.available:    
        await test.send(f"foo={bar.result}")

@test.handle()
async def handle_test4(qux: Query[bool] = AlconnaQuery("baz.qux", False)):
    if qux.available:
        await test.send(f"baz.qux={qux.result}")
```

## 消息段标注

示例中使用了消息段标注，其中 `At` 属于通用标注，而 `Image` 属于 `onebot12` 适配器下的标注。

消息段标注会匹配特定的 `MessageSegment`：

```python
...
ats: tuple[Ob12MS, ...] = result["add.member.target"]
group.extend(member.data["user_id"] for member in ats)
```

:::tip
通用标注与适配器标注的区别在于，通用标注会匹配多个适配器中相似类型的消息段。

通用标注返回的是 `nonebot_plugin_alconna.adapters` 中定义的 `Segment` 模型:

```python
class Segment:
    """基类标注"""
    origin: MessageSegment

class At(Segment):
    """At对象, 表示一类提醒某用户的元素"""
    target: str

class Emoji(Segment):
    """Emoji对象, 表示一类表情元素"""
    id: str
    name: Optional[str]

class Media(Segment):
    url: Optional[str]
    id: Optional[str]

class Image(Media):
    """Image对象, 表示一类图片元素"""

class Audio(Media):
    """Audio对象, 表示一类音频元素"""

class Voice(Media):
    """Voice对象, 表示一类语音元素"""

class Video(Media):
    """Video对象, 表示一类视频元素"""

class File(Segment):
    """File对象, 表示一类文件元素"""
    id: str
    name: Optional[str] = field(default=None)
```

:::




## 特殊装饰器

`nonebot_plugin_alconna` 提供 了一个 `funcommand` 装饰器, 其用于将一个接受任意参数，
返回 `str` 或 `Message` 或 `MessageSegment` 的函数转换为命令响应器。

```python
from nonebot_plugin_alconna import funcommand

@funcommand()
async def echo(msg: str):
    return msg
```

其等同于

```python
from arclet.alconna import Alconna, Args
from nonebot_plugin_alconna import on_alconna, AlconnaMatch, Match

echo = on_alconna(Alconna("echo", Args["msg", str]))

@echo.handle()
async def echo_exit(msg: Match[str] = AlconnaMatch("msg")):
    await echo.finish(msg.result)
```
