"""本模块包含了所有 NoneBot 运行时可能会抛出的异常。

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

FrontMatter:
    mdx:
        format: md
    sidebar_position: 10
    description: nonebot.exception 模块
"""

from typing import Any, Optional

from nonebot.compat import ModelField


class NoneBotException(Exception):
    """所有 NoneBot 发生的异常基类。"""

    def __str__(self) -> str:
        return self.__repr__()


# Rule Exception
class ParserExit(NoneBotException):
    """{ref}`nonebot.rule.shell_command` 处理消息失败时返回的异常。"""

    def __init__(self, status: int = 0, message: Optional[str] = None) -> None:
        self.status = status
        self.message = message

    def __repr__(self) -> str:
        return (
            f"ParserExit(status={self.status}"
            + (f", message={self.message!r}" if self.message else "")
            + ")"
        )


# Processor Exception
class ProcessException(NoneBotException):
    """事件处理过程中发生的异常基类。"""


class IgnoredException(ProcessException):
    """指示 NoneBot 应该忽略该事件。可由 PreProcessor 抛出。

    参数:
        reason: 忽略事件的原因
    """

    def __init__(self, reason: Any) -> None:
        self.reason: Any = reason

    def __repr__(self) -> str:
        return f"IgnoredException(reason={self.reason!r})"


class SkippedException(ProcessException):
    """指示 NoneBot 立即结束当前 `Dependent` 的运行。

    例如，可以在 `Handler` 中通过 {ref}`nonebot.matcher.Matcher.skip` 抛出。

    用法:
        ```python
        def always_skip():
            Matcher.skip()

        @matcher.handle()
        async def handler(dependency = Depends(always_skip)):
            # never run
        ```
    """


class TypeMisMatch(SkippedException):
    """当前 `Handler` 的参数类型不匹配。"""

    def __init__(self, param: ModelField, value: Any) -> None:
        self.param: ModelField = param
        self.value: Any = value

    def __repr__(self) -> str:
        return (
            f"TypeMisMatch(param={self.param.name}, "
            f"type={self.param._type_display()}, value={self.value!r}>"
        )


class MockApiException(ProcessException):
    """指示 NoneBot 阻止本次 API 调用或修改本次调用返回值，并返回自定义内容。
    可由 api hook 抛出。

    参数:
        result: 返回的内容
    """

    def __init__(self, result: Any):
        self.result = result

    def __repr__(self) -> str:
        return f"MockApiException(result={self.result!r})"


class StopPropagation(ProcessException):
    """指示 NoneBot 终止事件向下层传播。

    在 {ref}`nonebot.matcher.Matcher.block` 为 `True`
    或使用 {ref}`nonebot.matcher.Matcher.stop_propagation` 方法时抛出。

    用法:
        ```python
        matcher = on_notice(block=True)
        # 或者
        @matcher.handle()
        async def handler(matcher: Matcher):
            matcher.stop_propagation()
        ```
    """


# Matcher Exceptions
class MatcherException(NoneBotException):
    """所有 Matcher 发生的异常基类。"""


class PausedException(MatcherException):
    """指示 NoneBot 结束当前 `Handler` 并等待下一条消息后继续下一个 `Handler`。
    可用于用户输入新信息。

    可以在 `Handler` 中通过 {ref}`nonebot.matcher.Matcher.pause` 抛出。

    用法:
        ```python
        @matcher.handle()
        async def handler():
            await matcher.pause("some message")
        ```
    """


class RejectedException(MatcherException):
    """指示 NoneBot 结束当前 `Handler` 并等待下一条消息后重新运行当前 `Handler`。
    可用于用户重新输入。

    可以在 `Handler` 中通过 {ref}`nonebot.matcher.Matcher.reject` 抛出。

    用法:
        ```python
        @matcher.handle()
        async def handler():
            await matcher.reject("some message")
        ```
    """


class FinishedException(MatcherException):
    """指示 NoneBot 结束当前 `Handler` 且后续 `Handler` 不再被运行。可用于结束用户会话。

    可以在 `Handler` 中通过 {ref}`nonebot.matcher.Matcher.finish` 抛出。

    用法:
        ```python
        @matcher.handle()
        async def handler():
            await matcher.finish("some message")
        ```
    """


# Adapter Exceptions
class AdapterException(NoneBotException):
    """代表 `Adapter` 抛出的异常，所有的 `Adapter` 都要在内部继承自这个 `Exception`。

    参数:
        adapter_name: 标识 adapter
    """

    def __init__(self, adapter_name: str, *args: object) -> None:
        super().__init__(*args)
        self.adapter_name: str = adapter_name


class NoLogException(AdapterException):
    """指示 NoneBot 对当前 `Event` 进行处理但不显示 Log 信息。

    可在 {ref}`nonebot.adapters.Event.get_log_string` 时抛出
    """


class ApiNotAvailable(AdapterException):
    """在 API 连接不可用时抛出。"""


class NetworkError(AdapterException):
    """在网络出现问题时抛出，
    如: API 请求地址不正确, API 请求无返回或返回状态非正常等。
    """


class ActionFailed(AdapterException):
    """API 请求成功返回数据，但 API 操作失败。"""


# Driver Exceptions
class DriverException(NoneBotException):
    """`Driver` 抛出的异常基类。"""


class WebSocketClosed(DriverException):
    """WebSocket 连接已关闭。"""

    def __init__(self, code: int, reason: Optional[str] = None) -> None:
        self.code = code
        self.reason = reason

    def __repr__(self) -> str:
        return (
            f"WebSocketClosed(code={self.code}"
            + (f", reason={self.reason!r}" if self.reason else "")
            + ")"
        )
