---
sidebar_position: 5
description: 事件响应器组成与内置响应规则

options:
  menu:
    - category: advanced
      weight: 60
---

# 事件响应器进阶

在[指南](../tutorial/matcher.md)与[深入](../appendices/rule.md)中，我们已经介绍了事件响应器的基本用法以及响应规则、权限控制等功能。在这一节中，我们将介绍事件响应器的组成，内置的响应规则，与第三方响应规则拓展。

:::tip 提示
事件响应器允许继承，你可以通过直接继承 `Matcher` 类来创建一个新的事件响应器。
:::

## 事件响应器组成

### 事件响应器类型

事件响应器类型 `type` 即是该响应器所要响应的事件类型，只有在接收到的事件类型与该响应器的类型相同时，才会触发该响应器。如果类型为空字符串 `""`，则响应器将会响应所有类型的事件。事件响应器类型的检查在所有其他检查（权限控制、响应规则）之前进行。

NoneBot 内置了四种常用事件类型：`meta_event`、`message`、`notice`、`request`，分别对应元事件、消息、通知、请求。通常情况下，协议适配器会将事件合理地分类至这四种类型中。如果有其他类型的事件需要响应，可以自行定义新的类型。

### 事件触发权限

事件触发权限 `permission` 是一个 `Permission` 对象，这在[权限控制](../appendices/permission.mdx)一节中已经介绍过。事件触发权限会在事件响应器的类型检查通过后进行检查，如果权限检查通过，则执行响应规则检查。

### 事件响应规则

事件响应规则 `rule` 是一个 `Rule` 对象，这在[响应规则](../appendices/rule.md)一节中已经介绍过。事件响应器的响应规则会在事件响应器的权限检查通过后进行匹配，如果响应规则检查通过，则触发该响应器。

### 响应优先级

响应优先级 `priority` 是一个正整数，用于指定响应器的优先级。响应器的优先级越小，越先被触发。如果响应器的优先级相同，则按照响应器的注册顺序进行触发。

### 阻断

阻断 `block` 是一个布尔值，用于指定响应器是否阻断事件的传播。如果阻断为 `True`，则在该响应器被触发后，事件将不会再传播给其他下一优先级的响应器。

NoneBot 内置的事件响应器中，所有非 `command` 规则的 `message` 类型的事件响应器都会阻断事件传递，其他则不会。

