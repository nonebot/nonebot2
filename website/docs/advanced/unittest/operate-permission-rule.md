---
sidebar_position: 3
description: 规则和权限操作

options:
menu:
weight: 52
category: advanced
---

# 规则和权限操作

部分事件响应器使用 `Rule` 和 `Permission` 进行限制，这时无法通过普通方法对事件响应器，以及 `Rule` 和 `Permission` 进行测试。

但 NoneBug 提供了 `Rule` 和 `Permission` 的检查/测试/忽略的方法来进行进一步的测试。

接下来将以如下插件进行演示。

<details>
  <summary>示例插件</summary>

```python
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot import on_command

permission = on_command("权限测试", permission=SUPERUSER)
rule = on_command("规则测试", rule=to_me())


@permission.handle()
async def _():
  await permission.finish("权限测试通过")


@rule.handle()
async def _():
  await rule.finish("规则测试通过")

```

</details>

## should_pass_rule 和 should_pass_permission

判断能否通过规则/权限限制。

不通过时引发 `AssertionError`。

```python {3}
msg = Message("/权限测试")
event = make_fake_event(_message=msg, _to_me=True)()  # 这里的event替换为对应平台的事件类型
ctx.should_pass_permission()  # 出错：AssertionError
```

```python {3}
msg = Message("/规则测试")
event = make_fake_event(_message=msg, _to_me=True)()  # 这里的event替换为对应平台的事件类型
ctx.should_pass_rule()  # 通过
ctx.should_send_message(event, "规则测试通过", True)
ctx.should_finished()
```

## should_not_pass_rule 和 should_not_pass_permission

与 `should_pass_rule` 和 `should_pass_permission` 相反。

通过时引发 `AssertionError`。

```python {3}  
msg = Message("/权限测试")
event = make_fake_event(_message=msg, _to_me=True)()  # 这里的event替换为对应平台的事件类型
ctx.should_not_pass_permission()  # 通过
ctx.should_send_message(event, "权限测试通过", True)
ctx.should_finished()
```

```python {3}
msg = Message("/规则测试")
event = make_fake_event(_message=msg, _to_me=True)()
ctx.should_not_pass_rule()  # 出错：AssertionError
```

## should_ignore_rule 和 should_ignore_permission

忽略规则/权限限制。

```python {3}
msg = Message("/权限测试")
event = make_fake_event(_message=msg, _to_me=True)()  # 这里的event替换为对应平台的事件类型
ctx.should_ignore_permission()
ctx.should_send_message(event, "权限测试通过", True)
ctx.should_finished()
```

```python {3}
msg = Message("/规则测试")
event = make_fake_event(_message=msg)()  # 这里的event替换为对应平台的事件类型
ctx.should_ignore_rule()
ctx.should_send_message(event, "规则测试通过", True)
ctx.should_finished()
```
