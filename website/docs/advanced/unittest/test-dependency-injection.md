---
sidebar_position: 4
description: 测试依赖注入

options:
menu:
weight: 53
category: advanced
---

# 测试依赖注入

一般来说，依赖函数在测试事件响应时就已经被测试，但是有时我们需要独立测试依赖函数。

这时就可以用到 `NoneBug` 的 `test_dependent` 方法对依赖函数进行测试。

## 测试基本依赖注入

下面是一个简单的依赖注入插件示例和测试用例。

```python title=plugin.py
from nonebot.params import Depends
from nonebot.plugin import on_message

test = on_message()


def dependency():
    return True


@test.handle()
async def depend(x: bool = Depends(dependency)):
    return x
```

```python title=test_depend.py
import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_depend(app: App):
    from plugin import depend
    from nonebot.params import DependParam

    async with app.test_dependent(depend, allow_types=[DependParam]) as ctx:
        ctx.should_return(True)
```

`should_return` 为依赖函数应当返回的内容。

可以发现，这里被测试的函数 `depend` 并不是依赖函数，而是一个事件响应函数，这个函数实际上只是依赖函数的调用方。通过这样的方式调用依赖函数可以使用 `NoneBot` 的依赖注入特性（譬如 `use_cache`
）来更加真实地模拟事件响应的依赖注入。

## 测试依赖缓存

让我们对上面的函数和测试用例做一点修改。

```python title=plugin.py
from nonebot.params import Depends
from nonebot.plugin import on_message

test = on_message()
test_no_cache = on_message()
runned = []


def dependency():
    runned.append(1)
    return 1


def parameterless():
    assert len(runned) == 0
    runned.append(1)


@test.handle(parameterless=[Depends(parameterless)])
@test_no_cache.handle(parameterless=[Depends(parameterless)])
async def depend(x: int = Depends(dependency)):
    return x


@test.handle()
async def depend_cache(y: int = Depends(dependency, use_cache=True)):
    return y


@test_no_cache.handle()
async def depend_no_cache(z: int = Depends(dependency, use_cache=False)):
    return z
```

```python title=test_plugin.py
import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_depend(app: App):
    from nonebot.params import DependParam
    from plugin import test, runned, depend, depend_no_cache, test_no_cache
    from utils import make_fake_event

    async with app.test_dependent(depend, allow_types=[DependParam]) as ctx:
        ctx.should_return(1)
    
    # runned = [1]
    assert len(runned) == 1 and runned[0] == 1
    runned.clear()

    async with app.test_matcher(test) as ctx:
        bot = ctx.create_bot()
        event_next = make_fake_event()()  # 这里的event替换为对应平台的事件类型
        ctx.receive_event(bot, event_next)
  
    # runned = [1, 1]
    assert len(runned) == 2 and runned[0] == runned[1] == 1
    runned.clear()

    async with app.test_dependent(depend, allow_types=[DependParam]) as ctx:
        ctx.should_return(1)
    
    # runned = [1]
    assert len(runned) == 1 and runned[0] == 1
    runned.clear()
  
    async with app.test_matcher(test_no_cache) as ctx:
        bot = ctx.create_bot()
        event_next = make_fake_event()()  # 这里的event替换为对应平台的事件类型
        ctx.receive_event(bot, event_next)
    
    # runned = [1, 1, 1]
    assert len(runned) == 3 and runned[0] == runned[1] == runned[2] == 1
```

上面的测试是可以通过的，那么发生了什么？

在第一个依赖函数 `depend` 被调用时，列表 `runned` 添加元素 `1`，在随后的测试事件响应器中，由于使用了缓存，会使用依赖函数 `depend` 的 `runned` 并添加元素 `1`
，这时 `runned=[1, 1]`，所以断言 `len(runned) == 2 and runned[0] == runned[1] == 1` 通过。

第二个的事件响应器前， `runned = [1, 1]`，由于并未使用缓存，所以使用的是全局变量 `runned` 来添加元素 `1`，这时 `runned = [1, 1, 1]`
，所以断言 `len(runned) == 3 and runned[0] == runned[1] == runned[2] == 1` 通过。

