---
sidebar_position: 2
description: Alconna 基本介绍
---

# Alconna 本体

[`Alconna`](https://github.com/ArcletProject/Alconna) 隶属于 `ArcletProject`，是一个简单、灵活、高效的命令参数解析器, 并且不局限于解析命令式字符串。

我们先通过一个例子来讲解 **Alconna** 的核心 —— `Args`, `Subcommand`, `Option`：

```python
from arclet.alconna import Alconna, Args, Subcommand, Option


alc = Alconna(
    "pip",
    Subcommand(
        "install",
        Args["package", str],
        Option("-r|--requirement", Args["file", str]),
        Option("-i|--index-url", Args["url", str]),
    )
)

res = alc.parse("pip install nonebot2 -i URL")

print(res)
# matched=True, header_match=(origin='pip' result='pip' matched=True groups={}), subcommands={'install': (value=Ellipsis args={'package': 'nonebot2'} options={'index-url': (value=None args={'url': 'URL'})} subcommands={})}, other_args={'package': 'nonebot2', 'url': 'URL'}

print(res.all_matched_args)
# {'package': 'nonebot2', 'url': 'URL'}
```

这段代码通过`Alconna`创捷了一个接受主命令名为`pip`, 子命令为`install`且子命令接受一个 **Args** 参数`package`和二个 **Option** 参数`-r`和`-i`的命令参数解析器, 通过`parse`方法返回解析结果 **Arparma** 的实例。

## 命令头

命令头是指命令的前缀 (Prefix) 与命令名 (Command) 的组合，例如 !help 中的 ! 与 help。

命令构造时, `Alconna([prefix], command)` 与 `Alconna(command, [prefix])` 是等价的。

|             前缀             |   命令名   |                          匹配内容                           |       说明       |
| :--------------------------: | :--------: | :---------------------------------------------------------: | :--------------: |
|            不传入            |   "foo"    |                           `"foo"`                           | 无前缀的纯文字头 |
|            不传入            |    123     |                            `123`                            |  无前缀的元素头  |
|            不传入            | "re:\d{2}" |                           `"32"`                            |  无前缀的正则头  |
|            不传入            |    int     |                      `123` 或 `"456"`                       |  无前缀的类型头  |
|         [int, bool]          |   不传入   |                       `True` 或 `123`                       |  无名的元素类头  |
|        ["foo", "bar"]        |   不传入   |                     `"foo"` 或 `"bar"`                      |  无名的纯文字头  |
|        ["foo", "bar"]        |   "baz"    |                  `"foobaz"` 或 `"barbaz"`                   |     纯文字头     |
|         [int, bool]          |   "foo"    |             `[123, "foo"]` 或 `[False, "foo"]`              |      类型头      |
|         [123, 4567]          |   "foo"    |              `[123, "foo"]` 或 `[4567, "foo"]`              |      元素头      |
|      [nepattern.NUMBER]      |   "bar"    |            `[123, "bar"]` 或 `[123.456, "bar"]`             |     表达式头     |
|         [123, "foo"]         |   "bar"    |      `[123, "bar"]` 或 `"foobar"` 或 `["foo", "bar"]`       |      混合头      |
| [(int, "foo"), (456, "bar")] |   "baz"    | `[123, "foobaz"]` 或 `[456, "foobaz"]` 或 `[456, "barbaz"]` |       对头       |

对于无前缀的类型头，此时会将传入的值尝试转为 BasePattern，例如 `int` 会转为 `nepattern.INTEGER`。如此该命令头会匹配对应的类型， 例如 `int` 会匹配 `123` 或 `"456"`，但不会匹配 `"foo"`。解析后，Alconna 会将命令头匹配到的值转为对应的类型，例如 `int` 会将 `"123"` 转为 `123`。

:::tip

**正则内容只在命令名上生效，前缀中的正则会被转义**

:::

除了通过传入 `re:xxx` 来使用正则表达式外，Alconna 还提供了一种更加简洁的方式来使用正则表达式，称为 Bracket Header：

```python
alc = Alconna(".rd{roll:int}")
assert alc.parse(".rd123").header["roll"] == 123
```

Bracket Header 类似 python 里的 f-string 写法，通过 `"{}"` 声明匹配类型

`"{}"` 中的内容为 "name:type or pat"：

- `"{}"`, `"{:}"` ⇔ `"(.+)"`, 占位符
- `"{foo}"` ⇔ `"(?P&lt;foo&gt;.+)"`
- `"{:\d+}"` ⇔ `"(\d+)"`
- `"{foo:int}"` ⇔ `"(?P&lt;foo&gt;\d+)"`，其中 `"int"` 部分若能转为 `BasePattern` 则读取里面的表达式

## 参数声明(Args)

`Args` 是用于声明命令参数的组件， 可以通过以下几种方式构造 **Args** ：

- `Args[key, var, default][key1, var1, default1][...]`
- `Args[(key, var, default)]`
- `Args.key[var, default]`

其中，key **一定**是字符串，而 var 一般为参数的类型，default 为具体的值或者 **arclet.alconna.args.Field**

其与函数签名类似，但是允许含有默认值的参数在前；同时支持 keyword-only 参数不依照构造顺序传入 （但是仍需要在非 keyword-only 参数之后）。

### key

`key` 的作用是用以标记解析出来的参数并存放于 **Arparma** 中，以方便用户调用。

其有三种为 Args 注解的标识符: `?`、`/`、 `!`, 标识符与 key 之间建议以 `;` 分隔：

- `!` 标识符表示该处传入的参数应**不是**规定的类型，或**不在**指定的值中。
- `?` 标识符表示该参数为**可选**参数，会在无参数匹配时跳过。
- `/` 标识符表示该参数的类型注解需要隐藏。

另外，对于参数的注释也可以标记在 `key` 中，其与 key 或者标识符 以 `#` 分割：  
`foo#这是注释;?` 或 `foo?#这是注释`

:::tip

`Args` 中的 `key` 在实际命令中并不需要传入（keyword 参数除外）：

```python
from arclet.alconna import Alconna, Args


alc = Alconna("test", Args["foo", str])
alc.parse("test --foo abc") # 错误
alc.parse("test abc") # 正确
```

若需要 `test --foo abc`，你应该使用 `Option`：

```python
from arclet.alconna import Alconna, Args, Option


alc = Alconna("test", Option("--foo", Args["foo", str]))
```

:::

### var

var 负责命令参数的**类型检查**与**类型转化**

`Args` 的`var`表面上看需要传入一个 `type`，但实际上它需要的是一个 `nepattern.BasePattern` 的实例：

```python
from arclet.alconna import Args
from nepattern import BasePattern


# 表示 foo 参数需要匹配一个 @number 样式的字符串
args = Args["foo", BasePattern("@\d+")]
```

`pip` 示例中可以传入 `str` 是因为 `str` 已经注册在了 `nepattern.global_patterns` 中，因此会替换为 `nepattern.global_patterns[str]`

`nepattern.global_patterns`默认支持的类型有：

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
- `RawStr("foo")`: 匹配字符串 "foo" (即使有 `BasePattern` 与之关联也不会被替换)
- `"foo|bar|baz"`: 匹配 "foo" 或 "bar" 或 "baz"
- `[foo, bar, Baz, ...]`: 匹配其中的任意一个值或类型
- `Callable[[X], Y]`: 匹配一个参数为 `X` 类型的值，并返回通过该函数调用得到的 `Y` 类型的值
- `"re:xxx"`: 匹配一个正则表达式 `xxx`，会返回 Match[0]
- `"rep:xxx"`: 匹配一个正则表达式 `xxx`，会返回 `re.Match` 对象
- `{foo: bar, baz: qux}`: 匹配字典中的任意一个键, 并返回对应的值 (特殊的键 ... 会匹配任意的值)
- ...

**特别的**，你可以不传入 `var`，此时会使用 `key` 作为 `var`, 匹配 `key` 字符串。

:::

#### MultiVar 与 KeyWordVar

`MultiVar` 是一个特殊的标注，用于告知解析器该参数可以接受多个值，类似于函数中的 `*args`，其构造方法形如 `MultiVar(str)`。

同样的还有 `KeyWordVar`，类似于函数中的 `*, name: type`，其构造方法形如 `KeyWordVar(str)`，用于告知解析器该参数为一个 keyword-only 参数。

:::tip

`MultiVar` 与 `KeyWordVar` 组合时，代表该参数为一个可接受多个 key-value 的参数，类似于函数中的 `**kwargs`，其构造方法形如 `MultiVar(KeyWordVar(str))`

`MultiVar` 与 `KeyWordVar` 也可以传入 `default` 参数，用于指定默认值

`MultiVar` 不能在 `KeyWordVar` 之后传入

:::

#### AllParam

`AllParam` 是一个特殊的标注，用于告知解析器该参数接收命令中在此位置之后的所有参数并**结束解析**，可以认为是**泛匹配参数**。

`AllParam` 可直接使用 (`Args["xxx", AllParam]`), 也可以传入指定的接收类型 (`Args["xxx", AllParam(str)]`)。

:::tip

在 `nonebot_plugin_alconna` 下，`AllParam` 的返回值为 [`UniMessage`](./uniseg/message.mdx)

:::

### default

`default` 传入的是该参数的默认值或者 `Field`，以携带对于该参数的更多信息。

默认情况下 (即不声明) `default` 的值为特殊值 `Empty`。这也意味着你可以将默认值设置为 `None` 表示默认值为空值。

`Field` 构造需要的参数说明如下：

- default: 参数单元的默认值
- alias: 参数单元默认值的别名
- completion: 参数单元的补全说明生成函数
- unmatch_tips: 参数单元的错误提示生成函数，其接收一个表示匹配失败的元素的参数
- missing_tips: 参数单元的缺失提示生成函数

## 选项与子命令(Option & Subcommand)

`Option` 和 `Subcommand` 可以传入一组 `alias`，如 `Option("--foo|-F|--FOO|-f")`，`Subcommand("foo", alias=["F"])`

传入别名后，选项与子命令会选择其中长度最长的作为其名称。若传入为 "--foo|-f"，则命令名称为 "--foo"

:::tip 特别提醒!!!

Option 的名字或别名**没有要求**必须在前面写上 `-`

Option 与 Subcommand 的唯一区别在于 Subcommand 可以传入自己的 **Option** 与 **Subcommand**

:::

他们拥有如下共同参数：

- `help_text`: 传入该组件的帮助信息
- `dest`: 被指定为解析完成时标注匹配结果的标识符，不传入时默认为选项或子命令的名称 (name)
- `requires`: 一段指定顺序的字符串列表，作为唯一的前置序列与命令嵌套替换
  对于命令 `test foo bar baz qux <a:int>` 来讲，因为`foo bar baz` 仅需要判断是否相等, 所以可以这么编写：

```python
Alconna("test", Option("qux", Args.a[int], requires=["foo", "bar", "baz"]))
```

- `default`: 默认值，在该组件未被解析时使用使用该值替换。
  特别的，使用 `OptionResult` 或 `SubcomanndResult` 可以设置包括参数字典在内的默认值：

```python
from arclet.alconna import Option, OptionResult

opt1 = Option("--foo", default=False)
opt2 = Option("--foo", default=OptionResult(value=False, args={"bar": 1}))
```

### Action

`Option` 可以特别设置传入一类 `Action`，作为解析操作

`Action` 分为三类：

- `store`: 无 Args 时， 仅存储一个值， 默认为 Ellipsis； 有 Args 时， 后续的解析结果会覆盖之前的值
- `append`: 无 Args 时， 将多个值存为列表， 默认为 Ellipsis； 有 Args 时， 每个解析结果会追加到列表中, 当存在默认值并且不为列表时， 会自动将默认值变成列表， 以保证追加的正确性
- `count`: 无 Args 时， 计数器加一； 有 Args 时， 表现与 STORE 相同, 当存在默认值并且不为数字时， 会自动将默认值变成 1， 以保证计数器的正确性。

`Alconna` 提供了预制的几类 `Action`：

- `store`(默认)，`store_value`，`store_true`，`store_false`
- `append`，`append_value`
- `count`

## 解析结果

`Alconna.parse` 会返回由 **Arparma** 承载的解析结果

`Arparma` 有如下属性：

- 调试类
  - matched: 是否匹配成功
  - error_data: 解析失败时剩余的数据
  - error_info: 解析失败时的异常内容
  - origin: 原始命令，可以类型标注

- 分析类
  - header_match: 命令头部的解析结果，包括原始头部、解析后头部、解析结果与可能的正则匹配组
  - main_args: 命令的主参数的解析结果
  - options: 命令所有选项的解析结果
  - subcommands: 命令所有子命令的解析结果
  - other_args: 除主参数外的其他解析结果
  - all_matched_args: 所有 Args 的解析结果

### 路径查询

`Arparma` 同时提供了便捷的查询方法 `query[type]()`，会根据传入的 `path` 查找参数并返回

`path` 支持如下:

- `main_args`, `options`, ...: 返回对应的属性
- `args`: 返回 all_matched_args
- `args.<key>`: 返回 all_matched_args 中 `key` 键对应的值
- `main_args.<key>`: 返回主命令的解析参数字典中 `key` 键对应的值
- `<node>`: 返回选项/子命令 `node` 的解析结果 (OptionResult | SubcommandResult)
- `<node>.value`: 返回选项/子命令 `node` 的解析值
- `<node>.args`: 返回选项/子命令 `node` 的解析参数字典
- `<node>.<key>`, `<node>.args.<key>`: 返回选项/子命令 `node` 的参数字典中 `key` 键对应的值

以及:

- `options.<opt>`: 返回选项 `opt` 的解析结果 (OptionResult)
- `options.<opt>.value`: 返回选项 `opt` 的解析值
- `options.<opt>.args`: 返回选项 `opt` 的解析参数字典
- `options.<opt>.<key>`, `options.<node>.args.<key>`: 返回选项 `opt` 的参数字典中 `key` 键对应的值
- `subcommands.<subcmd>`: 返回子命令 `subcmd` 的解析结果 (SubcommandResult)
- `subcommands.<subcmd>.value`: 返回子命令 `subcmd` 的解析值
- `subcommands.<subcmd>.args`: 返回子命令 `subcmd` 的解析参数字典
- `subcommands.<subcmd>.<key>`, `subcommands.<node>.args.<key>`: 返回子命令 `subcmd` 的参数字典中 `key` 键对应的值

## 元数据(CommandMeta)

`Alconna` 的元数据相当于其配置，拥有以下条目：

- `description`: 命令的描述
- `usage`: 命令的用法
- `example`: 命令的使用样例
- `author`: 命令的作者
- `fuzzy_match`: 命令是否开启模糊匹配
- `fuzzy_threshold`: 模糊匹配阈值
- `raise_exception`: 命令是否抛出异常
- `hide`: 命令是否对 manager 隐藏
- `hide_shortcut`: 命令的快捷指令是否在 help 信息中隐藏
- `keep_crlf`: 命令解析时是否保留换行字符
- `compact`: 命令是否允许第一个参数紧随头部
- `strict`: 命令是否严格匹配，若为 False 则未知参数将作为名为 $extra 的参数
- `context_style`: 命令上下文插值的风格，None 为关闭，bracket 为 `{...}`，parentheses 为 `$(...)`
- `extra`: 命令的自定义额外信息

元数据一定使用 `meta=...` 形式传入：

```python
from arclet.alconna import Alconna, CommandMeta

alc = Alconna(..., meta=CommandMeta("foo", example="bar"))
```

## 命名空间配置

命名空间配置 （以下简称命名空间） 相当于 `Alconna` 的默认配置，其优先度低于 `CommandMeta`。

`Alconna` 默认使用 "Alconna" 命名空间。

命名空间有以下几个属性：

- name: 命名空间名称
- prefixes: 默认前缀配置
- separators: 默认分隔符配置
- formatter_type: 默认格式化器类型
- fuzzy_match: 默认是否开启模糊匹配
- raise_exception: 默认是否抛出异常
- builtin_option_name: 默认的内置选项名称(--help, --shortcut, --comp)
- disable_builtin_options: 默认禁用的内置选项(--help, --shortcut, --comp)
- enable_message_cache: 默认是否启用消息缓存
- compact: 默认是否开启紧凑模式
- strict: 命令是否严格匹配
- context_style: 命令上下文插值的风格
- ...

### 新建命名空间并替换

```python
from arclet.alconna import Alconna, namespace, Namespace, Subcommand, Args, config


ns = Namespace("foo", prefixes=["/"])  # 创建 "foo"命名空间配置, 它要求创建的Alconna的主命令前缀必须是/

alc = Alconna("pip", Subcommand("install", Args["package", str]), namespace=ns) # 在创建Alconna时候传入命名空间以替换默认命名空间

# 可以通过with方式创建命名空间
with namespace("bar") as np1:
    np1.prefixes = ["!"]    # 以上下文管理器方式配置命名空间，此时配置会自动注入上下文内创建的命令
    np1.formatter_type = ShellTextFormatter  # 设置此命名空间下的命令的 formatter 默认为 ShellTextFormatter
    np1.builtin_option_name["help"] = {"帮助", "-h"}  # 设置此命名空间下的命令的帮助选项名称

# 你还可以使用config来管理所有命名空间并切换至任意命名空间
config.namespaces["foo"] = ns  # 将命名空间挂载到 config 上

alc = Alconna("pip", Subcommand("install", Args["package", str]), namespace=config.namespaces["foo"]) # 也是同样可以切换到"foo"命名空间
```

### 修改默认的命名空间

```python
from arclet.alconna import config, namespace, Namespace


config.default_namespace.prefixes = [...]  # 直接修改默认配置

np = Namespace("xxx", prefixes=[...])
config.default_namespace = np  # 更换默认的命名空间

with namespace(config.default_namespace.name) as np:
    np.prefixes = [...]
```

## 快捷指令

快捷命令可以做到标识一段命令, 并且传递参数给原命令

一般情况下你可以通过 `Alconna.shortcut` 进行快捷指令操作 (创建，删除)

`shortcut` 的第一个参数为快捷指令名称，第二个参数为 `ShortcutArgs`，作为快捷指令的配置：

```python
class ShortcutArgs(TypedDict):
    """快捷指令参数"""

    command: NotRequired[str]
    """快捷指令的命令"""
    args: NotRequired[list[Any]]
    """快捷指令的附带参数"""
    fuzzy: NotRequired[bool]
    """是否允许命令后随参数"""
    prefix: NotRequired[bool]
    """是否调用时保留指令前缀"""
    wrapper: NotRequired[ShortcutRegWrapper]
    """快捷指令的正则匹配结果的额外处理函数"""
    humanized: NotRequired[str]
    """快捷指令的人类可读描述"""
```

### args的使用

```python
from arclet.alconna import Alconna, Args


alc = Alconna("setu", Args["count", int])

alc.shortcut("涩图(\d+)张", {"args": ["{0}"]})
# 'Alconna::setu 的快捷指令: "涩图(\\d+)张" 添加成功'

alc.parse("涩图3张").query("count")
# 3
```

### command的使用

```python
from arclet.alconna import Alconna, Args


alc = Alconna("eval", Args["content", str])

alc.shortcut("echo", {"command": "eval print(\\'{*}\\')"})
# 'Alconna::eval 的快捷指令: "echo" 添加成功'

alc.shortcut("echo", delete=True) # 删除快捷指令
# 'Alconna::eval 的快捷指令: "echo" 删除成功'

@alc.bind() # 绑定一个命令执行器, 若匹配成功则会传入参数, 自动执行命令执行器
def cb(content: str):
    eval(content, {}, {})

alc.parse('eval print(\\"hello world\\")')
# hello world

alc.parse("echo hello world!")
# hello world!
```

当 `fuzzy` 为 False 时，第一个例子中传入 `"涩图1张 abc"` 之类的快捷指令将视为解析失败

快捷指令允许三类特殊的 placeholder：

- `{%X}`: 如 `setu {%0}`，表示此处填入快捷指令后随的第 X 个参数。

例如，若快捷指令为 `涩图`, 配置为 `{"command": "setu {%0}"}`, 则指令 `涩图 1` 相当于 `setu 1`

- `{*}`: 表示此处填入所有后随参数，并且可以通过 `{*X}` 的方式指定组合参数之间的分隔符。

- `{X}`: 表示此处填入可能的正则匹配的组：

- 若 `command` 中存在匹配组 `(xxx)`，则 `{X}` 表示第 X 个匹配组的内容
- 若 `command` 中存储匹配组 `(?P<xxx>...)`, 则 `{X}` 表示 **名字** 为 X 的匹配结果

除此之外, 通过 **Alconna** 内置选项 `--shortcut` 可以动态操作快捷指令

例如：

- `cmd --shortcut <key> <cmd>` 来增加一个快捷指令
- `cmd --shortcut list` 来列出当前指令的所有快捷指令
- `cmd --shortcut delete key` 来删除一个快捷指令

```python
from arclet.alconna import Alconna, Args


alc = Alconna("eval", Args["content", str])

alc.shortcut("echo", {"command": "eval print(\\'{*}\\')"})

alc.parse("eval --shortcut list")
# 'echo'
```

## 紧凑命令

`Alconna`, `Option` 与 `Subcommand` 可以设置 `compact=True` 使得解析命令时允许名称与后随参数之间没有分隔：

```python
from arclet.alconna import Alconna, Option, CommandMeta, Args


alc = Alconna("test", Args["foo", int], Option("BAR", Args["baz", str], compact=True), meta=CommandMeta(compact=True))

assert alc.parse("test123 BARabc").matched
```

这使得我们可以实现如下命令：

```python
from arclet.alconna import Alconna, Option, Args, append


alc = Alconna("gcc", Option("--flag|-F", Args["content", str], action=append, compact=True))
print(alc.parse("gcc -Fabc -Fdef -Fxyz").query[list]("flag.content"))
# ['abc', 'def', 'xyz']
```

当 `Option` 的 `action` 为 `count` 时，其自动支持 `compact` 特性：

```python
from arclet.alconna import Alconna, Option, count


alc = Alconna("pp", Option("--verbose|-v", action=count, default=0))
print(alc.parse("pp -vvv").query[int]("verbose.value"))
# 3
```

## 模糊匹配

模糊匹配会应用在任意需要进行名称判断的地方，如 **命令名称**，**选项名称** 和 **参数名称** (如指定需要传入参数名称)。

```python
from arclet.alconna import Alconna, CommandMeta


alc = Alconna("test_fuzzy", meta=CommandMeta(fuzzy_match=True))

alc.parse("test_fuzy")
# test_fuzy is not matched. Do you mean "test_fuzzy"?
```

## 半自动补全

半自动补全为用户提供了推荐后续输入的功能

补全默认通过 `--comp` 或 `-cp` 或 `?` 触发：（命名空间配置可修改名称）

```python
from arclet.alconna import Alconna, Args, Option


alc = Alconna("test", Args["abc", int]) + Option("foo") + Option("bar")
alc.parse("test --comp")

'''
output

以下是建议的输入：
* <abc: int>
* --help
* -h
* -sct
* --shortcut
* foo
* bar
'''
```

## Duplication

**Duplication** 用来提供更好的自动补全，类似于 **ArgParse** 的 **Namespace**

普通情况下使用，需要利用到 **ArgsStub**、**OptionStub** 和 **SubcommandStub** 三个部分

以pip为例，其对应的 Duplication 应如下构造:

```python
from arclet.alconna import Alconna, Args, Option, OptionResult, Duplication, SubcommandStub, Subcommand, count


class MyDup(Duplication):
    verbose: OptionResult
    install: SubcommandStub


alc = Alconna(
    "pip",
    Subcommand(
        "install",
        Args["package", str],
        Option("-r|--requirement", Args["file", str]),
        Option("-i|--index-url", Args["url", str]),
    ),
    Option("-v|--version"),
    Option("-v|--verbose", action=count),
)

res = alc.parse("pip -v install ...") # 不使用duplication获得的提示较少
print(res.query("install"))
# (value=Ellipsis args={'package': '...'} options={} subcommands={})

result = alc.parse("pip -v install ...", duplication=MyDup)
print(result.install)
# SubcommandStub(_origin=Subcommand('install', args=Args('package': str)), _value=Ellipsis, available=True, args=ArgsStub(_origin=Args('package': str), _value={'package': '...'}, available=True), dest='install', options=[OptionStub(_origin=Option('requirement', args=Args('file': str)), _value=None, available=False, args=ArgsStub(_origin=Args('file': str), _value={}, available=False), dest='requirement', aliases=['r', 'requirement'], name='requirement'), OptionStub(_origin=Option('index-url', args=Args('url': str)), _value=None, available=False, args=ArgsStub(_origin=Args('url': str), _value={}, available=False), dest='index-url', aliases=['index-url', 'i'], name='index-url')], subcommands=[], name='install')
```

**Duplication** 也可以如 **Namespace** 一样直接标明参数名称和类型：

```python
from typing import Optional
from arclet.alconna import Duplication


class MyDup(Duplication):
    package: str
    file: Optional[str] = None
    url: Optional[str] = None
```

## 上下文插值

当 `context_style` 条目被设置后，传入的命令中符合上下文插值的字段会被自动替换成当前上下文中的信息。

上下文可以在 `parse` 中传入：

```python
from arclet.alconna import Alconna, Args, CommandMeta

alc = Alconna("test", Args["foo", int], meta=CommandMeta(context_style="parentheses"))

alc.parse("test $(bar)", {"bar": 123})
# {"foo": 123}
```

context_style 的值分两种：

- `"bracket"`: 插值格式为 `{...}`，例如 `{foo}`
- `"parentheses"`: 插值格式为 `$(...)`，例如 `$(bar)`
