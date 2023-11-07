---
sidebar_position: 2
description: Alconna 基本介绍
---

# Alconna 命令解析

[Alconna](https://github.com/ArcletProject/Alconna) 作为命令解析器，
是一个简单、灵活、高效的命令参数解析器，并且不局限于解析命令式字符串。

特点包括：

- 高效
- 直观的命令组件创建方式
- 强大的类型解析与类型转换功能
- 自定义的帮助信息格式
- 多语言支持
- 易用的快捷命令创建与使用
- 可创建命令补全会话，以实现多轮连续的补全提示
- 可嵌套的多级子命令
- 正则匹配支持

## 命令示范

```python
import sys
from io import StringIO

from arclet.alconna import Alconna, Args, Field, Option, CommandMeta, MultiVar, Arparma
from nepattern import AnyString

alc = Alconna(
    "exec",
    Args["code", MultiVar(AnyString), Field(completion=lambda: "print(1+1)")] / "\n",
    Option("纯文本"),
    Option("无输出"),
    Option("目标", Args["name", str, "res"]),
    meta=CommandMeta("exec python code", example="exec\\nprint(1+1)"),
)

alc.shortcut(
    "echo",
    {"command": "exec 纯文本\nprint(\\'{*}\\')"},
)

alc.shortcut(
    "sin(\d+)",
    {"command": "exec 纯文本\nimport math\nprint(math.sin({0}*math.pi/180))"},
)


def exec_code(result: Arparma):
    if result.find("纯文本"):
        codes = list(result.code)
    else:
        codes = str(result.origin).split("\n")[1:]
    output = result.query[str]("目标.name", "res")
    if not codes:
        return ""
    lcs = {}
    _stdout = StringIO()
    _to = sys.stdout
    sys.stdout = _stdout
    try:
        exec(
            "def rc(__out: str):\n    "
            + "    ".join(_code + "\n" for _code in codes)
            + "    return locals().get(__out)",
            {**globals(), **locals()},
            lcs,
        )
        code_res = lcs["rc"](output)
        sys.stdout = _to
        if result.find("无输出"):
            return ""
        if code_res is not None:
            return f"{output}: {code_res}"
        _out = _stdout.getvalue()
        return f"输出: {_out}"
    except Exception as e:
        sys.stdout = _to
        return str(e)
    finally:
        sys.stdout = _to

print(exec_code(alc.parse("echo 1234")))
print(exec_code(alc.parse("sin30")))
print(
    exec_code(
        alc.parse(
"""\
exec
print(
    exec_code(
        alc.parse(
            "exec\\n"
            "import sys;print(sys.version)"
        )
    )
)
"""
        )
    )
)
```

## 命令编写

### 命令头

命令头是指命令的前缀 (Prefix) 与命令名 (Command) 的组合，例如 `!help` 中的 `!` 与 `help`。

在 Alconna 中，你可以传入多种类型的命令头，例如：

|             前缀             |   命令名   |                          匹配内容                           |       说明       |
| :--------------------------: | :--------: | :---------------------------------------------------------: | :--------------: |
|              -               |   "foo"    |                           `"foo"`                           | 无前缀的纯文字头 |
|              -               |    123     |                            `123`                            |  无前缀的元素头  |
|              -               | "re:\d{2}" |                           `"32"`                            |  无前缀的正则头  |
|              -               |    int     |                      `123` 或 `"456"`                       |  无前缀的类型头  |
|         [int, bool]          |     -      |                       `True` 或 `123`                       |  无名的元素类头  |
|        ["foo", "bar"]        |     -      |                     `"foo"` 或 `"bar"`                      |  无名的纯文字头  |
|        ["foo", "bar"]        |   "baz"    |                  `"foobaz"` 或 `"barbaz"`                   |     纯文字头     |
|         [int, bool]          |   "foo"    |             `[123, "foo"]` 或 `[False, "foo"]`              |      类型头      |
|         [123, 4567]          |   "foo"    |              `[123, "foo"]` 或 `[4567, "foo"]`              |      元素头      |
|      [nepattern.NUMBER]      |   "bar"    |            `[123, "bar"]` 或 `[123.456, "bar"]`             |     表达式头     |
|         [123, "foo"]         |   "bar"    |      `[123, "bar"]` 或 `"foobar"` 或 `["foo", "bar"]`       |      混合头      |
| [(int, "foo"), (456, "bar")] |   "baz"    | `[123, "foobaz"]` 或 `[456, "foobaz"]` 或 `[456, "barbaz"]` |       对头       |

其中

- 元素头：只会匹配对应的值，例如 `[123, 456]` 只会匹配 `123` 或 `456`，不会匹配 `789`。
- 纯文字头：只会匹配对应的字符串，例如 `["foo", "bar"]` 只会匹配 `"foo"` 或 `"bar"`，不会匹配 `"baz"`。
- 正则头：`re:xxx` 会将 `xxx` 转为正则表达式，然后匹配对应的字符串，例如 `re:\d{2}` 只会匹配 `"12"` 或 `"34"`，不会匹配 `"foo"`。
  **正则只在命令名上生效，命令前缀中的正则会被转义**。
- 类型头：只会匹配对应的类型，例如 `[int, bool]` 只会匹配 `123` 或 `True`，不会匹配 `"foo"`。
  - 无前缀的类型头：此时会将传入的值尝试转为 BasePattern，例如 `int` 会转为 `nepattern.INTEGER`。此时命令头会匹配对应的类型，
    例如 `int` 会匹配 `123` 或 `"456"`，但不会匹配 `"foo"`。同时，Alconna 会将命令头匹配到的值转为对应的类型，例如 `int` 会将 `"123"` 转为 `123`。
- 表达式头：只会匹配对应的表达式，例如 `[nepattern.NUMBER]` 只会匹配 `123` 或 `123.456`，不会匹配 `"foo"`。
- 混合头：

除了通过传入 `re:xxx` 来使用正则表达式外，Alconna 还提供了一种更加简洁的方式来使用正则表达式，那就是 Bracket Header。

```python
from alconna import Alconna

alc = Alconna(".rd{roll:int}")
assert alc.parse(".rd123").header["roll"] == 123
```

Bracket Header 类似 python 里的 f-string 写法，通过 "{}" 声明匹配类型

"{}" 中的内容为 "name:type or pat"：

- "{}", "{:}": 占位符，等价于 "(.+)"
- "{foo}": 等价于 "(?P&lt;foo&gt;.+)"
- "{:\d+}": 等价于 "(\d+)"
- "{foo:int}": 等价于 "(?P&lt;foo&gt;\d+)"，其中 "int" 部分若能转为 `BasePattern` 则读取里面的表达式

### 组件

我们可以看到主要的两大组件：`Option` 与 `Subcommand`。

`Option` 可以传入一组 `alias`，如 `Option("--foo|-F|FOO|f")` 或 `Option("--foo", alias=["-F"])`

传入别名后，Option 会选择其中长度最长的作为选项名称。若传入为 "--foo|-f"，则命令名称为 "--foo"。

:::tip 特别提醒！！！

在 Alconna 中 Option 的名字或别名**没有要求**必须在前面写上 `-`

:::

`Subcommand` 则可以传入自己的 **Option** 与 **Subcommand**。

```python
from arclet.alconna import Alconna, Option, Subcommand

alc = Alconna(
    "command_name",
    Option("opt1"),
    Option("--opt2"),
    Subcommand(
        "sub1",
        Option("sub1_opt1"),
        Option("SO2"),
        Subcommand(
            "sub1_sub1"
        )
    ),
    Subcommand(
        "sub2"
    )
)
```

他们拥有如下共同参数：

- `help_text`: 传入该组件的帮助信息
- `dest`: 被指定为解析完成时标注匹配结果的标识符，不传入时默认为选项或子命令的名称 (name)
- `requires`: 一段指定顺序的字符串列表，作为唯一的前置序列与命令嵌套替换
  对于命令 `test foo bar baz qux <a:int>` 来讲，因为`foo bar baz` 仅需要判断是否相等，所以可以这么编写：

  ```python
  Alconna("test", Option("qux", Args["a", int], requires=["foo", "bar", "baz"]))
  ```

- `default`: 默认值，在该组件未被解析时使用使用该值替换。

  特别的，使用 `OptionResult` 或 `SubcomanndResult` 可以设置包括参数字典在内的默认值：

  ```python
  from arclet.alconna import Option, OptionResult

  opt1 = Option("--foo", default=False)
  opt2 = Option("--foo", default=OptionResult(value=False, args={"bar": 1}))
  ```

### 选项操作

`Option` 可以特别设置传入一类 `Action`，作为解析操作

`Action` 分为三类：

- `store`: 无 Args 时， 仅存储一个值， 默认为 Ellipsis； 有 Args 时， 后续的解析结果会覆盖之前的值
- `append`: 无 Args 时， 将多个值存为列表， 默认为 Ellipsis； 有 Args 时， 每个解析结果会追加到列表中

  当存在默认值并且不为列表时， 会自动将默认值变成列表， 以保证追加的正确性

- `count`: 无 Args 时， 计数器加一； 有 Args 时， 表现与 STORE 相同

  当存在默认值并且不为数字时， 会自动将默认值变成 1， 以保证计数器的正确性。

`Alconna` 提供了预制的几类 `action`：

- `store`，`store_value`，`store_true`，`store_false`
- `append`，`append_value`
- `count`

### 参数声明

`Args` 是用于声明命令参数的组件。

`Args` 是参数解析的基础组件，构造方法形如 `Args["foo", str]["bar", int]["baz", bool, False]`，
与函数签名类似，但是允许含有默认值的参数在前；同时支持 keyword-only 参数不依照构造顺序传入 （但是仍需要在非 keyword-only 参数之后）。

`Args` 中的 `name` 是用以标记解析出来的参数并存放于 **Arparma** 中，以方便用户调用。

其有三种为 Args 注解的标识符： `?`、`/` 与 `!`。标识符与 key 之间建议以 `;` 分隔：

- `!` 标识符表示该处传入的参数应不是规定的类型，或不在指定的值中。
- `?` 标识符表示该参数为可选参数，会在无参数匹配时跳过。
- `/` 标识符表示该参数的类型注解需要隐藏。

另外，对于参数的注释也可以标记在 `name` 中，其与 name 或者标识符 以 `#` 分割：

`foo#这是注释;?` 或 `foo?#这是注释`

:::tip

`Args` 中的 `name` 在实际命令中并不需要传入（keyword 参数除外）：

```python
from arclet.alconna import Alconna, Args

alc = Alconna("test", Args["foo", str])
alc.parse("test --foo abc")  # 错误
alc.parse("test abc")  # 正确
```

若需要 `test --foo abc`，你应该使用 `Option`：

```python
from arclet.alconna import Alconna, Args, Option

alc = Alconna("test", Option("--foo", Args["foo", str]))
```

:::

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

`MultiVar` 则是一个特殊的标注，用于告知解析器该参数可以接受多个值，其构造方法形如 `MultiVar(str)`。
同样的还有 `KeyWordVar`，其构造方法形如 `KeyWordVar(str)`，用于告知解析器该参数为一个 keyword-only 参数。

:::tip

`MultiVar` 与 `KeyWordVar` 组合时，代表该参数为一个可接受多个 key-value 的参数，其构造方法形如 `MultiVar(KeyWordVar(str))`

`MultiVar` 与 `KeyWordVar` 也可以传入 `default` 参数，用于指定默认值。

`MultiVar` 不能在 `KeyWordVar` 之后传入。

:::

### 紧凑命令

`Alconna`，`Option` 可以设置 `compact=True` 使得解析命令时允许名称与后随参数之间没有分隔：

```python
from arclet.alconna import Alconna, Option, CommandMeta, Args

alc = Alconna("test", Args["foo", int], Option("BAR", Args["baz", str], compact=True), meta=CommandMeta(compact=True))

assert alc.parse("test123 BARabc").matched
```

这使得我们可以实现如下命令：

```python
>>> from arclet.alconna import Alconna, Option, Args, append
>>> alc = Alconna("gcc", Option("--flag|-F", Args["content", str], action=append, compact=True))
>>> alc.parse("gcc -Fabc -Fdef -Fxyz").query[list[str]]("flag.content")
['abc', 'def', 'xyz']
```

当 `Option` 的 `action` 为 `count` 时，其自动支持 `compact` 特性：

```python
>>> from arclet.alconna import Alconna, Option, Args, count
>>> alc = Alconna("pp", Option("--verbose|-v", action=count, default=0))
>>> alc.parse("pp -vvv").query[int]("verbose.value")
3
```

## 命令特性

### 配置

`arclet.alconna.Namespace` 表示某一命名空间下的默认配置：

```python
from arclet.alconna import config, namespace, Namespace
from arclet.alconna.tools import ShellTextFormatter


np = Namespace("foo", prefixes=["/"])  # 创建 Namespace 对象，并进行初始配置

with namespace("bar") as np1:
    np1.prefixes = ["!"]    # 以上下文管理器方式配置命名空间，此时配置会自动注入上下文内创建的命令
    np1.formatter_type = ShellTextFormatter  # 设置此命名空间下的命令的 formatter 默认为 ShellTextFormatter
    np1.builtin_option_name["help"] = {"帮助", "-h"}  # 设置此命名空间下的命令的帮助选项名称

config.namespaces["foo"] = np  # 将命名空间挂载到 config 上
```

同时也提供了默认命名空间配置与修改方法：

```python
from arclet.alconna import config, namespace, Namespace


config.default_namespace.prefixes = [...]  # 直接修改默认配置

np = Namespace("xxx", prefixes=[...])
config.default_namespace = np  # 更换默认的命名空间

with namespace(config.default_namespace.name) as np:
    np.prefixes = [...]
```

### 半自动补全

半自动补全为用户提供了推荐后续输入的功能。

补全默认通过 `--comp` 或 `-cp` 或 `?` 触发：（命名空间配置可修改名称）

```python
from arclet.alconna import Alconna, Args, Option

alc = Alconna("test", Args["abc", int]) + Option("foo") + Option("bar")
alc.parse("test ?")

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

### 快捷指令

快捷指令顾名思义，可以为基础指令创建便捷的触发方式

一般情况下你可以通过 `Alconna.shortcut` 进行快捷指令操作 (创建，删除)；

```python
>>> from arclet.alconna import Alconna, Args
>>> alc = Alconna("setu", Args["count", int])
>>> alc.shortcut("涩图(\d+)张", {"args": ["{0}"]})
'Alconna::setu 的快捷指令: "涩图(\\d+)张" 添加成功'
>>> alc.parse("涩图3张").query("count")
3
```

`shortcut` 的第一个参数为快捷指令名称，第二个参数为 `ShortcutArgs`，作为快捷指令的配置

```python
class ShortcutArgs(TypedDict):
    """快捷指令参数"""

    command: NotRequired[DataCollection[Any]]
    """快捷指令的命令"""
    args: NotRequired[list[Any]]
    """快捷指令的附带参数"""
    fuzzy: NotRequired[bool]
    """是否允许命令后随参数"""
    prefix: NotRequired[bool]
    """是否调用时保留指令前缀"""
```

当 `fuzzy` 为 False 时，传入 `"涩图1张 abc"` 之类的快捷指令将视为解析失败

快捷指令允许三类特殊的 placeholder:

- `{%X}`: 如 `setu {%0}`，表示此处必须填入快捷指令后随的第 X 个参数。

  例如，若快捷指令为 `涩图`，配置为 `{"command": "setu {%0}"}`，则指令 `涩图 1` 相当于 `setu 1`

- `{*}`: 表示此处填入所有后随参数，并且可以通过 `{*X}` 的方式指定组合参数之间的分隔符。
- `{X}`: 表示此处填入可能的正则匹配的组：
  - 若 `command` 中存在匹配组 `(xxx)`，则 `{X}` 表示第 X 个匹配组的内容
  - 若 `command` 中存储匹配组 `(?P<xxx>...)`，则 `{X}` 表示名字为 X 的匹配结果

除此之外，通过内置选项 `--shortcut` 可以动态操作快捷指令。

例如：

- `cmd --shortcut <key> <cmd>` 来增加一个快捷指令
- `cmd --shortcut list` 来列出当前指令的所有快捷指令
- `cmd --shortcut delete key` 来删除一个快捷指令

### 使用模糊匹配

模糊匹配通过在 Alconna 中设置其 CommandMeta 开启。

模糊匹配会应用在任意需要进行名称判断的地方，如**命令名称**，**选项名称**和**参数名称**（如指定需要传入参数名称）。

```python
from arclet.alconna import Alconna, CommandMeta

alc = Alconna("test_fuzzy", meta=CommandMeta(fuzzy_match=True))
alc.parse("test_fuzy")
# output: test_fuzy is not matched. Do you mean "test_fuzzy"?
```

## 解析结果

`Alconna.parse` 会返回由 **Arparma** 承载的解析结果。

`Arpamar` 会有如下参数：

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

`Arparma` 同时提供了便捷的查询方法 `query[type]()`，会根据传入的 `path` 查找参数并返回

`path` 支持如下：

- `main_args`，`options`，...: 返回对应的属性
- `args`: 返回 all_matched_args
- `main_args.xxx`，`options.xxx`，...: 返回字典中 `xxx`键对应的值
- `args.xxx`: 返回 all_matched_args 中 `xxx`键对应的值
- `options.foo`，`foo`: 返回选项 `foo` 的解析结果 (OptionResult)
- `options.foo.value`，`foo.value`: 返回选项 `foo` 的解析值
- `options.foo.args`，`foo.args`: 返回选项 `foo` 的解析参数字典
- `options.foo.args.bar`，`foo.bar`: 返回选项 `foo` 的参数字典中 `bar` 键对应的值
  ...

同样，`Arparma["foo.bar"]` 的表现与 `query()` 一致

## Duplication

**Duplication** 用来提供更好的自动补全，类似于 **ArgParse** 的 **Namespace**，经测试表现良好（好耶）。

普通情况下使用，需要利用到 **ArgsStub**、**OptionStub** 和 **SubcommandStub** 三个部分，

以 pip 为例，其对应的 Duplication 应如下构造：

```python
from arclet.alconna import OptionResult, Duplication, SubcommandStub

class MyDup(Duplication):
    verbose: OptionResult
    install: SubcommandStub  # 选项与子命令对应的stub的变量名必须与其名字相同
```

并在解析时传入 Duplication：

```python
result = alc.parse("pip -v install ...", duplication=MyDup)
>>> type(result)
<class MyDup>
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
