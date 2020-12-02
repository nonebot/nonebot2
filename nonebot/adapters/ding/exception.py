from nonebot.exception import AdapterException


class DingAdapterException(AdapterException):

    def __init__(self) -> None:
        super.__init__("DING")


class ApiError(DingAdapterException):
    """
    :说明:

      API 请求成功返回数据，但 API 操作失败。

    """

    def __init__(self, errcode: int, errmsg: str):
        self.errcode = errcode
        self.errmsg = errmsg

    def __repr__(self):
        return f"<ApiError errcode={self.errcode} errmsg={self.errmsg}>"


class SessionExpired(DingAdapterException):

    def __repr__(self) -> str:
        return f"<sessionWebhook is Expired>"
