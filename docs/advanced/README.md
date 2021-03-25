# 深入

## 它如何工作？

如同[概览](../guide/README.md)所言:

> NoneBot2 是一个可扩展的 Python 异步机器人框架，它会对机器人收到的事件进行解析和处理，并以插件化的形式，按优先级分发给事件所对应的事件响应器，来完成具体的功能。

`Nonebot2` 是一个可以对机器人上报的事件进行处理并完成具体功能的机器人框架，在这里，我们将简要讲述它的工作内容。

**便捷起见，以下内容对 `Nonebot2` 会被称为 `nonebot`，与 `Nonebot2` 交互的机器人实现会被称为 `协议端`**。

在实际应用中，`nonebot` 会充当一个高性能，轻量级的 Python 微服务框架。协议端可以通过 `http`, `websocket` 等方式与之通信，这个通信往往是双向的：一方面，协议端可以上报数据给 `nonebot`，`nonebot` 会处理数据并返回响应给协议端；另一方面，`nonebot` 可以主动推送数据给协议端。而 `nonebot` 便是围绕双向通信进行工作的。

在开始工作之前，`nonebot` 需要进行准备工作：

1. **运行 `nonebot.init` 初始化函数**，它会读取配置文件，并初始化 `nonebot` 和后端驱动 `driver` 对象。
2. **注册协议适配器 `adapter`** 。
3. **加载插件**。

准备工作完成后，`nonebot` 会利用 `uvicorn` 启动，并运行 `on_startup` 钩子函数。

随后，倘若一个协议端与 `nonebot` 进行了连接，`nonebot` 的后端驱动 `driver` 就会将 `adapter` 实例化为 `bot`，`nonebot` 便会利用 `bot` 开始工作，它的工作内容分为两个方面：

1. **事件处理**，`bot` 会将协议端上报的数据转化为 `事件`(`Event`)，之后 `nonebot` 会根据一套既定流程来处理 `事件`。

2. **调用 `API`**, 在**事件处理**的过程中，`nonebot` 可以通过 `bot` 调用协议端指定的 `API` 来获取更多数据，或者反馈响应给协议端; `nonebot` 也可以通过调用 `API` 向协议端主动请求数据或者主动推送数据。

在**指南**模块， 我们已经叙述了[如何配置 nonebot](../guide/basic-configuration.md), [如何注册协议适配器](../guide/getting-started.md)，[如何加载插件](../guide/loading-a-plugin.md), 在这里便不再赘述。

下面，我们将对**事件处理**， **调用 API**进行说明。

## 事件处理

我们可以先看事件处理的流程图：

![handle-event](../guide/images/Handle-Event.png)

在流程图里，我们可以看到，`nonebot` 会有三个阶段来处理事件：

1. **driver 处理上报数据**
2. **adapter 处理原始数据**
3. **nonebot 处理 Event**

我们将顺序说明这三个阶段。其中，会将第三个阶段拆分成**概念解释**，**处理 Event**，**特殊异常处理**三个部分来说明。

### driver 处理上报数据

1. 协议端会通过 `websocket` 或者 `http` 等方式与 `nonebot` 的后端驱动 `driver` 连接，`driver` 会根据之前注册的 `adapter` 和配置文件的内容来进行鉴权，从而获得这个连接的唯一识别 id `self-id`，随后 `adapter` 就会利用 `self-id` 实例化为 `bot` 对象。

   ::: tip
   需要注意的是，如果协议端通过 `websocket` 与 `nonebot` 连接，这个步骤只会在建立连接时进行，并在之后运行 `on_bot_connect` 钩子函数；通过 `http` 方式连接时，会在协议端每次上报数据时都进行这个步骤。
   :::

   ::: warning
   连接之前必须要注册 `adapter`
   :::

   ::: warning
   `self-id` 是帐号的唯一识别 ID，这意味着不能出现相同的 `self-id`。
   :::

2. `driver` 会将接收到的数据转交给 `bot` 对象进一步处理。

### adapter 处理原始数据

1. `bot` 会利用事先定义好的 `Event Model` 对上报的数据进行分析处理，将数据转化为 `nonebot` 可以处理的 `Event` 对象。

   ::: tip
   `adapter` 在转换数据格式的同时可以进行一系列的特殊操作，例如 `CQHTTP` 会对 `reply` 信息进行提取。
   :::

2. `Event` 会传入 `nonebot` 做进一步处理。

### nonebot 处理 Event

在讲述这个阶段之前，我们需要先对几个概念进行解释。

#### 概念解释

1. **hook**，或者说**钩子函数**，它们可以在 `nonebot` 处理 `Event` 的不同时刻进行拦截，修改或者扩展，在 `nonebot` 中，钩子函数分为 `事件预处理hook`，`运行预处理hook`，`运行后处理hook` 和 `事件后处理hook`。

   ::: tip
   关于`hook`的更多信息，可以查阅[这里](./runtime-hook.md)
   :::

2. **Matcher**与**matcher**，在**指南**中，我们讲述了[如何注册事件响应器](../guide/creating-a-matcher)，这里的事件响应器或者说 `Matcher` 并不是一个具体的实例 `instance`，而是一个具有特定属性的类 `class`。只有当 `Matcher` **响应事件**时，才会实例化为具体的 `instance`，也就是 `matcher`。`matcher` 可以认为是 `nonebot` 处理 `Event` 的基本单位，运行 `matcher` 是`nonebot`工作的主要内容。

