---
sidebar_position: 3
description: 响应规则的使用
---

# Alconna 响应规则

以下为一个使用示例：

```python
from nonebot_plugin_alconna.adapters.onebot12 import Image
from nonebot_plugin_alconna import At, on_alconna
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
async def _(result: Arparma):
    if result.find("list"):
        img = await ob12_gen_role_group_list_image()
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
- `aliases: set[str | tuple[str, ...]] | None = None`: 命令别名，作用类似于 `on_command` 中的 aliases
- `comp_config: CompConfig | None = None`: 补全会话配置，不传入则不启用补全会话
- `extensions: list[type[Extension] | Extension] | None = None`: 需要加载的匹配扩展，可以是扩展类或扩展实例
- `exclude_ext: list[type[Extension] | str] | None = None`: 需要排除的匹配扩展，可以是扩展类或扩展的 id
- `use_origin: bool = False`: 是否使用未经 to_me 等处理过的消息
- `use_cmd_start: bool = False`: 是否使用 COMMAND_START 作为命令前缀
- `use_cmd_sep: bool = False`: 是否使用 COMMAND_SEP 作为命令分隔符

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
from nonebot_plugin_alconna import on_alconna, AlconnaMatch, Match, UniMessage

login = on_alconna(Alconna(["/"], "login", Args["password?", str], Option("-r|--recall")))

@login.assign("recall")
async def login_exit():
    await login.finish("已退出")

@login.assign("password")
async def login_handle(pw: Match[str] = AlconnaMatch("password")):
    if pw.available:
        login.set_path_arg("password", pw.result)

@login.got_path("password", prompt=UniMessage.template("{:At(user, $event.get_user_id())} 请输入密码"))
async def login_got(password: str):
    assert password
    await login.send("登录成功")
```

## 依赖注入

`Alconna` 的解析结果会放入 `Arparma` 类中，或用户指定的 `Duplication` 类。

而 `AlconnaMatcher` 在原有 Matcher 的基础上拓展了允许的依赖注入：

```python
@cmd.handle()
async def handle(
    result: CommandResult,
    arp: Arparma,
    dup: Duplication,  # 基类或子类都可以
    ext: Extension,
    source: Alconna,
    abc: str,  # 类似 Match, 但是若匹配结果不存在对应字段则跳过该 handler
    foo: Match[str],
    bar: Query[int] = Query("ttt.bar", 0)  # Query 仍然需要一个默认值来传递 path 参数
):
    ...
```

可以看到，本插件提供了几类额外的模型：

- `CommandResult`: 解析结果，包括了源命令 `source: Alconna` ，解析结果 `result: Arparma`，以及可能的输出信息 `output: str | None` 字段
- `Match`: 匹配项，表示参数是否存在于 `all_matched_args` 内，可用 `Match.available` 判断是否匹配，`Match.result` 获取匹配的值
- `Query`: 查询项，表示参数是否可由 `Arparma.query` 查询并获得结果，可用 `Query.available` 判断是否查询成功，`Query.result` 获取查询结果

:::note

如果你更喜欢 Depends 式的依赖注入，`nonebot_plugin_alconna` 同时提供了一系列的依赖注入函数，他们包括：

- `AlconnaResult`: `CommandResult` 类型的依赖注入函数
- `AlconnaMatches`: `Arparma` 类型的依赖注入函数
- `AlconnaDuplication`: `Duplication` 类型的依赖注入函数
- `AlconnaMatch`: `Match` 类型的依赖注入函数，其能够额外传入一个 middleware 函数来处理得到的参数
- `AlconnaQuery`: `Query` 类型的依赖注入函数，其能够额外传入一个 middleware 函数来处理得到的参数
- `AlconnaExecResult`: 提供挂载在命令上的 callback 的返回结果 (`Dict[str, Any]`) 的依赖注入函数
- `AlconnaExtension`: 提供指定类型的 `Extension` 的依赖注入函数

:::

实例:

```python
...
from nonebot import require
require("nonebot_plugin_alconna")
...

from nonebot_plugin_alconna import on_alconna, Match, Query, AlconnaQuery
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
async def handle_test2(bar: Match[int]):
    if bar.available:
        await test.send(f"foo={bar.result}")

@test.handle()
async def handle_test3(qux: Query[bool] = AlconnaQuery("baz.qux", False)):
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
| [QQ bot](https://github.com/nonebot/adapter-qq)                     | adapters.qq                          |
| [QQ 频道 bot](https://github.com/nonebot/adapter-qq)                | adapters.qqguild                     |
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
| [Satori 协议](https://github.com/nonebot/adapter-satori)            | adapters.satori                      |

## 条件控制

本插件可以通过 `assign` 来控制一个具体的响应函数是否在不满足条件时跳过响应。

```python
...
from nonebot import require
require("nonebot_plugin_alconna")
...

from arclet.alconna import Alconna, Subcommand, Option, Args
from nonebot_plugin_alconna import on_alconna, CommandResult

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

# 仅在命令为 `pip install pip` 时响应
@pip_cmd.assign("install.pak", "pip")
async def update(res: CommandResult):
    ...

# 仅在命令为 `pip list` 时响应
@pip_cmd.assign("list")
async def list_(res: CommandResult):
    ...

