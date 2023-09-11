---
sidebar_position: 3
description: 响应规则的使用
---

# Alconna 响应规则

以下为一个简单的使用示例：

```python
from nonebot_plugin_alconna.adapters.onebot12 import Image
from nonebot_plugin_alconna import At, AlconnaMatches, on_alconna
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
    Option("icon", Args["icon", Image])
)
rg = on_alconna(alc, auto_send_output=True)


@rg.handle()
async def _(result: Arparma = AlconnaMatches()):
    if result.find("list"):
        img = await gen_role_group_list_image()
        await rg.finish(Image(img))
    if result.find("add"):
        group = await create_role_group(result.query[str]("add.name"))
        if result.find("add.member"):
            ats = result.query[tuple[At, ...]]("add.member.target")
            group.extend(member.target for member in ats)
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
- `use_cmd_start`: 是否使用 COMMAND_START 作为命令前缀

`on_alconna` 返回的是 `Matcher` 的子类 `AlconnaMatcher`，其拓展了如下方法：

- `.assign(path, value, or_not)`: 用于对包含多个选项/子命令的命令的分派处理
- `.got_path(path, prompt, middleware)`: 在 `got` 方法的基础上，会以 path 对应的参数为准，读取传入 message 的最后一个消息段并验证转换
- `.set_path_arg(key, value)`, `.get_path_arg(key)`: 类似 `set_arg` 和 `got_arg`，为 `got_path` 的特化版本
- `.reject_path(path[, prompt, fallback])`: 类似于 `reject_arg`，对应 `got_path`
- `.dispatch`: 同样的分派处理，但是是类似 `CommandGroup` 一样返回新的 `AlconnaMatcher`
- `.got`, `send`, `reject`, ...: 拓展了 prompt 类型，即支持使用 `UniMessage` 作为 prompt

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
- `AlconnaMatch`: `Match` 类型的依赖注入函数，其能够额外传入一个 middleware 函数来处理得到的参数
- `AlconnaQuery`: `Query` 类型的依赖注入函数，其能够额外传入一个 middleware 函数来处理得到的参数
- `AlconnaExecResult`: 提供挂载在命令上的 callback 的返回结果 (`Dict[str, Any]`) 的依赖注入函数

可以看到，本插件提供了几类额外的模型：

- `CommandResult`: 解析结果，包括了源命令 `source: Alconna` ，解析结果 `result: Arparma`，以及可能的输出信息 `output: str | None` 字段
- `Match`: 匹配项，表示参数是否存在于 `all_matched_args` 内，可用 `Match.available` 判断是否匹配，`Match.result` 获取匹配的值
- `Query`: 查询项，表示参数是否可由 `Arparma.query` 查询并获得结果，可用 `Query.available` 判断是否查询成功，`Query.result` 获取查询结果

同时，基于 [`Annotated` 支持](https://github.com/nonebot/nonebot2/pull/1832), 添加了三类注解:

- `AlcMatches`：同 `AlconnaMatches`
- `AlcResult`：同 `AlconnaResult`
- `AlcExecResult`: 同 `AlconnaExecResult`

而若设置配置项 **ALCONNA_USE_PARAM** (默认为 True) 为 True，则上述依赖注入的目标参数皆不需要使用依赖注入函数：

```python
async def handle(
    result: CommandResult,
    arp: Arparma,
    dup: Duplication,
    source: Alconna,
    abc: str,  # 类似 Match, 但是若匹配结果不存在对应字段则跳过该 handler
    foo: Match[str],
    bar: Query[int] = Query("ttt.bar", 0)  # Query 仍然需要一个默认值来传递 path 参数
):
    ...
```

该效果对于 `got_path` 下的 Arg 同样有效

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
    AlconnaQuery,
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
async def handle_test2(result: Arparma):
    await test.send(f"head result: {result.header_result}")
    await test.send(f"args: {result.all_matched_args}")

@test.handle()
async def handle_test3(bar: Match[int]):
    if bar.available:
        await test.send(f"foo={bar.result}")

@test.handle()
async def handle_test4(qux: Query[bool] = AlconnaQuery("baz.qux", False)):
    if qux.available:
        await test.send(f"baz.qux={qux.result}")
```

## 消息段标注

示例中使用了消息段标注，其中 `At` 属于通用标注，而 `Image` 属于 `onebot12` 适配器下的标注。

