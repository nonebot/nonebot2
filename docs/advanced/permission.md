# 权限控制

**权限控制**是机器人在实际应用中需要解决的重点问题之一，`Nonebot `提供了十分完善且灵活的权限控制机制——` Permission `机制。接下来我们将对这个机制进行简单的说明。

## 应用

如同` Rule `一样,  ` Permission `可以在[注册事件响应器](../guide/creating-a-matcher)时添加` permission `参数来加以应用，这样` Nonebot `会在事件响应时检测事件主体的权限。下面我们以` SUPERUSER `为例，对该机制的应用做一下介绍。

```python
from nonebot.permission import SUPERUSER
from nonebot.adapters import Bot
from nonebot import on_command

matcher = on_command('测试超管', permission=SUPERUSER)


@matcher.handle()
async def _(bot: Bot):
    await matcher.send("超管命令测试成功")


@matcher.got("key1", "超管提问")
async def _(bot: Bot, event: Event):
    await matcher.send("超管命令got成功")
```

在这段代码中，我们事件响应器指定了` SUPERUSER `这样一个权限，那么机器人只会响应超级管理员的` 测试超管 `命令，并且会响应该超级管理员的连续对话。

::: tip 提示

在这里需要强调的是，` Permission `与` Rule `的表现并不相同，` Rule `只会在初次响应时生效，在余下的对话中并没有限制事件；但是` Permission `会持续生效，在连续对话中会一直对事件主体加以限制。

:::

## 进阶

` Permission `除了可以在注册事件响应器时加以应用，还可以在编写事件处理函数` handler `时主动调用，我们可以利用这个特性在一个` handler `里对不同权限的事件主体进行区别响应，下面我们以 ` CQHTTP `中的` GROUP_ADMIN  `(普通管理员非群主)和` GROUP_OWNER `为例，说明下怎么进行主动调用。

```python
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot import on_command

matcher = on_command("测试权限")


@matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if await GROUP_ADMIN(bot, event):
        await matcher.send("管理员测试成功")
    elif await GROUP_OWNER(bot, event):
        await matcher.send("群主测试成功")
    else:
        await matcher.send("群员测试成功")
      
```

在这段代码里，我们并没有对命令的权限指定，这个命令会响应所有在群聊中的` 测试权限 `命令，但是在` handler `里，我们对两个` Permission `进行主动调用，从而可以对不同的角色进行不同的响应。

## 自定义

如同` Rule `一样,   ` Permission `也是由非负数个` PermissionChecker `组成的，但只需其中一个返回` True `时就会匹配成功。下面则是` PermissionChecker `和` Permission `示例：

```python
from nonebot.permission import Permission
from nonebot.adapters import Bot, Event

async def async_checker(bot: Bot, event: Event) -> bool:
	return True

def sync_checker(bot: Bot, event: Event) -> bool:
	return True

def check(arg1, arg2):

	async def _checker(bot: Bot, event: Event) -> bool:
    	return bool(arg1 + arg2)

	return Permission(_checker)
```

`Permission` 和 `PermissionChecker` 之间可以使用 `或 |` 互相组合：

```python
from nonebot.permission import Permission

Permission(async_checker1) | sync_checker | async_checker2
```

同样地，如果想用` Permission(*checkers) ` 包裹构造` Permission `，函数必须是异步的；但是在利用` 或 | `符号连接构造时，` Nonebot `会自动包裹同步函数为异步函数。

