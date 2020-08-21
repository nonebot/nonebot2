#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常
====

下列文档中的异常是所有 NoneBot 运行时可能会抛出的。
这些异常并非所有需要用户处理，在 NoneBot 内部运行时被捕获，并进行对应操作。
"""

from nonebot.typing import List, Type, Optional


class _ExceptionContainer(Exception):

    def __init__(self, exceptions: List[Type[Exception]]) -> None:
        self.exceptions = exceptions


class IgnoredException(Exception):
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


class PausedException(Exception):
    """
    :说明:

      指示 NoneBot 结束当前 ``Handler`` 并等待下一条消息后继续下一个 ``Handler``。
      可用于用户输入新信息。

    :用法:

      可以在 ``Handler`` 中通过 ``Matcher.pause()`` 抛出。
    """
    pass


class RejectedException(Exception):
    """
    :说明:

      指示 NoneBot 结束当前 ``Handler`` 并等待下一条消息后重新运行当前 ``Handler``。
      可用于用户重新输入。

    :用法:

      可以在 ``Handler`` 中通过 ``Matcher.reject()`` 抛出。
    """
    pass


class FinishedException(Exception):
    """
    :说明:

      指示 NoneBot 结束当前 ``Handler`` 且后续 ``Handler`` 不再被运行。
      可用于结束用户会话。

    :用法:

      可以在 ``Handler`` 中通过 ``Matcher.finish()`` 抛出。
    """
    pass


class ExpiredException(Exception):
    """
    :说明:

      指示 NoneBot 当前 ``Matcher`` 已失效。

    :用法:

      当 ``Matcher`` 运行前检查时抛出。
    """
    pass


class StopPropagation(Exception):
    """
    :说明:

      指示 NoneBot 终止事件向下层传播。

    :用法:

      在 ``Matcher.block == True`` 时抛出。
    """
    pass


class ApiNotAvailable(Exception):
    """
    :说明:

      在 API 连接不可用时抛出。
    """
    pass


class NetworkError(Exception):
    """
    :说明:

      在网络出现问题时抛出，如: API 请求地址不正确, API 请求无返回或返回状态非正常等。
    """
    pass


class ActionFailed(Exception):
    """
    :说明:

      API 请求成功返回数据，但 API 操作失败。

    :参数:

      * ``retcode``: 错误代码
    """

    def __init__(self, retcode: Optional[int]):
        self.retcode = retcode

    def __repr__(self):
        return f"<ActionFailed, retcode={self.retcode}>"

    def __str__(self):
        return self.__repr__()