适配器下的消息段标注会匹配特定的 `MessageSegment`：

而通用标注与适配器标注的区别在于，通用标注会匹配多个适配器中相似类型的消息段，并返回
`nonebot_plugin_alconna.uniseg` 中定义的 [`Segment` 模型](./utils.md#通用消息段)

例如：

```python
...
ats = result.query[tuple[At, ...]]("add.member.target")
group.extend(member.target for member in ats)
```

这样插件使用者就不用考虑平台之间字段的差异

本插件为以下适配器提供了专门的适配器标注：

| 协议名称                                                            | 路径                                 |
| ------------------------------------------------------------------- | ------------------------------------ |
| [OneBot 协议](https://github.com/nonebot/adapter-onebot)            | adapters.onebot11, adapters.onebot12 |
| [Telegram](https://github.com/nonebot/adapter-telegram)             | adapters.telegram                    |
| [飞书](https://github.com/nonebot/adapter-feishu)                   | adapters.feishu                      |
| [GitHub](https://github.com/nonebot/adapter-github)                 | adapters.github                      |
| [QQ 频道](https://github.com/nonebot/adapter-qqguild)               | adapters.qqguild                     |
| [钉钉](https://github.com/nonebot/adapter-ding)                     | adapters.ding                        |
| [Console](https://github.com/nonebot/adapter-console)               | adapters.console                     |
| [开黑啦](https://github.com/Tian-que/nonebot-adapter-kaiheila)      | adapters.kook                        |
| [Mirai](https://github.com/ieew/nonebot_adapter_mirai2)             | adapters.mirai                       |
| [Ntchat](https://github.com/JustUndertaker/adapter-ntchat)          | adapters.ntchat                      |
| [MineCraft](https://github.com/17TheWord/nonebot-adapter-minecraft) | adapters.minecraft                   |
| [BiliBili Live](https://github.com/wwweww/adapter-bilibili)         | adapters.bilibili                    |
| [Walle-Q](https://github.com/onebot-walle/nonebot_adapter_walleq)   | adapters.onebot12                    |
| [Villa](https://github.com/CMHopeSunshine/nonebot-adapter-villa)    | adapters.villa                       |
| [Discord](https://github.com/nonebot/adapter-discord)               | adapters.discord                     |
| [Red 协议](https://github.com/nonebot/adapter-red)                  | adapters.red                         |

## 条件控制

本插件可以通过 `handle(parameterless)` 来控制一个具体的响应函数是否在不满足条件时跳过响应。

```python
...
from nonebot import require
require("nonebot_plugin_alconna")
...

from arclet.alconna import Alconna, Subcommand, Option, Args
from nonebot_plugin_alconna import assign, on_alconna, CommandResult, Check

pip = Alconna(
    "pip",
    Subcommand(
        "install", Args["pak", str],
        Option("--upgrade"),
        Option("--force-reinstall")
    ),
    Subcommand("list", Option("--out-dated"))
)

pip_cmd = on_alconna(pip)

# 仅在命令为 `pip install` 并且 pak 为 `pip` 时响应
@pip_cmd.handle([Check(assign("install.pak", "pip"))])
async def update(arp: CommandResult):
    ...

# 仅在命令为 `pip list` 时响应
@pip_cmd.handle([Check(assign("list"))])
async def list_(arp: CommandResult):
    ...

# 仅在命令为 `pip install` 时响应
@pip_cmd.handle([Check(assign("install"))])
async def install(arp: CommandResult):
    ...
```

或者使用 `AlconnaMatcher.assign`：

```python
@pip_cmd.assign("install.pak", "pip")
async def update(arp: CommandResult):
    ...

# 仅在命令为 `pip list` 时响应
@pip_cmd.assign("list")
async def list_(arp: CommandResult):
    ...

# 仅在命令为 `pip install` 时响应
@pip_cmd.assign("install")
async def install(arp: CommandResult):
    ...
```

或者使用 `AlconnaMatcher.dispatch`：

此外，还能像 `CommandGroup` 一样为每个分发设置独立的 matcher：

```python
update_cmd = pip_cmd.dispatch("install.pak", "pip")

@update_cmd.handle()
async def update(arp: CommandResult = AlconnaResult()):
    ...
```
