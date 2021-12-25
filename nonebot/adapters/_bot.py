import abc
import asyncio
from functools import partial
from typing_extensions import Protocol
from typing import TYPE_CHECKING, Any, Set, Union, Optional

from nonebot.log import logger
from nonebot.config import Config
from nonebot.exception import MockApiException
from nonebot.typing import T_CalledAPIHook, T_CallingAPIHook

if TYPE_CHECKING:
    from ._event import Event
    from ._adapter import Adapter
    from ._message import Message, MessageSegment


class _ApiCall(Protocol):
    async def __call__(self, **kwargs: Any) -> Any:
        ...


class Bot(abc.ABC):
    """
    Bot 基类。用于处理上报消息，并提供 API 调用接口。
    """

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

    def __init__(self, adapter: "Adapter", self_id: str):
        """
        :参数:

          * ``self_id: str``: 机器人 ID
          * ``request: HTTPConnection``: request 连接对象
        """
        self.adapter: "Adapter" = adapter
        self.self_id: str = self_id
        """机器人 ID"""

    def __getattr__(self, name: str) -> _ApiCall:
        return partial(self.call_api, name)

    @property
    def type(self) -> str:
        return self.adapter.get_name()

    @property
    def config(self) -> Config:
        return self.adapter.config

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

        result: Any = None
        skip_calling_api: bool = False
        exception: Optional[Exception] = None

        coros = list(map(lambda x: x(self, api, data), self._calling_api_hook))
        if coros:
            try:
                logger.debug("Running CallingAPI hooks...")
                await asyncio.gather(*coros)
            except MockApiException as e:
                skip_calling_api = True
                result = e.result
                logger.debug(
                    f"Calling API {api} is cancelled. Return {result} instead."
                )
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running CallingAPI hook. "
                    "Running cancelled!</bg #f8bbd0></r>"
                )

        if not skip_calling_api:
            try:
                result = await self.adapter._call_api(self, api, **data)
            except Exception as e:
                exception = e

        coros = list(
            map(lambda x: x(self, exception, api, data, result), self._called_api_hook)
        )
        if coros:
            try:
                logger.debug("Running CalledAPI hooks...")
                await asyncio.gather(*coros)
            except MockApiException as e:
                result = e.result
                logger.debug(
                    f"Calling API {api} result is mocked. Return {result} instead."
                )
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running CalledAPI hook. "
                    "Running cancelled!</bg #f8bbd0></r>"
                )

        if exception:
            raise exception
        return result

    @abc.abstractmethod
    async def send(
        self, event: "Event", message: Union[str, "Message", "MessageSegment"], **kwargs
    ) -> Any:
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
