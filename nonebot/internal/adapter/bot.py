import abc
import asyncio
from functools import partial
from typing import TYPE_CHECKING, Any, Set, Union, Optional, Protocol

from nonebot.log import logger
from nonebot.config import Config
from nonebot.exception import MockApiException
from nonebot.typing import T_CalledAPIHook, T_CallingAPIHook

if TYPE_CHECKING:
    from .event import Event
    from .adapter import Adapter
    from .message import Message, MessageSegment

    class _ApiCall(Protocol):
        async def __call__(self, **kwargs: Any) -> Any:
            ...


class Bot(abc.ABC):
    """Bot 基类。

    用于处理上报消息，并提供 API 调用接口。

    参数:
        adapter: 协议适配器实例
        self_id: 机器人 ID
    """

    _calling_api_hook: Set[T_CallingAPIHook] = set()
    """call_api 时执行的函数"""
    _called_api_hook: Set[T_CalledAPIHook] = set()
    """call_api 后执行的函数"""

    def __init__(self, adapter: "Adapter", self_id: str):
        self.adapter: "Adapter" = adapter
        """协议适配器实例"""
        self.self_id: str = self_id
        """机器人 ID"""

    def __repr__(self) -> str:
        return f"Bot(type={self.type!r}, self_id={self.self_id!r})"

    def __getattr__(self, name: str) -> "_ApiCall":
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
        return partial(self.call_api, name)

    @property
    def type(self) -> str:
        """协议适配器名称"""
        return self.adapter.get_name()

    @property
    def config(self) -> Config:
        """全局 NoneBot 配置"""
        return self.adapter.config

    async def call_api(self, api: str, **data: Any) -> Any:
        """调用机器人 API 接口，可以通过该函数或直接通过 bot 属性进行调用

        参数:
            api: API 名称
            data: API 数据

        用法:
            ```python
            await bot.call_api("send_msg", message="hello world")
            await bot.send_msg(message="hello world")
            ```
        """

        result: Any = None
        skip_calling_api: bool = False
        exception: Optional[Exception] = None

        if coros := [hook(self, api, data) for hook in self._calling_api_hook]:
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

        if coros := [
            hook(self, exception, api, data, result) for hook in self._called_api_hook
        ]:
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
        self,
        event: "Event",
        message: Union[str, "Message", "MessageSegment"],
        **kwargs: Any,
    ) -> Any:
        """调用机器人基础发送消息接口

        参数:
            event: 上报事件
            message: 要发送的消息
            kwargs: 任意额外参数
        """
        raise NotImplementedError

    @classmethod
    def on_calling_api(cls, func: T_CallingAPIHook) -> T_CallingAPIHook:
        """调用 api 预处理。

        钩子函数参数:

        - bot: 当前 bot 对象
        - api: 调用的 api 名称
        - data: api 调用的参数字典
        """
        cls._calling_api_hook.add(func)
        return func

    @classmethod
    def on_called_api(cls, func: T_CalledAPIHook) -> T_CalledAPIHook:
        """调用 api 后处理。

        钩子函数参数:

        - bot: 当前 bot 对象
        - exception: 调用 api 时发生的错误
        - api: 调用的 api 名称
        - data: api 调用的参数字典
        - result: api 调用的返回
        """
        cls._called_api_hook.add(func)
        return func