# 在命令为 `pip install xxx` 时响应
@pip_cmd.assign("install")
async def install(res: CommandResult):
    ...
```

此外，使用 `AlconnaMatcher.dispatch` 还能像 `CommandGroup` 一样为每个分发设置独立的 matcher：

```python
update_cmd = pip_cmd.dispatch("install.pak", "pip")

@update_cmd.handle()
async def update(arp: CommandResult):
    ...
```

另外，`AlconnaMatcher` 有类似于 `got` 的 `got_path`：

```python
from nonebot_plugin_alconna import At, Match, UniMessage, on_alconna

test_cmd = on_alconna(Alconna("test", Args["target?", Union[str, At]]))

@test_cmd.handle()
async def tt_h(target: Match[Union[str, At]]):
    if target.available:
        test_cmd.set_path_arg("target", target.result)

@test_cmd.got_path("target", prompt="请输入目标")
async def tt(target: Union[str, At]):
    await test_cmd.send(UniMessage(["ok\n", target]))
```

`got_path` 与 `assign`，`Match`，`Query` 等地方一样，都需要指明 `path` 参数 (即对应 Arg 验证的路径)

`got_path` 会获取消息的最后一个消息段并转为 path 对应的类型，例如示例中 `target` 对应的 Arg 里要求 str 或 At，则 got 后用户输入的消息只有为 text 或 at 才能进入处理函数。

:::tip

`path` 支持 ~XXX 语法，其会把 ~ 替换为可能的父级路径：

```python
 pip = Alconna(
     "pip",
     Subcommand(
         "install",
         Args["pak", str],
         Option("--upgrade|-U"),
         Option("--force-reinstall"),
     ),
     Subcommand("list", Option("--out-dated")),
 )

 pipcmd = on_alconna(pip)
 pip_install_cmd = pipcmd.dispatch("install")


 @pip_install_cmd.assign("~upgrade")
 async def pip1_u(pak: Query[str] = Query("~pak")):
     await pip_install_cmd.finish(f"pip upgrading {pak.result}...")
```

:::

## 匹配拓展

本插件提供了一个 `Extension` 类，其用于自定义 AlconnaMatcher 的部分行为。

例如 `LLMExtension` (仅举例)：

```python
from nonebot_plugin_alconna import Extension, Alconna, on_alconna, Interface

class LLMExtension(Extension):
    @property
    def priority(self) -> int:
        return 10

    @property
    def id(self) -> str:
        return "LLMExtension"

    def __init__(self, llm):
      self.llm = llm

    def post_init(self, alc: Alconna) -> None:
        self.llm.add_context(alc.command, alc.meta.description)

    async def receive_wrapper(self, bot, event, receive):
        resp = await self.llm.input(str(receive))
        return receive.__class__(resp.content)

    def before_catch(self, name, annotation, default):
        return name == "llm"

    def catch(self, interface: Interface):
        if interface.name == "llm":
            return self.llm

matcher = on_alconna(
    Alconna(...),
    extensions=[LLMExtension(LLM)]
)
...
```

那么使用了 `LLMExtension` 的响应器便能接受任何能通过 llm 翻译为具体命令的自然语言消息，同时可以在响应器中为所有 `llm` 参数注入模型变量

目前 `Extension` 的功能有：

- `validate`: 对于事件的来源适配器或 bot 选择是否接受响应
- `output_converter`: 输出信息的自定义转换方法
- `message_provider`: 从传入事件中自定义提取消息的方法
- `receive_provider`: 对传入的消息 (Message 或 UniMessage) 的额外处理
- `permission_check`: 命令对消息解析并确认头部匹配（即确认选择响应）时对发送者的权限判断
- `parse_wrapper`: 对命令解析结果的额外处理
- `send_wrapper`: 对发送的消息 (Message 或 UniMessage) 的额外处理
- `before_catch`: 自定义依赖注入的绑定确认函数
- `catch`: 自定义依赖注入处理函数
- `post_init`: 响应器创建后对命令对象的额外除了

例如内置的 `DiscordSlashExtension`，其可自动将 Alconna 对象翻译成 slash 指令并注册，且将收到的指令交互事件转为指令供命令解析:

```python
from nonebot_plugin_alconna import Match, on_alconna

from nonebot_plugin_alconna.adapters.discord import DiscordSlashExtension

alc = Alconna(
    ["/"],
    "permission",
    Subcommand("add", Args["plugin", str]["priority?", int]),
    Option("remove", Args["plugin", str]["time?", int]),
    meta=CommandMeta(description="权限管理"),
)

matcher = on_alconna(alc, extensions=[DiscordSlashExtension()])

@matcher.assign("add")
async def add(plugin: Match[str], priority: Match[int]):
    await matcher.finish(f"added {plugin.result} with {priority.result if priority.available else 0}")

@matcher.assign("remove")
async def remove(plugin: Match[str], time: Match[int]):
    await matcher.finish(f"removed {plugin.result} with {time.result if time.available else -1}")
```

:::tip

全局的 Extension 可延迟加载 (即若有全局拓展加载于部分 AlconnaMatcher 之后，这部分响应器会被追加拓展)

:::