在部分情况中，可以使用 [`stop_propagation`](../appendices/session-control.mdx#stop_propagation) 方法动态阻止事件传播，该方法需要 handler 在参数中获取 matcher 实例后调用方法。

### 有效期

事件响应器的有效期分为 `temp` 和 `expire_time` 。`temp` 是一个布尔值，用于指定响应器是否为临时响应器。如果为 `True`，则该响应器在被触发后会被自动销毁。`expire_time` 是一个 `datetime` 对象，用于指定响应器的过期时间。如果 `expire_time` 不为 `None`，则在该时间点后，该响应器会被自动销毁。

### 默认状态

事件响应器的默认状态 `default_state` 是一个 `dict` 对象，用于指定响应器的默认状态。在响应器被触发时，响应器将会初始化默认状态然后开始执行事件处理流程。

## 基本辅助函数

NoneBot 为四种类型的事件响应器提供了五个基本的辅助函数：

- `on`：创建任何类型的事件响应器。
- `on_metaevent`：创建元事件响应器。
- `on_message`：创建消息事件响应器。
- `on_request`：创建请求事件响应器。
- `on_notice`：创建通知事件响应器。

除了 `on` 函数具有一个 `type` 参数外，其余参数均相同：

- `rule`：响应规则，可以是 `Rule` 对象或者 `RuleChecker` 函数。
- `permission`：事件触发权限，可以是 `Permission` 对象或者 `PermissionChecker` 函数。
- `handlers`：事件处理函数列表。
- `temp`：是否为临时响应器。
- `expire_time`：响应器的过期时间。
- `priority`：响应器的优先级。
- `block`：是否阻断事件传播。
- `state`：响应器的默认状态。

在消息类型的事件响应器的基础上，NoneBot 还内置了一些常用的响应规则，并结合为辅助函数来方便我们快速创建指定功能的响应器。下面我们逐个介绍。

## 内置响应规则

:::tip
响应规则的使用方法可以参考 [深入 - 响应规则](../appendices/rule.md)。
:::

### `startswith`

`startswith` 响应规则用于匹配消息纯文本部分的开头是否与指定字符串（或一系列字符串）相同。可选参数 `ignorecase` 用于指定是否忽略大小写，默认为 `False`。

例如，我们可以创建一个匹配消息开头为 `!` 或者 `/` 的规则：

```python
from nonebot.rule import startswith

rule = startswith(("!", "/"), ignorecase=False)
```

也可以直接使用辅助函数新建一个响应器：

```python
from nonebot import on_startswith

matcher = on_startswith(("!", "/"), ignorecase=False)
```

### `endswith`

`endswith` 响应规则用于匹配消息纯文本部分的结尾是否与指定字符串（或一系列字符串）相同。可选参数 `ignorecase` 用于指定是否忽略大小写，默认为 `False`。

例如，我们可以创建一个匹配消息结尾为 `.` 或者 `。` 的规则：

```python
from nonebot.rule import endswith

rule = endswith((".", "。"), ignorecase=False)
```

也可以直接使用辅助函数新建一个响应器：

```python
from nonebot import on_endswith

matcher = on_endswith((".", "。"), ignorecase=False)
```

### `fullmatch`

`fullmatch` 响应规则用于匹配消息纯文本部分是否与指定字符串（或一系列字符串）完全相同。可选参数 `ignorecase` 用于指定是否忽略大小写，默认为 `False`。

例如，我们可以创建一个匹配消息为 `ping` 或者 `pong` 的规则：

```python
from nonebot.rule import fullmatch

rule = fullmatch(("ping", "pong"), ignorecase=False)
```

也可以直接使用辅助函数新建一个响应器：

```python
from nonebot import on_fullmatch

matcher = on_fullmatch(("ping", "pong"), ignorecase=False)
```

### `keyword`

`keyword` 响应规则用于匹配消息纯文本部分是否包含指定字符串（或一系列字符串）。

例如，我们可以创建一个匹配消息中包含 `hello` 或者 `hi` 的规则：

```python
from nonebot.rule import keyword

rule = keyword("hello", "hi")
```

也可以直接使用辅助函数新建一个响应器：

```python
from nonebot import on_keyword

matcher = on_keyword({"hello", "hi"})
```

### `command`

`command` 是最常用的响应规则，它用于匹配消息是否为命令。它会根据配置中的 [Command Start 和 Command Separator](../appendices/config.mdx#command-start-和-command-separator) 来判断消息是否为命令。

例如，当我们配置了 `Command Start` 为 `/`，`Command Separator` 为 `.` 时：

```python
from nonebot.rule import command

# 匹配 "/help" 或者 "/帮助" 开头的消息
rule = command("help", "帮助")
# 匹配 "/help.cmd" 开头的消息
rule = command(("help", "cmd"))
```

也可以直接使用辅助函数新建一个响应器：

```python
from nonebot import on_command

matcher = on_command("help", aliases={"帮助"})
```

此外，`command` 响应规则默认允许消息命令与参数间不加空格，如果需要严格匹配命令与参数间的空白符，可以使用 `command` 函数的 `force_whitespace` 参数。`force_whitespace` 参数可以是 bool 类型或者具体的字符串，默认为 `False`。如果为 `True`，则命令与参数间必须有任意个数的空白符；如果为字符串，则命令与参数间必须有且与给定字符串一致的空白符。

```python
rule = command("help", force_whitespace=True)
rule = command("help", force_whitespace=" ")
```

命令解析后的结果可以通过 [`Command`](./dependency.mdx#command)、[`RawCommand`](./dependency.mdx#rawcommand)、[`CommandArg`](./dependency.mdx#commandarg)、[`CommandStart`](./dependency.mdx#commandstart)、[`CommandWhitespace`](./dependency.mdx#commandwhitespace) 依赖注入获取。

### `shell_command`

`shell_command` 响应规则用于匹配类 shell 命令形式的消息。它首先与 [`command`](#command) 响应规则一样进行命令匹配，如果匹配成功，则会进行进一步的参数解析。参数解析采用 `argparse` 标准库进行，在此基础上添加了消息序列 `Message` 支持。

例如，我们可以创建一个匹配 `/cmd` 命令并且带有 `-v` 选项与默认 `-h` 帮助选项的规则：

```python
from nonebot.rule import shell_command, ArgumentParser

parser = ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")

rule = shell_command("cmd", parser=parser)
```

更多关于 `argparse` 的使用方法请参考 [argparse 文档](https://docs.python.org/zh-cn/3/library/argparse.html)。我们也可以选择不提供 `parser` 参数，这样 `shell_command` 将不会解析参数，但会提供参数列表 `argv`。

直接使用辅助函数新建一个响应器：

```python
from nonebot import on_shell_command
from nonebot.rule import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")

matcher = on_shell_command("cmd", parser=parser)
```

参数解析后的结果可以通过 [`ShellCommandArgv`](./dependency.mdx#shellcommandargv)、[`ShellCommandArgs`](./dependency.mdx#shellcommandargs) 依赖注入获取。

### `regex`

`regex` 响应规则用于匹配消息是否与指定正则表达式匹配。

:::tip 提示
正则表达式匹配使用 search 而非 match，如需从头匹配请使用 `r"^xxx"` 模式来确保匹配开头。
:::

例如，我们可以创建一个匹配消息中包含字母并且忽略大小写的规则：

```python
from nonebot.rule import regex

rule = regex(r"[a-z]+", flags=re.IGNORECASE)
```

也可以直接使用辅助函数新建一个响应器：

```python
from nonebot import on_regex

matcher = on_regex(r"[a-z]+", flags=re.IGNORECASE)
```

正则匹配后的结果可以通过 [`RegexStr`](./dependency.mdx#regexstr)、[`RegexGroup`](./dependency.mdx#regexgroup)、[`RegexDict`](./dependency.mdx#regexdict) 依赖注入获取。

### `to_me`

`to_me` 响应规则用于匹配事件是否与机器人相关。

例如：

```python
from nonebot.rule import to_me

rule = to_me()
```

### `is_type`

`is_type` 响应规则用于匹配事件类型是否为指定类型（或者一系列类型）。

例如，我们可以创建一个匹配 OneBot v11 私聊和群聊消息事件的规则：

```python
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent

rule = is_type(PrivateMessageEvent, GroupMessageEvent)
```

## 响应器组

为了更方便的管理一系列功能相近的响应器，NoneBot 提供了两种响应器组，它们可以帮助我们进行响应器的统一管理。

### `CommandGroup`

`CommandGroup` 可以用于管理一系列具有相同前置命令的子命令响应器。

例如，我们创建 `/cmd`、`/cmd.sub`、`/cmd.help` 三个命令，他们具有相同的优先级：

```python
from nonebot import CommandGroup

group = CommandGroup("cmd", priority=10)

cmd = group.command(tuple())
sub_cmd = group.command("sub")
help_cmd = group.command("help")
```

命令别名 aliases 默认不会添加 `CommandGroup` 设定的前缀，如果需要为 aliases 添加前缀，可以添加 `prefix_aliases=True` 参数:

```python
from nonebot import CommandGroup

group = CommandGroup("cmd", prefix_aliases=True)

cmd = group.command(tuple())
help_cmd = group.command("help", aliases={"帮助"})
```

这样就能成功匹配 `/cmd`、`/cmd.help`、`/cmd.帮助` 命令。如果未设置，将默认匹配 `/cmd`、`/cmd.help`、`/帮助` 命令。

### `MatcherGroup`

`MatcherGroup` 可以用于管理一系列具有相同属性的响应器。

例如，我们创建一个具有相同响应规则的响应器组：

```python
from nonebot.rule import to_me
from nonebot import MatcherGroup

group = MatcherGroup(rule=to_me())

matcher1 = group.on_message()
matcher2 = group.on_message()
```

## 第三方响应规则

### Alconna

[`nonebot-plugin-alconna`](https://github.com/nonebot/plugin-alconna) 是一类提供了拓展响应规则的插件。
该插件使用 [Alconna](https://github.com/ArcletProject/Alconna) 作为命令解析器，
是一个简单、灵活、高效的命令参数解析器, 并且不局限于解析命令式字符串。

该插件提供了一类新的事件响应器辅助函数 `on_alconna`，以及 `AlconnaResult` 等依赖注入函数。

基于 `Alconna` 的特性，该插件同时提供了一系列便捷的消息段标注。
标注可用于在 `Alconna` 中匹配消息中除 text 外的其他消息段，也可用于快速创建各适配器下的消息段。所有标注位于 `nonebot_plugin_alconna.adapters` 中。

该插件同时通过提供 `UniMessage` (通用消息模型) 实现了**跨平台接收和发送消息**的功能。

详情请阅读最佳实践中的 [命令解析拓展](../best-practice/alconna/README.mdx) 章节。
