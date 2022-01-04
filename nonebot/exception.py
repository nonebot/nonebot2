"""
异常
====

下列文档中的异常是所有 NoneBot 运行时可能会抛出的。
这些异常并非所有需要用户处理，在 NoneBot 内部运行时被捕获，并进行对应操作。
"""

from typing import Any, Optional

from pydantic.fields import ModelField


class NoneBotException(Exception):
    """
    :说明:

      所有 NoneBot 发生的异常基类。
    """


# Rule Exception
class ParserExit(NoneBotException):
    """
    :说明:

      ``shell command`` 处理消息失败时返回的异常

    :参数:

      * ``status``
      * ``message``
    """

    def __init__(self, status: int = 0, message: Optional[str] = None):
        self.status = status
        self.message = message

    def __repr__(self):
        return f"<ParserExit status={self.status} message={self.message}>"

    def __str__(self):
        return self.__repr__()


# Processor Exception
class ProcessException(NoneBotException):
    """
    :说明:

      事件处理过程中发生的异常基类。
    """


class IgnoredException(ProcessException):
    """
    :说明:

      指示 NoneBot 应该忽略该事件。可由 PreProcessor 抛出。

    :参数:

      * ``reason``: 忽略事件的原因
    """

    def __init__(self, reason):
        self.reason = reason

    def __repr__(self):
        return f"<IgnoredException, reason={self.reason}>"

    def __str__(self):
        return self.__repr__()


class MockApiException(ProcessException):
    """
    :说明:

      指示 NoneBot 阻止本次 API 调用或修改本次调用返回值，并返回自定义内容。可由 api hook 抛出。

    :参数:

      * ``result``: 返回的内容
    """

    def __init__(self, result: Any):
        self.result = result

    def __repr__(self):
        return f"<ApiCancelledException, result={self.result}>"

    def __str__(self):
        return self.__repr__()


class StopPropagation(ProcessException):
    """
    :说明:

      指示 NoneBot 终止事件向下层传播。

    :用法:

      在 ``Matcher.block == True`` 时抛出。
    """


# Matcher Exceptions
class MatcherException(NoneBotException):
    """
    :说明:

      所有 Matcher 发生的异常基类。
    """


class SkippedException(MatcherException):
    """
    :说明:

      指示 NoneBot 立即结束当前 ``Handler`` 的处理，继续处理下一个 ``Handler``。

    :用法:

      可以在 ``Handler`` 中通过 ``Matcher.skip()`` 抛出。
    """


class TypeMisMatch(SkippedException):
    """
    :说明:

      当前 ``Handler`` 的参数类型不匹配。
    """

    def __init__(self, param: ModelField, value: Any):
        self.param: ModelField = param
        self.value: Any = value

    def __repr__(self):
        return f"<TypeMisMatch, param={self.param}, value={self.value}>"

    def __str__(self):
        self.__repr__()


class PausedException(MatcherException):
    """
    :说明:

      指示 NoneBot 结束当前 ``Handler`` 并等待下一条消息后继续下一个 ``Handler``。
      可用于用户输入新信息。

    :用法:

      可以在 ``Handler`` 中通过 ``Matcher.pause()`` 抛出。
    """


class RejectedException(MatcherException):
    """
    :说明:

      指示 NoneBot 结束当前 ``Handler`` 并等待下一条消息后重新运行当前 ``Handler``。
      可用于用户重新输入。

    :用法:

      可以在 ``Handler`` 中通过 ``Matcher.reject()`` 抛出。
    """


class FinishedException(MatcherException):
    """
    :说明:

      指示 NoneBot 结束当前 ``Handler`` 且后续 ``Handler`` 不再被运行。
      可用于结束用户会话。

    :用法:

      可以在 ``Handler`` 中通过 ``Matcher.finish()`` 抛出。
    """


# Adapter Exceptions
class AdapterException(NoneBotException):
    """
    :说明:

      代表 ``Adapter`` 抛出的异常，所有的 ``Adapter`` 都要在内部继承自这个 ``Exception``

    :参数:

      * ``adapter_name: str``: 标识 adapter
    """

    def __init__(self, adapter_name: str) -> None:
        self.adapter_name = adapter_name


class NoLogException(AdapterException):
    """
    :说明:

      指示 NoneBot 对当前 ``Event`` 进行处理但不显示 Log 信息，可在 ``get_log_string`` 时抛出
    """

    pass


class ApiNotAvailable(AdapterException):
    """
    :说明:

      在 API 连接不可用时抛出。
    """

    pass


class NetworkError(AdapterException):
    """
    :说明:

      在网络出现问题时抛出，如: API 请求地址不正确, API 请求无返回或返回状态非正常等。
    """

    pass


class ActionFailed(AdapterException):
    """
    :说明:

      API 请求成功返回数据，但 API 操作失败。
    """

    pass


# Driver Exceptions
class DriverException(NoneBotException):
    """
    :说明:

      ``Driver`` 抛出的异常基类
    """


class WebSocketClosed(DriverException):
    """
    :说明:

      WebSocket 连接已关闭
    """

    def __init__(self, code: int, reason: Optional[str] = None):
        self.code = code
        self.reason = reason

    def __repr__(self) -> str:
        return f"<WebSocketClosed code={self.code} reason={self.reason}>"
