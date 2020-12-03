from nonebot.exception import AdapterException, ActionFailed, ApiNotAvailable


class DingAdapterException(AdapterException):
    """
    :说明:

      钉钉 Adapter 错误基类

    """

    def __init__(self) -> None:
        super().__init__("ding")


class ApiError(DingAdapterException, ActionFailed):
    """
    :说明:

      API 请求返回错误信息。

    """

    def __init__(self, errcode: int, errmsg: str):
        super().__init__()
        self.errcode = errcode
        self.errmsg = errmsg

    def __repr__(self):
        return f"<ApiError errcode={self.errcode} errmsg={self.errmsg}>"


class SessionExpired(DingAdapterException, ApiNotAvailable):
    """
    :说明:

      发消息的 session 已经过期。

    """

    def __repr__(self) -> str:
        return f"<Session Webhook is Expired>"
