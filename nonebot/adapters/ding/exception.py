from typing import Optional

from nonebot.exception import (AdapterException, ActionFailed as
                               BaseActionFailed, ApiNotAvailable as
                               BaseApiNotAvailable, NetworkError as
                               BaseNetworkError)


class DingAdapterException(AdapterException):
    """
    :说明:

      钉钉 Adapter 错误基类
    """

    def __init__(self) -> None:
        super().__init__("ding")


class ActionFailed(BaseActionFailed, DingAdapterException):
    """
    :说明:

      API 请求返回错误信息。

    :参数:

      * ``errcode: Optional[int]``: 错误码
      * ``errmsg: Optional[str]``: 错误信息
    """

    def __init__(self,
                 errcode: Optional[int] = None,
                 errmsg: Optional[str] = None):
        super().__init__()
        self.errcode = errcode
        self.errmsg = errmsg

    def __repr__(self):
        return f"<ApiError errcode={self.errcode} errmsg=\"{self.errmsg}\">"

    def __str__(self):
        return self.__repr__()


class ApiNotAvailable(BaseApiNotAvailable, DingAdapterException):
    pass


class NetworkError(BaseNetworkError, DingAdapterException):
    """
    :说明:

      网络错误。

    :参数:

      * ``retcode: Optional[int]``: 错误码
    """

    def __init__(self, msg: Optional[str] = None):
        super().__init__()
        self.msg = msg

    def __repr__(self):
        return f"<NetWorkError message={self.msg}>"

    def __str__(self):
        return self.__repr__()


class SessionExpired(ApiNotAvailable, DingAdapterException):
    """
    :说明:

      发消息的 session 已经过期。
    """

    def __repr__(self) -> str:
        return f"<Session Webhook is Expired>"

    def __str__(self):
        return self.__repr__()
