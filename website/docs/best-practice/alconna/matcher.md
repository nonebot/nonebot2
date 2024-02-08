---
sidebar_position: 3
description: 响应规则的使用
---

# Alconna插件 响应规则

展示：

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

本插件基于 **Alconna** , 为 **Nonebot** 提供了一类新的事件响应器辅助函数 `on_alconna`.

```python
def on_alconna(
    command: Alconna | str,
    skip_for_unmatch: bool = True,
    auto_send_output: bool = False,
    aliases: set[str | tuple[str, ...]] | None = None,
    comp_config: CompConfig | None = None,
    extensions: list[type[Extension] | Extension] | None = None,
    exclude_ext: list[type[Extension] | str] | None = None,
    use_origin: bool = False,
    use_cmd_start: bool = False,
    use_cmd_sep: bool = False,
    **kwargs,
    ...,
):
```

- `command`: Alconna 命令或字符串，字符串将通过 `AlconnaFormat` 转换为 Alconna 命令
- `skip_for_unmatch`: 是否在命令不匹配时跳过该响应
- `auto_send_output`: 是否自动发送输出信息并跳过响应
- `aliases`: 命令别名， 作用类似于 `on_command` 中的 aliases
- `comp_config`: 补全会话配置， 不传入则不启用补全会话
- `extensions`: 需要加载的匹配扩展, 可以是扩展类或扩展实例
- `exclude_ext`: 需要排除的匹配扩展, 可以是扩展类或扩展的id
- `use_origin`: 是否使用未经 to_me 等处理过的消息
- `use_cmd_start`: 是否使用 COMMAND_START 作为命令前缀
- `use_cmd_sep`: 是否使用 COMMAND_SEP 作为命令分隔符

`on_alconna` 返回的是 `Matcher` 的子类 `AlconnaMatcher`，其拓展了如下方法:

- `.assign(path, value, or_not)`: 用于对包含多个选项/子命令的命令的分派处理(具体请看条件控制)
- `.got_path(path, prompt, middleware)`: 在 `got` 方法的基础上，会以 path 对应的参数为准，读取传入 message 的最后一个消息段并验证转换
- `.set_path_arg(key, value)`, `.get_path_arg(key)`: 类似 `set_arg` 和 `got_arg`，为 `got_path` 的特化版本
- `.reject_path(path[, prompt, fallback])`: 类似于 `reject_arg`，对应 `got_path`
- `.dispatch`: 同样的分派处理，但是是类似 `CommandGroup` 一样返回新的 `AlconnaMatcher`
- `.got`, `send`, `reject`, ...: 拓展了 prompt 类型，即支持使用 `UniMessage` 作为 prompt

`assign`实例:

```python
from nonebot import require
require("nonebot_plugin_alconna")

from arclet.alconna import Alconna, Option, Args
from nonebot_plugin_alconna import on_alconna, AlconnaMatch, Match, UniMessage


login = on_alconna(Alconna(["/"], "login", Args["password?", str], Option("-r|--recall"))) # 这里["/"]指命令前缀必须是/

@login.assign("recall") # /login -r
async def login_exit():
    await login.finish("已退出")

@login.assign("password") # /login xxx
async def login_handle(pw: Match[str] = AlconnaMatch("password")):
    if pw.available:
        login.set_path_arg("password", pw.result)
```

`dispatch`每个分发设置独立的 matcher:

```python
update_cmd = pip_cmd.dispatch("install.pak", "pip")

@update_cmd.handle()
async def update(arp: CommandResult = AlconnaResult()):
    ...
```

`got_path`类似 Nonebot2 的got, 它与 `assign`，`Match`，`Query` 等地方一样，都需要指明 `path` 参数 (即对应 Arg 验证的路径)

`got_path` 会获取消息的最后一个消息段并转为 path 对应的类型，例如示例中 `target` 对应的 Arg 里要求 str 或 At，则 got 后用户输入的消息只有为 text 或 at 才能进入处理函数.