3. **handler**，或者说**事件处理函数**, 它们可以认为是 `nonebot` 处理 `Event` 的最小单位。在不考虑 `hook` 的情况下，**运行 matcher 就是顺序运行 matcher.handlers**，这句话换种表达方式就是，`handler` 只有添加到 `matcher.handlers` 时，才可以参与到 `nonebot` 的工作中来。

   ::: tip
   如何让 `handler` 添加到 `matcher.handlers`？

   一方面，我们可以参照[这里](../guide/creating-a-handler)利用装饰器来添加；另一方面，我们在用 `on()` 或者 `on_*()` 注册事件响应器时，可以添加 `handlers=[handler1, handler2, ...]` 这样的关键词参数来添加。
   :::

#### 处理 Event

1. **执行事件预处理 hook**， `nonebot` 接收到 `Event` 后，会传入到 `事件预处理hook` 中进行处理。

   ::: warning
   需要注意的是，执行多个 `事件预处理hook` 时并无顺序可言，它们是**并行运行**的。这个原则同样适用于其他的 `hook`。
   :::

2. **按优先级升序选出同一优先级的 Matcher**，`nonebot` 提供了一个全局字典 `matchers`，这个字典的 `key` 是优先级 `priority`，`value` 是一个 `list`，里面存放着同一优先级的 `Matcher`。在注册 `Matcher` 时，它和优先级 `priority` 会添加到里面。

   在执行 `事件预处理hook` 后，`nonebot` 会对 `matchers` 的 `key` 升序排序并选择出当前最小优先级的 `Matcher`。

3. **根据 Matcher 定义的 Rule, Permission 判断是否运行**，在选出 `Matcher` 后，`nonebot` 会将 `bot`，`Event` 传入到 `Matcher.check_rule` 和 `Matcher.check_perm` 两个函数中，两个函数分别对 Matcher 定义的 Rule, Permission 进行 check，当 check 通过后，这个 `Matcher` 就会响应事件。但是当同一个优先级的所有 `Matcher` 均没有响应时，`nonebot` 会返回到上一个步骤，选择出下一优先级的 `Matcher`。

4. **实例化 matcher 并执行运行预处理 hook**，当 `Matcher` 响应事件后，它便会实例化为 `matcher`，并执行 `运行预处理hook`。

5. **顺序运行 matcher 的所有 handlers**，`运行预处理hook` 执行完毕后，便会运行 `matcher`，也就是**顺序运行**它的 `handlers`。

   ::: tip
   `matcher` 运行 `handlers` 的顺序是: 先运行该 `matcher` 的类 `Matcher` 注册时添加的 `handlers`(如果有的话)，再按照装饰器装饰顺序运行装饰的 `handlers`。
   :::

6. **执行运行后处理 hook**，`matcher` 的 `handlers` 运行完毕后，会执行 `运行后处理hook`。

7. **判断是否停止事件传播**，`nonebot` 会根据当前优先级所有 `matcher` 的 `block` 参数或者 `StopPropagation` 异常判断是否停止传播 `Event`，如果事件没有停止传播，`nonebot` 便会返回到第 2 步， 选择出下一优先级的 `Matcher`。

8. **执行事件后处理 hook**，在 `Event` 停止传播或执行完所有响应的 `Matcher` 后，`nonebot` 会执行 `事件后处理hook`。

   当 `事件后处理hook` 执行完毕后，当前`Event`的处理周期就顺利结束了。

#### 特殊异常处理

在这个阶段，`nonebot` 规定了几个特殊的异常，当 `nonebot` 捕获到它们时，会用特定的行为来处理它们。

1. **IgnoredException**

   这个异常可以在 `事件预处理hook` 和 `运行预处理hook` 抛出。

   当 `事件预处理hook` 抛出它时，`nonebot` 会忽略当前的 `Event`，不进行处理。

   当 `运行预处理hook` 抛出它时，`nonebot` 会忽略当前的 `matcher`，结束当前 `matcher` 的运行。

   ::: warning
   当 `hook` 需要抛出这个异常时，要写明原因。
   :::

2. **PausedException**

   这个异常可以在 `handler` 中由 `Matcher.pause` 抛出。

   当 `nonebot` 捕获到它时，会停止运行当前 `handler` 并结束当前 `matcher` 的运行，并将后续的 `handler` 交给一个临时 `Matcher` 来响应当前交互用户的下一个消息事件，当临时 `Matcher` 响应时，临时 `Matcher` 会运行后续的 handlers。

3. **RejectedException**

   这个异常可以在 `handler` 中由 `Matcher.reject` 抛出。

   当 `nonebot` 捕获到它时，会停止运行当前 `handler` 并结束当前 `matcher` 的运行，并将当前 handler 和后续 `handler` 交给一个临时 `Matcher` 来响应当前交互用户的下一个消息事件，当临时 `Matcher` 响应时，临时 `Matcher` 会运行当前 `handler` 和后续的 `handler`。

4. **FinishedException**

   这个异常可以在 `handler` 中由 `Matcher.finish` 抛出。

   当 `nonebot` 捕获到它时，会停止运行当前 `handler` 并结束当前 `matcher` 的运行。

5. **StopPropagation**

   这个异常一般会在执行 `运行后处理hook` 后抛出。

   当 `nonebot` 捕获到它时， 会停止传播当前 `Event`，不再寻找下一优先级的 `Matcher`，直接执行 `事件后处理hook`。

## 调用 API

`nonebot` 可以通过 `bot` 来调用 `API` ，`API` 可以向协议端发送数据，也可以向协议端请求更多的数据。

::: tip
不同 `adapter` 规定了不同的 API，对应的 API 列表请参照协议规范。
:::

一般来说，我们可以用 `bot.*` 来调用 `API`(\*是 `API` 的 `action` 或者 `endpoint`)。

对于发送消息而言，一方面可以调用既有的 API；另一方面 `nonebot` 实现了两个便捷方法，`bot.send(event, message, **kwargs)` 方法和可以在 `handler` 中使用的 `Matcher.send(message, **kwargs)` 方法，来向事件主体发送消息。
