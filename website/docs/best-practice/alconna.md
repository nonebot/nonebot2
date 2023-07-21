---
sidebar_position: 6
description: Alconna 命令解析拓展
---

# Alconna 命令解析

[`nonebot-plugin-alconna`](https://github.com/nonebot/plugin-alconna) 是一类提供了拓展响应规则的插件。
该插件使用 [Alconna](https://github.com/ArcletProject/Alconna) 作为命令解析器，
是一个简单、灵活、高效的命令参数解析器, 并且不局限于解析命令式字符串。

特点包括:

- 高效
- 直观的命令组件创建方式
- 强大的类型解析与类型转换功能
- 自定义的帮助信息格式
- 多语言支持
- 易用的快捷命令创建与使用
- 可创建命令补全会话, 以实现多轮连续的补全提示
- 可嵌套的多级子命令
- 正则匹配支持

该插件提供了一类新的事件响应器辅助函数 `on_alconna`，以及 `AlconnaResult` 等依赖注入函数。

同时，基于 [Annotated 支持](https://github.com/nonebot/nonebot2/pull/1832), 添加了两类注解 `AlcMatches` 与 `AlcResult`

该插件还可以通过 `handle(parameterless)` 来控制一个具体的响应函数是否在不满足条件时跳过响应：

- `pip.handle([Check(assign("add.name", "nb"))])` 表示仅在命令为 `role-group add` 并且 name 为 `nb` 时响应
- `pip.handle([Check(assign("list"))])` 表示仅在命令为 `role-group list` 时响应
- `pip.handle([Check(assign("add"))])` 表示仅在命令为 `role-group add` 时响应

基于 `Alconna` 的特性，该插件同时提供了一系列便捷的消息段标注。
标注可用于在 `Alconna` 中匹配消息中除 text 外的其他消息段，也可用于快速创建各适配器下的消息段。所有标注位于 `nonebot_plugin_alconna.adapters` 中。

## 安装插件

在使用前请先安装 `nonebot-plugin-alconna` 插件至项目环境中，可参考[获取商店插件](../tutorial/store.mdx#安装插件)来了解并选择安装插件的方式。如：

在**项目目录**下执行以下命令：

```shell
nb plugin install nonebot-plugin-alconna
```

或

```shell
pip install nonebot-plugin-alconna
```

## 使用插件

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

### 导入插件

由于 `nonebot-plugin-alconna` 作为插件，因此需要在使用前对其进行**加载**并**导入**其中的 `on_alconna` 来使用命令拓展。使用 `require` 方法可轻松完成这一过程，可参考 [跨插件访问](../advanced/requiring.md) 一节进行了解。

```python
from nonebot import require

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import on_alconna
```

### 命令编写

我们可以看到主要的两大组件：`Option` 与 `Subcommand`。

`Option` 可以传入一组别名，如 `Option("--foo|-F|--FOO|-f")` 或 `Option("--foo", alias=["-F"]`

`Subcommand` 则可以传入自己的 `Option` 与 `Subcommand`：

他们拥有如下共同参数：

- `help_text`: 传入该组件的帮助信息
- `dest`: 被指定为解析完成时标注匹配结果的标识符，不传入时默认为选项或子命令的名称 (name)
- `requires`: 一段指定顺序的字符串列表，作为唯一的前置序列与命令嵌套替换
- `default`: 默认值，在该组件未被解析时使用使用该值替换。

然后是 `Args` 与 `MultiVar`，他们是用于解析参数的组件。

`Args` 是参数解析的基础组件，构造方法形如 `Args["foo", str]["bar", int]["baz", bool, False]`，
与函数签名类似，但是允许含有默认值的参数在前；同时支持 keyword-only 参数不依照构造顺序传入 （但是仍需要在非 keyword-only 参数之后）。

`MultiVar` 则是一个特殊的标注，用于告知解析器该参数可以接受多个值，其构造方法形如 `MultiVar(str)`。
同样的还有 `KeyWordVar`，其构造方法形如 `KeyWordVar(str)`，用于告知解析器该参数为一个 keyword-only 参数。

:::tip
`MultiVar` 与 `KeyWordVar` 组合时，代表该参数为一个可接受多个 key-value 的参数，其构造方法形如 `MultiVar(KeyWordVar(str))`

`MultiVar` 与 `KeyWordVar` 也可以传入 `default` 参数，用于指定默认值。

`MultiVar` 不能在 `KeyWordVar` 之后传入。
:::

### 参数标注

`Args` 的参数类型表面上看需要传入一个 `type`，但实际上它需要的是一个 `nepattern.BasePattern` 的实例。

```python
from arclet.alconna import Args
from nepattern import BasePattern

# 表示 foo 参数需要匹配一个 @number 样式的字符串
args = Args["foo", BasePattern("@\d+")]
```

示例中传入的 `str` 是因为 `str` 已经注册在了 `nepattern.global_patterns` 中，因此会替换为 `nepattern.global_patterns[str]`。

默认支持的类型有：

- `str`: 匹配任意字符串
- `int`: 匹配整数
- `float`: 匹配浮点数
- `bool`: 匹配 `True` 与 `False` 以及他们小写形式
- `hex`: 匹配 `0x` 开头的十六进制字符串
- `url`: 匹配网址
- `email`: 匹配 `xxxx@xxx` 的字符串
- `ipv4`: 匹配 `xxx.xxx.xxx.xxx` 的字符串
- `list`: 匹配类似 `["foo","bar","baz"]` 的字符串
- `dict`: 匹配类似 `{"foo":"bar","baz":"qux"}` 的字符串
- `datetime`: 传入一个 `datetime` 支持的格式字符串，或时间戳
- `Any`: 匹配任意类型
- `AnyString`: 匹配任意类型，转为 `str`
- `Number`: 匹配 `int` 与 `float`，转为 `int`

同时可以使用 typing 中的类型：

- `Literal[X]`: 匹配其中的任意一个值
- `Union[X, Y]`: 匹配其中的任意一个类型
- `Optional[xxx]`: 会自动将默认值设为 `None`，并在解析失败时使用默认值
- `List[X]`: 匹配一个列表，其中的元素为 `X` 类型
- `Dict[X, Y]`: 匹配一个字典，其中的 key 为 `X` 类型，value 为 `Y` 类型
- ...

:::tip
几类特殊的传入标记：

- `"foo"`: 匹配字符串 "foo" (若没有某个 `BasePattern` 与之关联)
- `RawStr("foo")`: 匹配字符串 "foo" (不会被 `BasePattern` 替换)
- `"foo|bar|baz"`: 匹配 "foo" 或 "bar" 或 "baz"
- `[foo, bar, Baz, ...]`: 匹配其中的任意一个值或类型
- `Callable[[X], Y]`: 匹配一个参数为 `X` 类型的值，并返回通过该函数调用得到的 `Y` 类型的值
- `"re:xxx"`: 匹配一个正则表达式 `xxx`，会返回 Match[0]
- `"rep:xxx"`: 匹配一个正则表达式 `xxx`，会返回 `re.Match` 对象
- `{foo: bar, baz: qux}`: 匹配字典中的任意一个键, 并返回对应的值 (特殊的键 ... 会匹配任意的值)
- ...

:::

### 消息段标注

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

### 响应器使用

`on_alconna` 的所有参数如下：

- `command: Alconna | str`: Alconna 命令
- `skip_for_unmatch: bool = True`: 是否在命令不匹配时跳过该响应
- `auto_send_output: bool = False`: 是否自动发送输出信息并跳过响应
- `output_converter: TConvert | None = None`: 输出信息字符串转换为消息序列方法
- `aliases: set[str | tuple[str, ...]] | None = None`: 命令别名， 作用类似于 `on_command` 中的 aliases
- `comp_config: CompConfig | None = None`: 补全会话配置， 不传入则不启用补全会话

`AlconnaMatches` 是一个依赖注入函数，可注入 `Alconna` 命令解析结果。

### 配置项

#### alconna_auto_send_output

- **类型**: `bool`
- **默认值**: `False`

"是否全局启用输出信息自动发送，不启用则会在触特殊内置选项后仍然将解析结果传递至响应器。

#### alconna_use_command_start

- **类型**: `bool`
- **默认值**: `False`

是否读取 Nonebot 的配置项 `COMMAND_START` 来作为全局的 Alconna 命令前缀

#### alconna_auto_completion

- **类型**: `bool`
- **默认值**: `False`

是否全局启用命令自动补全，启用后会在参数缺失或触发 `--comp` 选项时自自动启用交互式补全。

## 文档参考

插件文档: [📦 这里](https://github.com/nonebot/plugin-alconna/blob/master/docs.md)

官方文档: [👉 指路](https://arclet.top/)

QQ 交流群: [🔗 链接](https://jq.qq.com/?_wv=1027&k=PUPOnCSH)

友链: [📚 文档](https://graiax.cn/guide/message_parser/alconna.html)