实例:

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

:::tip

`path`支持 ~XXX 语法，其会把 ~ 替换为可能的父级路径:

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

## Alconna的依赖注入

本插件提供了一系列依赖注入函数，便于在响应函数中获取解析结果:

- `AlconnaResult`: `CommandResult` 类型的依赖注入函数
- `AlconnaMatches`: `Arparma` 类型的依赖注入函数
- `AlconnaDuplication`: `Duplication` 类型的依赖注入函数
- `AlconnaMatch`: `Match` 类型的依赖注入函数
- `AlconnaQuery`: `Query` 类型的依赖注入函数

同时，基于 [`Annotated` 支持](https://github.com/nonebot/nonebot2/pull/1832), 添加了两类注解:

- `AlcMatches`：同 `AlconnaMatches`
- `AlcResult`：同 `AlconnaResult`

可以看到，本插件提供了几类额外的模型:

- `CommandResult`: 解析结果，包括了源命令 `source: Alconna` ，解析结果 `result: Arparma`，以及可能的输出信息 `output: str | None` 字段
- `Match`: 匹配项，表示参数是否存在于 `all_matched_args` 内，可用 `Match.available` 判断是否匹配，`Match.result` 获取匹配的值
- `Query`: 查询项，表示参数是否可由 `Arparma.query` 查询并获得结果，可用 `Query.available` 判断是否查询成功，`Query.result` 获取查询结果

**Alconna** 默认依赖注入的目标参数皆不需要使用依赖注入函数， 该效果对于 `AlconnaMatcher.got_path` 下的 Arg 同样有效:

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

:::tip

如果你更喜欢 Depends 式的依赖注入，`nonebot_plugin_alconna` 同时提供了一系列的依赖注入函数，他们包括：

- `AlconnaResult`: `CommandResult` 类型的依赖注入函数
- `AlconnaMatches`: `Arparma` 类型的依赖注入函数
- `AlconnaDuplication`: `Duplication` 类型的依赖注入函数
- `AlconnaMatch`: `Match` 类型的依赖注入函数，其能够额外传入一个 middleware 函数来处理得到的参数
- `AlconnaQuery`: `Query` 类型的依赖注入函数，其能够额外传入一个 middleware 函数来处理得到的参数
- `AlconnaExecResult`: 提供挂载在命令上的 callback 的返回结果 (`Dict[str, Any]`) 的依赖注入函数
- `AlconnaExtension`: 提供指定类型的 `Extension` 的依赖注入函数

:::

实例:

```python
from nonebot import require
require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import (
    on_alconna,
    Match,
    Query,
    AlconnaMatch,
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
async def handle_test3(bar: Match[int] = AlconnaMatch("bar")):
    if bar.available:
        await test.send(f"foo={bar.result}")

@test.handle()
async def handle_test4(qux: Query[bool] = Query("baz.qux", False)):
    if qux.available:
        await test.send(f"baz.qux={qux.result}")
```

## 跨平台适配

`uniseg` 模块属于 `nonebot-plugin-alconna` 的子插件，其提供了一套通用的消息组件，用于在 `nonebot-plugin-alconna` 下构建通用消息.

### 通用消息段

适配器下的消息段标注会匹配适配器特定的 `MessageSegment`, 而通用消息段与适配器消息段的区别在于:

通用消息段会匹配多个适配器中相似类型的消息段，并返回 `uniseg` 模块中定义的 [`Segment` 模型](https://nonebot.dev/docs/next/best-practice/alconna/utils#%E9%80%9A%E7%94%A8%E6%B6%88%E6%81%AF%E6%AE%B5), 以达到**跨平台接收消息**的作用

`uniseg` 模块提供了类似 `MessageSegment` 的通用消息段，并可在 `Alconna` 下直接标注使用：

```python
class Segment:
    """基类标注"""

class Text(Segment):
    """Text对象, 表示一类文本元素"""
    text: str
    style: Optional[str]

class At(Segment):
    """At对象, 表示一类提醒某用户的元素"""
    type: Literal["user", "role", "channel"]
    target: str

class AtAll(Segment):
    """AtAll对象, 表示一类提醒所有人的元素"""

class Emoji(Segment):
    """Emoji对象, 表示一类表情元素"""
    id: str
    name: Optional[str]

class Media(Segment):
    url: Optional[str]
    id: Optional[str]
    path: Optional[str]
    raw: Optional[bytes]

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
    name: Optional[str]

class Reply(Segment):
    """Reply对象，表示一类回复消息"""
    id: str
    """此处不一定是消息ID，可能是其他ID，如消息序号等"""
    msg: Optional[Union[Message, str]]
    origin: Optional[Any]

class Reference(Segment):
    """Reference对象，表示一类引用消息。转发消息 (Forward) 也属于此类"""
    id: Optional[str]
    """此处不一定是消息ID，可能是其他ID，如消息序号等"""
    content: Optional[Union[Message, str, List[Union[RefNode, CustomNode]]]]

class Card(Segment):
    type: Literal["xml", "json"]
    raw: str

class Other(Segment):
    """其他 Segment"""
```

此类消息段通过 `UniMessage.export` 可以转为特定的 `MessageSegment`.

### 通用信息序列

`uniseg` 模块还提供了一个类似于 `Message` 的 `UniMessage` 类型，其元素为经过通用标注转换后的通用消息段.

你可以通过提供的 `UniversalMessage` 或 `UniMsg` 依赖注入器来获取 `UniMessage`.

```python
from nonebot_plugin_alconna.uniseg import UniMsg, At, Reply


matcher = on_xxx(...)

@matcher.handle()
async def _(msg: UniMsg):
    reply = msg[Reply, 0]
    print(reply.origin)
    if msg.has(At):
        ats = msg.get(At)
        print(ats)
    ...
```

还可以通过 `UniMessage` 的 `export` 与 `send` 方法来**跨平台发送消息**.

```python
from nonebot import Bot, on_command
from nonebot_plugin_alconna.uniseg import Image, UniMessage


test = on_command("test")

@test.handle()
async def handle_test():
    await test.send(await UniMessage(Image(path="path/to/img")).export())
```

`UniMessage.export` 会通过传入的 `bot: Bot` 参数，或上下文中的 `Bot` 对象读取适配器信息，并使用对应的生成方法把通用消息转为适配器对应的消息序列.

而在 `AlconnaMatcher` 下，`got`, `send`, `reject` 等可以发送消息的方法皆支持使用 `UniMessage`，不需要手动调用 export 方法：

```python
from arclet.alconna import Alconna, Args
from nonebot_plugin_alconna import Match, AlconnaMatcher, on_alconna
from nonebot_plugin_alconna.uniseg import At,  UniMessage


test_cmd = on_alconna(Alconna("test", Args["target?", At]))

@test_cmd.handle()
async def tt_h(matcher: AlconnaMatcher, target: Match[At]):
    if target.available:
        matcher.set_path_arg("target", target.result)

@test_cmd.got_path("target", prompt="请输入目标")
async def tt(target: At):
    await test_cmd.send(UniMessage([target, "\ndone."]))
```

除此之外 `UniMessage.send` 方法基于 `UniMessage.export` 并调用各适配器下的发送消息方法，返回一个 `Receipt` 对象，用于修改/撤回消息：

```python
from nonebot import Bot, on_command
from nonebot_plugin_alconna.uniseg import UniMessage


test = on_command("test")

@test.handle()
async def handle():
    receipt = await UniMessage.text("hello!").send(at_sender=True, reply_to=True)
    await receipt.recall(delay=1)
```

在响应器以外的地方，`bot` 参数必须手动传入

本插件为以下设配器提供了 **Segment** 标注，可用于匹配各适配器的 `MessageSegment`，也可用于创建 `MessageSegment`:

| 协议名称                                                            | 路径                                 |
| ------------------------------------------------------------------- | ------------------------------------ |
| [OneBot 协议](https://github.com/nonebot/adapter-onebot)            | adapters.onebot11, adapters.onebot12 |
| [Telegram](https://github.com/nonebot/adapter-telegram)             | adapters.telegram                    |
| [飞书](https://github.com/nonebot/adapter-feishu)                   | adapters.feishu                      |
| [GitHub](https://github.com/nonebot/adapter-github)                 | adapters.github                      |
| [QQ bot](https://github.com/nonebot/adapter-qq)                     | adapters.qq                          |
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
| [Satori](https://github.com/nonebot/adapter-satori)                 | adapters.satori                      |
| [Dodo IM](https://github.com/nonebot/adapter-dodo)                  | adapters.dodo                        |

#### 构造

类比 `Message`, `UniMessage` 可以传入单个字符串/消息段或可迭代的字符串/消息段：

```python
from nonebot_plugin_alconna.uniseg import UniMessage, At


msg = UniMessage("Hello")
msg1 = UniMessage(At("user", "124"))
msg2 = UniMessage(["Hello", At("user", "124")])
```

`UniMessage` 上同时存在便捷方法，令其可以链式地添加消息段：

```python
from nonebot_plugin_alconna.uniseg import UniMessage, At, Image


msg = UniMessage.text("Hello").at("124").image(path="/path/to/img")
assert msg == UniMessage(
    ["Hello", At("user", "124"), Image(path="/path/to/img")]
)
```

#### 拼接消息

`str`、`UniMessage`、`Segment` 对象之间可以直接相加，相加均会返回一个新的 `UniMessage` 对象.

```python
# 消息序列与消息段相加
UniMessage("text") + Text("text")
# 消息序列与字符串相加
UniMessage([Text("text")]) + "text"
# 消息序列与消息序列相加
UniMessage("text") + UniMessage([Text("text")])
# 字符串与消息序列相加
"text" + UniMessage([Text("text")])
# 消息段与消息段相加
Text("text") + Text("text")
# 消息段与字符串相加
Text("text") + "text"
# 消息段与消息序列相加
Text("text") + UniMessage([Text("text")])
# 字符串与消息段相加
"text" + Text("text")
```

如果需要在当前消息序列后直接拼接新的消息段，可以使用 `Message.append`、`Message.extend` 方法，或者使用自加.

```python
msg = UniMessage([Text("text")])
# 自加
msg += "text"
msg += Text("text")
msg += UniMessage([Text("text")])
# 附加
msg.append(Text("text"))
# 扩展
msg.extend([Text("text")])
```

#### 使用消息模板

`UniMessage.template` 同样类似于 `Message.template`，可以用于格式化消息。大体用法参考 [消息模板](https://nonebot.dev/docs/next/tutorial/message#%E4%BD%BF%E7%94%A8%E6%B6%88%E6%81%AF%E6%A8%A1%E6%9D%BF).

这里额外说明 `UniMessage.template` 的拓展控制符.

相比 `Message`，UniMessage 对于 {:XXX} 做了另一类拓展。其能够识别例如 At(xxx, yyy) 或 Emoji(aaa, bbb)的字符串并执行.

以 At(...) 为例使用通用消息段的拓展控制符：

```python
>>> from nonebot_plugin_alconna.uniseg import UniMessage
>>>  UniMessage.template("{:At(user, target)}").format(target="123")
UniMessage(At("user", "123"))
>>> UniMessage.template("{:At(type=user, target=id)}").format(id="123")
UniMessage(At("user", "123"))
>>> UniMessage.template("{:At(type=user, target=123)}").format()
UniMessage(At("user", "123"))
```

而在 `AlconnaMatcher` 中，{:XXX} 更进一步地提供了获取 `event` 和 `bot` 中的属性的功能.

在AlconnaMatcher中使用通用消息段的拓展控制符:

```python
from arclet.alconna import Alconna, Args
from nonebot_plugin_alconna import At, Match, UniMessage, AlconnaMatcher, on_alconna


test_cmd = on_alconna(Alconna("test", Args["target?", At]))

@test_cmd.handle()
async def tt_h(matcher: AlconnaMatcher, target: Match[At]):
    if target.available:
        matcher.set_path_arg("target", target.result)

@test_cmd.got_path(
    "target",
    prompt=UniMessage.template("{:At(user, $event.get_user_id())} 请确认目标")
)
async def tt():
    await test_cmd.send(
      UniMessage.template("{:At(user, $event.get_user_id())} 已确认目标为 {target}")
    )
```

另外也有 `$message_id` 与 `$target` 两个特殊值

#### 检查消息段

我们可以通过 `in` 运算符或消息序列的 `has` 方法来：

```python
# 是否存在消息段
At("user", "1234") in message
# 是否存在指定类型的消息段
At in message
```

我们还可以使用 `only` 方法来检查消息中是否仅包含指定的消息段。

```python
# 是否都为 "test"
message.only("test")
# 是否仅包含指定类型的消息段
message.only(Text)
```

#### 获取消息纯文本

类似于 `Message.extract_plain_text()`，用于获取通用消息的纯文本.

```python
from nonebot_plugin_alconna.uniseg import UniMessage, At


# 提取消息纯文本字符串
assert UniMessage(
    [At("user", "1234"), "text"]
).extract_plain_text() == "text"
```

#### 遍历

通用消息序列继承自 `List[Segment]` ，因此可以使用 `for` 循环遍历消息段。

```python
for segment in message:  # type: Segment
	...
```

#### 过滤、索引与切片

消息序列对列表的索引与切片进行了增强，在原有列表 `int` 索引与 `slice` 切片的基础上，支持 `type` 过滤索引与切片.

```python
from nonebot_plugin_alconna.uniseg import UniMessage, At, Text, Reply


message = UniMessage(
    [
        Reply(...),
        "text1",
        At("user", "1234"),
        "text2"
    ]
)
# 索引
message[0] == Reply(...)
# 切片
message[0:2] == UniMessage([Reply(...), Text("text1")])
# 类型过滤
message[At] == Message([At("user", "1234")])
# 类型索引
message[At, 0] == At("user", "1234")
# 类型切片
message[Text, 0:2] == UniMessage([Text("text1"), Text("text2")])
```

我们也可以通过消息序列的 `include`、`exclude` 方法进行类型过滤.

```python
message.include(Text, At)
message.exclude(Reply)
```

同样的，消息序列对列表的 `index`、`count` 方法也进行了增强，可以用于索引指定类型的消息段.

```python
# 指定类型首个消息段索引
message.index(Text) == 1
# 指定类型消息段数量
message.count(Text) == 2
```

此外，消息序列添加了一个 `get` 方法，可以用于获取指定类型指定个数的消息段.

```python
# 获取指定类型指定个数的消息段
message.get(Text, 1) == UniMessage([Text("test1")])
```

#### 消息发送

通用消息可用 `UniMessage.send` 发送自身：

```python
async def send(
    self,
    target: Union[Event, Target, None] = None,
    bot: Optional[Bot] = None,
    fallback: bool = True,
    at_sender: Union[str, bool] = False,
    reply_to: Union[str, bool] = False,
) -> Receipt:
```

实际上，`UniMessage` 同时提供了获取消息事件 id 与消息发送对象的方法:

```python
from nonebot import Event, Bot
from nonebot_plugin_alconna.uniseg import UniMessage, Target


matcher = on_xxx(...)

@matcher.handle()
asycn def _(bot: Bot, event: Event):
    target: Target = UniMessage.get_target(event, bot)
    msg_id: str = UniMessage.get_message_id(event, bot)

```

`send`, `get_target`, `get_message_id` 中与 `event`, `bot` 相关的参数都会尝试从上下文中获取对象.

其中，`Target`:

```python
class Target:
    id: str
    """目标id；若为群聊则为group_id或者channel_id，若为私聊则为user_id"""
    parent_id: str = ""
    """父级id；若为频道则为guild_id，其他情况为空字符串"""
    channel: bool = False
    """是否为频道，仅当目标平台同时支持群聊和频道时有效"""
    private: bool = False
    """是否为私聊"""
    source: str = ""
    """可能的事件id"""
```

是用来描述响应消息时的发送对象.

同样的，你可以通过依赖注入的方式在响应器中直接获取它们.

## 条件控制

本插件可以通过 `assign` 来控制一个具体的响应函数是否在不满足条件时跳过响应

```python
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

## 响应器创建装饰

本插件提供了一个 `funcommand` 装饰器, 其用于将一个接受任意参数， 返回 `str` 或 `Message` 或 `MessageSegment` 的函数转换为命令响应器.

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

## 类Koishi构造器

本插件提供了一个 `Command` 构造器，其基于 `arclet.alconna.tools` 中的 `AlconnaString`， 以类似 `Koishi` 中注册命令的方式来构建一个 **AlconnaMatcher** :

```python
from nonebot_plugin_alconna import Command, Arparma


book = (
    Command("book", "测试")
    .option("writer", "-w <id:int>")
    .option("writer", "--anonymous", {"id": 0})
    .usage("book [-w <id:int> | --anonymous]")
    .shortcut("测试", {"args": ["--anonymous"]})
    .build()
)

@book.handle()
async def _(arp: Arparma):
    await book.send(str(arp.options))
```

甚至，你可以设置 `action` 来设定响应行为：

```python
book = (
    Command("book", "测试")
    .option("writer", "-w <id:int>")
    .option("writer", "--anonymous", {"id": 0})
    .usage("book [-w <id:int> | --anonymous]")
    .shortcut("测试", {"args": ["--anonymous"]})
    .action(lambda options: str(options))  # 会自动通过 bot.send 发送
    .build()
)
```

## 返回值回调

在 `AlconnaMatch`, `AlconnaQuery` 或 `got_path` 中，你可以使用 `middleware` 参数来传入一个对返回值进行处理的函数:

```python
from nonebot_plugin_alconna import image_fetch


mask_cmd = on_alconna(
    Alconna("search", Args["img?", Image]),
)


@mask_cmd.handle()
async def mask_h(matcher: AlconnaMatcher, img: Match[bytes] = AlconnaMatch("img", image_fetch)):
    result = await search_img(img.result)
    await matcher.send(result.content)
```

其中，`image_fetch` 是一个中间件，其接受一个 `Image` 对象，并提取图片的二进制数据返回.

## 匹配拓展

本插件提供了一个 `Extension` 类，其用于自定义 AlconnaMatcher 的部分行为.

例如 `LLMExtension` (仅举例)：

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

那么添加了 `LLMExtension` 的响应器便能接受任何能通过 llm 翻译为具体命令的自然语言消息，同时可以在响应器中为所有 `llm` 参数注入模型变量

目前 `Extension` 的功能有:

- `validate`: 对于事件的来源适配器或 bot 选择是否接受响应
- `output_converter`: 输出信息的自定义转换方法
- `message_provider`: 从传入事件中自定义提取消息的方法
- `receive_provider`: 对传入的消息 (Message 或 UniMessage) 的额外处理
- `permission_check`: 命令对消息解析并确认头部匹配（即确认选择响应）时对发送者的权限判断
- `parse_wrapper`: 对命令解析结果的额外处理
- `send_wrapper`: 对发送的消息 (Message 或 UniMessage) 的额外处理
- `before_catch`: 自定义依赖注入的绑定确认函数
- `catch`: 自定义依赖注入处理函数
- `post_init`: 响应器创建后对命令对象的额外处理

例如内置的 `DiscordSlashExtension`，其可自动将 Alconna 对象翻译成 slash 指令并注册，且将收到的指令交互事件转为指令供命令解析:

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