通过上面的例子可以看到，测试依赖缓存就是检查依赖预期输出是否符合同一事件响应的依赖缓存的值。

## 测试 Class 依赖

测试 Class 依赖与测试基本依赖注入方法一致。

```python title=plugin.py
from nonebot.params import Depends
from nonebot.plugin import on_message

test = on_message()


class DependClass:
    def __init__(self):
        self.result = True


@test.handle()
async def depend(x: DependClass = Depends(DependClass)):
    return x.result


# 等同于下面
@test.handle()
async def depend_by_type_hints(x: DependClass = Depends()):
    return x.result
```

```python title=test_plugin.py
import pytest

from nonebug import App


@pytest.mark.asyncio
async def test_depend(app: App):
    from nonebot.internal.params import DependParam
    from plugin import depend, DependClass

    async with app.test_dependent(depend, allow_types=[DependParam]) as ctx:
        ctx.should_return(True)

    # 等同于下面
    async with app.test_dependent(depend, allow_types=[DependParam]) as ctx:
        ctx.should_return(DependClass().result)
```

:::warning 警告
因为内存地址的不同，请不要使用实例化的依赖类对结果进行断言，而应使用常量或者类属性，除非重写 `__eq__` （和 `__hash__`） 方法。

```python {5-10}
class DependClass:
    def __init__(self):
        self.result = True

    def __eq__(self, other):
        if isinstance(other, DependClass):
            return self.result == other.result
        elif isinstance(other, bool):
            return self.result == other
        return False
```

:::

## 测试含有参数的依赖函数

大部分时候，依赖函数需要接受其他参数，这时可以通过设置方法的 `allow_types` 参数来设置接受的参数类型，使用 `DependentMixin` 的 `pass_params` 方法可以将函数需要的参数传入。

`allow_types` 的类型是 `List[Param]`，需要根据参数类型添加。

下面是参数类型对应的 `Param` 类型表格。

| 类型             | `Param` 类型                                                                                                                                            |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| DependParam    | 在有其他类型参数或无参数时使用                                                                                                                                       |
| EventParam     | 参数包含 `Event` 类型或者为 `EventMessage`，`EventPlainText`，`EventToMe` 或 `EventType`                                                                          |
| MatcherParam   | 参数包含 `Matcher` 类型                                                                                                                                     |
| ArgParam       | 参数为 `Arg`，`ArgStr` 或 `ArgPlainText`                                                                                                                   |
| ExceptionParam | 参数包含异常类                                                                                                                                               |
| DefaultParam   | 参数含有默认值                                                                                                                                               |
| BotParam       | 参数包含 `Bot` 类型                                                                                                                                         |
| StateParam     | 参数包含 `T_State` 类型或者为 `Command`，`RawCommand`，`CommandArg`，`ShellCommandArgs`，`ShellCommandArgv`，`RegexDict`，`RegexGroup`，`RegexGroup` 和 `RegexMatched` |                                                   |

下面是一个简单的测试用例。

```python title=test_plugin.py
import pytest

from nonebug import App


@pytest.mark.asyncio
async def test_depend(app: App):
    from nonebot.params import BotParam, EventParam, DependParam, StateParam
    from plugin import dependency
    from utils import make_fake_event

    async with app.test_dependent(dependency, allow_types=[BotParam, EventParam]) as ctx:
        bot = ctx.create_bot()
        event = make_fake_event()()  # 这里的event替换为对应平台的事件类型
        ctx.pass_params(bot=bot, event=event)
        ctx.should_return({'self_id': bot.self_id, 'is_tome': event.is_tome()})
```

<details>

<summary>示例插件</summary>

```python title=plugin.py
from nonebot import Bot
from nonebot.adapters import Event


def dependency(bot: Bot, event: Event):
    return {'self_id': bot.self_id, 'is_tome': event.is_tome()}
```

</details>
