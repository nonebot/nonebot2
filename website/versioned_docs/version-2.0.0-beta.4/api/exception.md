---
sidebar_position: 10
description: nonebot.exception 模块
---

# nonebot.exception

本模块包含了所有 NoneBot 运行时可能会抛出的异常。

这些异常并非所有需要用户处理，在 NoneBot 内部运行时被捕获，并进行对应操作。

```bash
NoneBotException
├── ParserExit
├── ProcessException
|   ├── IgnoredException
|   ├── SkippedException
|   |   └── TypeMisMatch
|   ├── MockApiException
|   └── StopPropagation
├── MatcherException
|   ├── PausedException
|   ├── RejectedException
|   └── FinishedException
├── AdapterException
|   ├── NoLogException
|   ├── ApiNotAvailable
|   ├── NetworkError
|   └── ActionFailed
└── DriverException
    └── WebSocketClosed
```

## _class_ `NoneBotException()` {#NoneBotException}

- **说明**

  所有 NoneBot 发生的异常基类。

## _class_ `ParserExit(status=0, message=None)` {#ParserExit}

- **说明**

  [shell_command](./rule.md#shell_command) 处理消息失败时返回的异常

- **参数**

  - `status` (int)

  - `message` (str | None)

## _class_ `ProcessException()` {#ProcessException}

- **说明**

  事件处理过程中发生的异常基类。

## _class_ `IgnoredException(reason)` {#IgnoredException}

- **说明**

  指示 NoneBot 应该忽略该事件。可由 PreProcessor 抛出。

- **参数**

  - `reason` (Any): 忽略事件的原因

## _class_ `SkippedException()` {#SkippedException}

- **说明**

  指示 NoneBot 立即结束当前 `Dependent` 的运行。

  例如，可以在 `Handler` 中通过 [Matcher.skip](./matcher.md#Matcher-skip) 抛出。

- **用法**

  ```python
  def always_skip():
      Matcher.skip()

  @matcher.handle()
  async def handler(dependency = Depends(always_skip)):
      # never run
  ```

## _class_ `TypeMisMatch(param, value)` {#TypeMisMatch}

- **说明**

  当前 `Handler` 的参数类型不匹配。

- **参数**

  - `param` (pydantic.fields.ModelField)

  - `value` (Any)

## _class_ `MockApiException(result)` {#MockApiException}

- **说明**

  指示 NoneBot 阻止本次 API 调用或修改本次调用返回值，并返回自定义内容。可由 api hook 抛出。

- **参数**

  - `result` (Any): 返回的内容

## _class_ `StopPropagation()` {#StopPropagation}

- **说明**

  指示 NoneBot 终止事件向下层传播。

  在 {ref}`nonebot.matcher.Matcher.block` 为 `True`
  或使用 [Matcher.stop_propagation](./matcher.md#Matcher-stop_propagation) 方法时抛出。

- **用法**

  ```python
  matcher = on_notice(block=True)
  # 或者
  @matcher.handle()
  async def handler(matcher: Matcher):
      matcher.stop_propagation()
  ```

## _class_ `MatcherException()` {#MatcherException}

- **说明**

  所有 Matcher 发生的异常基类。

## _class_ `PausedException()` {#PausedException}

- **说明**

  指示 NoneBot 结束当前 `Handler` 并等待下一条消息后继续下一个 `Handler`。可用于用户输入新信息。

  可以在 `Handler` 中通过 [Matcher.pause](./matcher.md#Matcher-pause) 抛出。

- **用法**

  ```python
  @matcher.handle()
  async def handler():
      await matcher.pause("some message")
  ```

## _class_ `RejectedException()` {#RejectedException}

- **说明**

  指示 NoneBot 结束当前 `Handler` 并等待下一条消息后重新运行当前 `Handler`。可用于用户重新输入。

  可以在 `Handler` 中通过 [Matcher.reject](./matcher.md#Matcher-reject) 抛出。

- **用法**

  ```python
  @matcher.handle()
  async def handler():
      await matcher.reject("some message")
  ```

## _class_ `FinishedException()` {#FinishedException}

- **说明**

  指示 NoneBot 结束当前 `Handler` 且后续 `Handler` 不再被运行。可用于结束用户会话。

  可以在 `Handler` 中通过 [Matcher.finish](./matcher.md#Matcher-finish) 抛出。

- **用法**

  ```python
  @matcher.handle()
  async def handler():
      await matcher.finish("some message")
  ```

## _class_ `AdapterException(adapter_name)` {#AdapterException}

- **说明**

  代表 `Adapter` 抛出的异常，所有的 `Adapter` 都要在内部继承自这个 `Exception`

- **参数**

  - `adapter_name` (str): 标识 adapter

## _class_ `NoLogException(adapter_name)` {#NoLogException}

- **说明**

  指示 NoneBot 对当前 `Event` 进行处理但不显示 Log 信息。

  可在 [Event.get_log_string](./adapters/index.md#Event-get_log_string) 时抛出

- **参数**

  - `adapter_name` (str)

## _class_ `ApiNotAvailable(adapter_name)` {#ApiNotAvailable}

- **说明**

  在 API 连接不可用时抛出。

- **参数**

  - `adapter_name` (str)

## _class_ `NetworkError(adapter_name)` {#NetworkError}

- **说明**

  在网络出现问题时抛出，如: API 请求地址不正确, API 请求无返回或返回状态非正常等。

- **参数**

  - `adapter_name` (str)

## _class_ `ActionFailed(adapter_name)` {#ActionFailed}

- **说明**

  API 请求成功返回数据，但 API 操作失败。

- **参数**

  - `adapter_name` (str)

## _class_ `DriverException()` {#DriverException}

- **说明**

  `Driver` 抛出的异常基类

## _class_ `WebSocketClosed(code, reason=None)` {#WebSocketClosed}

- **说明**

  WebSocket 连接已关闭

- **参数**

  - `code` (int)

  - `reason` (str | None)
