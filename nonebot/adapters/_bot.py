import abc
import asyncio
from functools import partial
from typing_extensions import Protocol
from typing import TYPE_CHECKING, Any, Set, Tuple, Union, Optional

from nonebot.log import logger
from nonebot.config import Config
from nonebot.typing import T_CalledAPIHook, T_CallingAPIHook
from nonebot.drivers import Driver, HTTPResponse, HTTPConnection

if TYPE_CHECKING:
    from ._event import Event
    from ._message import Message, MessageSegment


class _ApiCall(Protocol):

    async def __call__(self, **kwargs: Any) -> Any:
        ...


class Bot(abc.ABC):
    """
    Bot 基类。用于处理上报消息，并提供 API 调用接口。
    """

    driver: Driver
    """Driver 对象"""
    config: Config
    """Config 配置对象"""
    _calling_api_hook: Set[T_CallingAPIHook] = set()
    """
    :类型: ``Set[T_CallingAPIHook]``
    :说明: call_api 时执行的函数
    """
    _called_api_hook: Set[T_CalledAPIHook] = set()
    """
    :类型: ``Set[T_CalledAPIHook]``
    :说明: call_api 后执行的函数
    """

    def __init__(self, self_id: str, request: HTTPConnection):
        """
        :参数:

          * ``self_id: str``: 机器人 ID
          * ``request: HTTPConnection``: request 连接对象
        """
        self.self_id: str = self_id
        """机器人 ID"""
        self.request: HTTPConnection = request
        """连接信息"""

    def __getattr__(self, name: str) -> _ApiCall:
        return partial(self.call_api, name)

    @property
    @abc.abstractmethod
    def type(self) -> str:
        """Adapter 类型"""
        raise NotImplementedError

    @classmethod
    def register(cls, driver: Driver, config: Config, **kwargs):
        """
        :说明:

          ``register`` 方法会在 ``driver.register_adapter`` 时被调用，用于初始化相关配置
        """
        cls.driver = driver
        cls.config = config

    @classmethod
    @abc.abstractmethod
    async def check_permission(
        cls, driver: Driver, request: HTTPConnection
    ) -> Tuple[Optional[str], Optional[HTTPResponse]]:
        """
        :说明:

          检查连接请求是否合法的函数，如果合法则返回当前连接 ``唯一标识符``，通常为机器人 ID；如果不合法则抛出 ``RequestDenied`` 异常。

        :参数:

          * ``driver: Driver``: Driver 对象
          * ``request: HTTPConnection``: request 请求详情

        :返回:

          - ``Optional[str]``: 连接唯一标识符，``None`` 代表连接不合法
          - ``Optional[HTTPResponse]``: HTTP 上报响应
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def handle_message(self, message: bytes):
        """
        :说明:

          处理上报消息的函数，转换为 ``Event`` 事件后调用 ``nonebot.message.handle_event`` 进一步处理事件。

        :参数:

          * ``message: bytes``: 收到的上报消息
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def _call_api(self, api: str, **data) -> Any:
        """
        :说明:

          ``adapter`` 实际调用 api 的逻辑实现函数，实现该方法以调用 api。

        :参数:

          * ``api: str``: API 名称
          * ``**data``: API 数据
        """
        raise NotImplementedError

    async def call_api(self, api: str, **data: Any) -> Any:
        """
        :说明:

          调用机器人 API 接口，可以通过该函数或直接通过 bot 属性进行调用

        :参数:

          * ``api: str``: API 名称
          * ``**data``: API 数据

        :示例:

        .. code-block:: python

            await bot.call_api("send_msg", message="hello world")
            await bot.send_msg(message="hello world")
        """
        coros = list(map(lambda x: x(self, api, data), self._calling_api_hook))
        if coros:
            try:
                logger.debug("Running CallingAPI hooks...")
                await asyncio.gather(*coros)
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running CallingAPI hook. "
                    "Running cancelled!</bg #f8bbd0></r>")

        exception = None
        result = None

        try:
            result = await self._call_api(api, **data)
        except Exception as e:
            exception = e

        coros = list(
            map(lambda x: x(self, exception, api, data, result),
                self._called_api_hook))
        if coros:
            try:
                logger.debug("Running CalledAPI hooks...")
                await asyncio.gather(*coros)
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running CalledAPI hook. "
                    "Running cancelled!</bg #f8bbd0></r>")

        if exception:
            raise exception
        return result

    @abc.abstractmethod
    async def send(self, event: "Event", message: Union[str, "Message",
                                                        "MessageSegment"],
                   **kwargs) -> Any:
        """
        :说明:

          调用机器人基础发送消息接口

        :参数:

          * ``event: Event``: 上报事件
          * ``message: Union[str, Message, MessageSegment]``: 要发送的消息
          * ``**kwargs``
        """
        raise NotImplementedError

    @classmethod
    def on_calling_api(cls, func: T_CallingAPIHook) -> T_CallingAPIHook:
        """
        :说明:

          调用 api 预处理。

        :参数:

          * ``bot: Bot``: 当前 bot 对象
          * ``api: str``: 调用的 api 名称
          * ``data: Dict[str, Any]``: api 调用的参数字典
        """
        cls._calling_api_hook.add(func)
        return func

    @classmethod
    def on_called_api(cls, func: T_CalledAPIHook) -> T_CalledAPIHook:
        """
        :说明:

          调用 api 后处理。

        :参数:

          * ``bot: Bot``: 当前 bot 对象
          * ``exception: Optional[Exception]``: 调用 api 时发生的错误
          * ``api: str``: 调用的 api 名称
          * ``data: Dict[str, Any]``: api 调用的参数字典
          * ``result: Any``: api 调用的返回
        """
        cls._called_api_hook.add(func)
        return func
