---
sidebar_position: 7
description: 控制会话响应对象

options:
  menu:
    - category: advanced
      weight: 80
---

# 会话更新

在 NoneBot 中，在某个事件响应器对事件响应后，即是进入了会话状态，会话状态会持续到整个事件响应流程结束。会话过程中，机器人可以与用户进行多次交互。每次需要等待用户事件时，NoneBot 将会复制一个新的临时事件响应器，并更新该事件响应器使其响应当前会话主体的消息，这个过程称为会话更新。

会话更新分为两部分：**更新[事件响应器类型](./matcher.md#事件响应器类型)**和**更新[事件触发权限](./matcher.md#事件触发权限)**。

## 更新事件响应器类型

通常情况下，与机器人用户进行的会话都是通过消息事件进行的，因此会话更新后的默认响应事件类型为 `message`。如果希望接收一个特定类型的消息，比如 `notice` 等，我们需要自定义响应事件类型更新函数。响应事件类型更新函数是一个 `Dependent`，可以使用依赖注入。

```python {3-5}
foo = on_message()

@foo.type_updater
async def _() -> str:
    return "notice"
```

在注册了上述响应事件类型更新函数后，当我们需要等待用户事件时，将只会响应 `notice` 类型的事件。如果希望在会话过程中的不同阶段响应不同类型的事件，我们就需要使用更复杂的逻辑来更新响应事件类型（如：根据会话状态），这里将不再展示。

## 更新事件触发权限

会话通常是由机器人与用户进行的一对一交互，因此会话更新后的默认触发权限为当前事件的会话 ID。这个会话 ID 由协议适配器生成，通常由用户 ID 和群 ID 等组成。如果希望实现更复杂的会话功能（如：多用户同时参与的会话），我们需要自定义触发权限更新函数。触发权限更新函数是一个 `Dependent`，可以使用依赖注入。

```python {5-7}
from nonebot.permission import User

foo = on_message()

@foo.permission_updater
async def _(event: Event, matcher: Matcher) -> Permission:
    return Permission(User.from_event(event, perm=matcher.permission))
```

上述权限更新函数是默认的权限更新函数，它将会话的触发权限更新为当前事件的会话 ID。如果我们希望响应多个用户的消息，我们可以如下修改：

```python {5-7}
from nonebot.permission import USER

foo = on_message()

@foo.permission_updater
async def _(matcher: Matcher) -> Permission:
    return USER("session1", "session2", perm=matcher.permission)
```

请注意，此处为全大写字母的 `USER` 权限，它可以匹配多个会话 ID。通过这种方式，我们可以实现多用户同时参与的会话。

我们已经了解了如何控制会话的更新，相信你已经能够实现更复杂的会话功能了，例如多人小游戏等等。欢迎将你的作品分享到[插件商店](/store/plugins)。
