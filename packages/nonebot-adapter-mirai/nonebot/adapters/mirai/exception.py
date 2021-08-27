from typing import Optional
from nonebot.exception import ActionFailed as BaseActionFailed
from nonebot.exception import AdapterException
from nonebot.exception import ApiNotAvailable as BaseApiNotAvailable
from nonebot.exception import NetworkError as BaseNetworkError


class MiraiAdapterException(AdapterException):

    def __init__(self):
        super().__init__('mirai')


class ActionFailed(BaseActionFailed, MiraiAdapterException):

    def __init__(self, **kwargs):
        super().__init__()
        self.info = kwargs

    def __repr__(self):
        return f"<ActionFailed " + ", ".join(
            f"{k}={v}" for k, v in self.info.items()) + ">"

    def __str__(self):
        return self.__repr__()


class NetworkError(BaseNetworkError, MiraiAdapterException):

    def __init__(self, msg: Optional[str] = None):
        super().__init__()
        self.msg = msg

    def __repr__(self):
        return f"<NetWorkError message={self.msg}>"

    def __str__(self):
        return self.__repr__()


class ApiNotAvailable(BaseApiNotAvailable, MiraiAdapterException):
    pass
