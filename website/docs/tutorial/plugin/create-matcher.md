---
sidebar_position: 3
description: 定义事件响应器，对特定的事件进行处理

options:
  menu:
    weight: 26
    category: guide
---

# 定义事件响应器

事件响应器 (`Matcher`) 是对接收到的事件进行响应的基本单元，所有的事件响应器都继承自 `Matcher` 基类。为方便编写插件，NoneBot 在 `nonebot.plugin` 模块中为插件开发定义了一些辅助函数，以便插件开发者可以简化插件开发。首先，让我们来了解一下 `Matcher` 由哪些部分组成。

## 事件响应器的基本组成

### 事件响应器类型 `type`

事件响应器的类型即是该响应器所要响应的事件类型，只有在接收到的事件类型与该响应器的类型相同时，才会触发该响应器。如果类型留空，则该响应器将会响应所有类型的事件。

NoneBot 内置了四种主要类型：`meta_event`, `message`, `notice`, `request`。通常情况下，协议适配器会将事件合理的分类至这四种类型中。如果有其他类型的事件需要响应，可以自行定义新的类型。

:::warning 注意
当会话状态更新时，会执行 `type_updater` 以更新 `type` 属性，以便会话收到新事件时能够正确匹配。

`type_updater` 默认将 `type` 修改为 `message`，你也可以自行定义 `type_updater` 来控制 `type` 属性更新。`type_updater` 是一个返回 `str` 的函数，可选依赖注入参数参考类型 `T_TypeUpdater`。

```python {3-5}
matcher = on_request()

@matcher.type_updater
async def update_type():
    return "message"
```

:::

### 事件匹配规则 `rule`

事件响应器的匹配规则是一个 `Rule` 对象，它是一系列 `checker` 的集合，当所有的 `checker` 都返回 `True` 时，才会触发该响应器。

规则编写方法参考 [自定义规则](#自定义规则)。

:::warning 注意
当会话状态更新时，`rule` 会被清空，以便会话收到新事件时能够正确匹配。
:::

### 事件触发权限 `permission`

事件响应器的触发权限是一个 `Permission` 对象，它也是一系列 `checker` 的集合，当其中一个 `checker` 返回 `True` 时，就会触发该响应器。

权限编写方法参考 [自定义权限](#自定义权限)。

:::warning 注意
与 `rule` 不同的是，`permission` 不会在会话状态更新时丢失，因此 `permission` 通常用于会话的响应控制。

并且, 当会话状态更新时，会执行 `permission_updater` 以更新 `permission`。默认情况下，`permission_updater` 会在原有的 `permission` 基础上添加一个 `USER` 条件，以检查事件的 `session_id` 是否与当前会话一致。

你可以自行定义 `permission_updater` 来控制会话的响应权限更新。`permission_updater` 是一个返回 `Permission` 的函数，可选依赖注入参数参考类型 `T_PermissionUpdater`。

```python {3-5}
matcher = on_message()

@matcher.permission_updater
async def update_type(matcher: Matcher):
    return matcher.permission  # return same without session_id check
```

:::

### 优先级 `priority`

事件响应器的优先级代表事件响应器的执行顺序

:::warning 警告
同一优先级的事件响应器会 **同时执行**，优先级数字 **越小** 越先响应！优先级请从 `1` 开始排序！
:::

### 阻断 `block`

当有任意事件响应器发出了阻止事件传递信号时，该事件将不再会传递给下一优先级，直接结束处理。

NoneBot 内置的事件响应器中，所有非 `command` 规则的 `message` 类型的事件响应器都会阻断事件传递，其他则不会。

在部分情况中，可以使用 `matcher.stop_propagation()` 方法动态阻止事件传播，该方法需要 `handler` 在参数中获取 `matcher` 实例后调用方法。

```python {5}
foo = on_request()

@foo.handle()
async def handle(matcher: Matcher):
    matcher.stop_propagation()
```

### 有效期 `temp` / `expire_time`

事件响应器可以设置有效期，当事件响应器超过有效期时，将会被移除。

- `temp` 属性：配置事件响应器在下一次响应之后移除。
- `expire_time` 属性：配置事件响应器在指定时间之后移除。

## 自定义规则

## 自定义权限
