# 基本配置

到目前为止我们还在使用 NoneBot 的默认行为，在开始编写自己的插件之前，我们先尝试在配置文件上动动手脚，让 NoneBot 表现出不同的行为。

::: tip 提示
本章的完整代码可以在 [awesome-bot-1](https://github.com/richardchien/nonebot/tree/master/docs/guide/code/awesome-bot-1) 查看。
:::

## 项目结构

要使用自定义配置的话，我们的机器人代码将不再只有一个文件（`bot.py`），这时候良好的项目结构开始变得重要了。

在这里，我们创建一个名为 `awesome-bot` 的目录作为我们的项目主目录，你也可以使用其它你想要的名字。然后把之前的 `bot.py` 移动到 `awesome-bot` 中，再新建一个名为 `config.py` 的空文件。此时项目结构如下：

```
awesome-bot
├── bot.py
└── config.py
```

在后面几章中，我们将在此结构上进行扩展和改进。

## 配置超级用户

上一章中我们知道 NoneBot 内置了 `echo` 和 `say` 命令，我们已经测试了 `echo` 命令，并且正确地收到了机器人的回复，现在来尝试向它发送一个 `say` 命令：

```
/say [CQ:music,type=qq,id=209249583]
```

可以预料，命令不会起任何效果，因为我们提到过，`say` 命令只有超级用户可以调用，而现在我们还没有将自己的 QQ 号配置为超级用户。

因此下面我们往 `config.py` 中填充如下内容：

```python
from nonebot.default_config import *

SUPERUSERS = {12345678}
```

**这里的第 1 行是从 NoneBot 的默认配置中导入所有项，通常这是必须的，除非你知道自己在做什么，否则始终应该在配置文件的开头写上这一行。**

之后就是配置 `SUPERUSERS` 了，这个配置项的要求是值为 `int` 类型的**容器**，也就是说，可以是 `set`、`list`、`tuple` 等类型，元素类型为 `int`；`12345678` 是你想设置为超级用户的 QQ。

`config.py` 写好之后，修改 `bot.py` 如下：

```python {3,6}
import nonebot

import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.run(host='127.0.0.1', port=8080)
```

第 3 行导入 `config.py` 模块，第 6 行将 `config.py` 作为配置对象传给 `nonebot.init()` 函数，这样 NoneBot 就知道了超级用户有哪些。

重启 NoneBot 后再次尝试发送：

```
/say [CQ:music,type=qq,id=209249583]
```

可以看到这次机器人成功地给你回复了一个音乐分享消息。

## 配置命令的起始字符

目前我们发送的命令都必须以一个特殊符号 `/` 开头，实际上，NoneBot 默认支持以 `/`、`／`、`!`、`！` 其中之一作为开头，现在我们希望能够不需要特殊符号开头就可以调用命令，要做到这一点非常简单，在 `config.py` 添加一行即可：

```python {4}
from nonebot.default_config import *

SUPERUSERS = {12345678}
COMMAND_START = {'', '/', '!', '／', '！'}
```

首先需要知道，NoneBot 默认的 `COMMAND_START` 是一个 `set` 对象，如下：

```python
COMMAND_START = {'/', '!', '／', '！'}
```

这表示会尝试把 `/`、`!`、`／`、`！` 开头的消息理解成命令。而我们上面修改了的 `COMMAND_START` 加入了空字符串 `''`，也就告诉了 NoneBot，我们希望不需要任何起始字符也能调用命令。

`COMMAND_START` 的值和 `SUPERUSERS` 一样，可以是 `list`、`tuple`、`set` 等任意容器类型，元素类型可以是 `str` 或正则表达式，例如：

```python
import re
from nonebot.default_config import *

COMMAND_START = ['', re.compile(r'[/!]+')]
```

现在重启 NoneBot，你就可以使用形如 `echo 你好，世界` 的消息来调用 `echo` 命令了，这么做的好处在 `echo` 命令中可能体现不出来，但对于其它实用型命令，可能会让使用更方便一些，比如天气查询命令：

```
天气 南京
```

这里命令名是 `天气`，参数是 `南京`，从肉眼上看起来非常直观，相比 `/天气 南京` 使用起来也更加舒适。

## 配置监听的 IP 和端口

当有了配置文件之后，我们可能会希望将 `nonebot.run()` 参数中的 `host` 和 `port` 移动到配置文件中，毕竟这两项是有可能随着运行场景的变化而有不同的需求的，把它们放到配置文件中有利于配置和代码的解耦。这同样很容易做到，只需进行如下配置：

```python {3-4}
from nonebot.default_config import *

HOST = '0.0.0.0'
PORT = 8080
```

然后在 `bot.py` 中就不再需要传入 `host` 和 `port`，如下：

```python {8}
import nonebot

import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.run()
```

实际上，不需要配置这两项也可以直接使用 `nonebot.run()`，NoneBot 会使用如下默认配置：

```python
HOST = '127.0.0.1'
PORT = 8080
```
