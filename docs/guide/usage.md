# 编写使用帮助

经过前面的部分，我们已经给机器人编写了天气查询和图灵聊天插件，当然，你可能已经另外编写了更多具有个性化功能的插件。

现在，为了让用户能够更方便的使用，是时候编写一个使用帮助了。

:::tip 提示
本章的完整代码可以在 [awesome-bot-7](https://github.com/richardchien/nonebot/tree/master/docs/guide/code/awesome-bot-7) 查看。
:::

## 给插件添加名称和用法

这里以天气查询和图灵聊天两个插件为例，分别在 `awesome/plugins/weather/__init__.py` 和 `awesome/plugins/tuling.py` 两个文件的开头，通过 `__plugin_name__` 和 `__plugin_usage__` 两个特殊变量设置插件的名称和使用方法，如下：

```python
# awesome/plugins/weather/__init__.py

# ... 各种 import

__plugin_name__ = '天气'
__plugin_usage__ = r"""
天气查询

天气  [城市名称]
"""
```

```python
# awesome/plugins/tuling.py

# ... 各种 import

__plugin_name__ = '智能聊天'
__plugin_usage__ = r"""
智能聊天

直接跟我聊天即可～
""".strip()
```

一旦使用 `__plugin_name__` 和 `__plugin_usage__` 特殊变量设置了插件的名称和使用方法，NoneBot 在加载插件时就能够读取到这些内容，并存放在已加载插件的数据结构中。

## 编写使用帮助命令

新建插件 `awesome/plugins/usage.py`，编写内容如下：

```python {8,13-14,20}
import nonebot
from nonebot import on_command, CommandSession


@on_command('usage', aliases=['使用帮助', '帮助', '使用方法'])
async def _(session: CommandSession):
    # 获取设置了名称的插件列表
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))

    arg = session.current_arg_text.strip().lower()
    if not arg:
        # 如果用户没有发送参数，则发送功能列表
        await session.send(
            '我现在支持的功能有：\n\n' + '\n'.join(p.name for p in plugins))
        return

    # 如果发了参数则发送相应命令的使用帮助
    for p in plugins:
        if p.name.lower() == arg:
            await session.send(p.usage)
```

这里高亮的内容是重点：

- `nonebot.get_loaded_plugins()` 函数用于获取所有已经加载的插件，**注意，由于可能存在插件没有设置 `__plugin_name__` 变量的情况，插件的名称有可能为空**，因此建议过滤一下
- 插件的 `name` 属性（`plugin.name`）用于获得插件模块的 `__plugin_name__` 特殊变量的值
- 插件的 `usage` 属性（`plugin.usage`）用于获得插件模块的 `__plugin_usage__` 特殊变量的值

到这里，使用帮助命令就已经编写完成了。如果愿意，可以继续按照自己的思路实现相对应的自然语言处理器，以优化使用体验。
