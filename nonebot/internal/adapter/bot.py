import abc
from functools import partial
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Protocol, Union

import anyio
from exceptiongroup import BaseExceptionGroup, catch

from nonebot.config import Config
from nonebot.exception import MockApiException
from nonebot.log import logger
from nonebot.typing import T_CalledAPIHook, T_CallingAPIHook
from nonebot.utils import flatten_exception_group

if TYPE_CHECKING:
    from .adapter import Adapter
    from .event import Event
    from .message import Message, MessageSegment

    class _ApiCall(Protocol):
        async def __call__(self, **kwargs: Any) -> Any: ...


class Bot(abc.ABC):
    """Bot 基类。

    用于处理上报消息，并提供 API 调用接口。

    参数:
        adapter: 协议适配器实例
        self_id: 机器人 ID
    """

    _calling_api_hook: ClassVar[set[T_CallingAPIHook]] = set()
    """call_api 时执行的函数"""
    _called_api_hook: ClassVar[set[T_CalledAPIHook]] = set()
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

        if self._calling_api_hook:
            logger.debug("Running CallingAPI hooks...")

            def _handle_mock_api_exception(
                exc_group: BaseExceptionGroup[MockApiException],
            ) -> None:
                nonlocal skip_calling_api, result

                excs = [
                    exc
                    for exc in flatten_exception_group(exc_group)
                    if isinstance(exc, MockApiException)
                ]
                if not excs:
                    return
                elif len(excs) > 1:
                    logger.warning(
                        "Multiple hooks want to mock API result. Use the first one."
                    )

                skip_calling_api = True
                result = excs[0].result

                logger.debug(
                    f"Calling API {api} is cancelled. Return {result!r} instead."
                )

            def _handle_exception(exc_group: BaseExceptionGroup[Exception]) -> None:
                for exc in flatten_exception_group(exc_group):
                    logger.opt(colors=True, exception=exc).error(
                        "<r><bg #f8bbd0>Error when running CallingAPI hook. "
                        "Running cancelled!</bg #f8bbd0></r>"
                    )

            with catch(
                {
                    MockApiException: _handle_mock_api_exception,
                    Exception: _handle_exception,
                }
            ):
                async with anyio.create_task_group() as tg:
                    for hook in self._calling_api_hook:
                        tg.start_soon(hook, self, api, data)

        if not skip_calling_api:
            try:
                result = await self.adapter._call_api(self, api, **data)
            except Exception as e:
                exception = e

        if self._called_api_hook:
            logger.debug("Running CalledAPI hooks...")

            def _handle_mock_api_exception(
                exc_group: BaseExceptionGroup[MockApiException],
            ) -> None:
                nonlocal result, exception

                excs = [
                    exc
                    for exc in flatten_exception_group(exc_group)
                    if isinstance(exc, MockApiException)
                ]
                if not excs:
                    return
                elif len(excs) > 1:
                    logger.warning(
                        "Multiple hooks want to mock API result. Use the first one."
                    )

                result = excs[0].result
                exception = None
                logger.debug(
                    f"Calling API {api} result is mocked. Return {result} instead."
                )

            def _handle_exception(exc_group: BaseExceptionGroup[Exception]) -> None:
                for exc in flatten_exception_group(exc_group):
                    logger.opt(colors=True, exception=exc).error(
                        "<r><bg #f8bbd0>Error when running CalledAPI hook. "
                        "Running cancelled!</bg #f8bbd0></r>"
                    )

            with catch(
                {
                    MockApiException: _handle_mock_api_exception,
                    Exception: _handle_exception,
                }
            ):
                async with anyio.create_task_group() as tg:
                    for hook in self._called_api_hook:
                        tg.start_soon(hook, self, exception, api, data, result)

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
