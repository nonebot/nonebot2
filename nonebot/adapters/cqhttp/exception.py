from nonebot.exception import AdapterException, ActionFailed


class CQHTTPAdapterException(AdapterException):

    def __init__(self):
        super().__init__("cqhttp")


class ApiError(CQHTTPAdapterException, ActionFailed):
    """
    :说明:

      API 请求返回错误信息。

    :参数:

      * ``retcode: Optional[int]``: 错误码
    """

    def __init__(self, retcode: Optional[int] = None):
        super().__init__()
        self.retcode = retcode

    def __repr__(self):
        return f"<ActionFailed retcode={self.retcode}>"

    def __str__(self):
        return self.__repr__()
