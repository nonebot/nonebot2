import abc
import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from typing import TYPE_CHECKING, Any, Set, Dict, Type, Callable, AsyncGenerator

from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.dependencies import Dependent
from nonebot.exception import SkippedException
from nonebot.utils import escape_tag, run_coro_with_catch
from nonebot.internal.params import BotParam, DependParam, DefaultParam
from nonebot.typing import (
    T_DependencyCache,
    T_BotConnectionHook,
    T_BotDisconnectionHook,
)

from .model import Request, Response, WebSocket, HTTPServerSetup, WebSocketServerSetup

if TYPE_CHECKING:
    from nonebot.internal.adapter import Bot, Adapter


BOT_HOOK_PARAMS = [DependParam, BotParam, DefaultParam]


class Driver(abc.ABC):
    """Driver 基类。

    参数:
        env: 包含环境信息的 Env 对象
        config: 包含配置信息的 Config 对象
    """

    _adapters: Dict[str, "Adapter"] = {}
    """已注册的适配器列表"""
    _bot_connection_hook: Set[Dependent[Any]] = set()
    """Bot 连接建立时执行的函数"""
    _bot_disconnection_hook: Set[Dependent[Any]] = set()
    """Bot 连接断开时执行的函数"""

    def __init__(self, env: Env, config: Config):
        self.env: str = env.environment
        """环境名称"""
        self.config: Config = config
        """全局配置对象"""
        self._bots: Dict[str, "Bot"] = {}

    def __repr__(self) -> str:
        return (
            f"Driver(type={self.type!r}, "
            f"adapters={len(self._adapters)}, bots={len(self._bots)})"
        )

    @property
    def bots(self) -> Dict[str, "Bot"]:
        """获取当前所有已连接的 Bot"""
        return self._bots

    def register_adapter(self, adapter: Type["Adapter"], **kwargs) -> None:
        """注册一个协议适配器

        参数:
            adapter: 适配器类
            kwargs: 其他传递给适配器的参数
        """
        name = adapter.get_name()
        if name in self._adapters:
            logger.opt(colors=True).debug(
                f'Adapter "<y>{escape_tag(name)}</y>" already exists'
            )
            return
        self._adapters[name] = adapter(self, **kwargs)
        logger.opt(colors=True).debug(
            f'Succeeded to load adapter "<y>{escape_tag(name)}</y>"'
        )

    @property
    @abc.abstractmethod
    def type(self) -> str:
        """驱动类型名称"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def logger(self):
        """驱动专属 logger 日志记录器"""
        raise NotImplementedError

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        """启动驱动框架"""
        logger.opt(colors=True).debug(
            f"<g>Loaded adapters: {escape_tag(', '.join(self._adapters))}</g>"
        )

    @abc.abstractmethod
    def on_startup(self, func: Callable) -> Callable:
        """注册一个在驱动器启动时执行的函数"""
        raise NotImplementedError

    @abc.abstractmethod
    def on_shutdown(self, func: Callable) -> Callable:
        """注册一个在驱动器停止时执行的函数"""
        raise NotImplementedError

    @classmethod
    def on_bot_connect(cls, func: T_BotConnectionHook) -> T_BotConnectionHook:
        """装饰一个函数使他在 bot 连接成功时执行。

        钩子函数参数:

        - bot: 当前连接上的 Bot 对象
        """
        cls._bot_connection_hook.add(
            Dependent[Any].parse(call=func, allow_types=BOT_HOOK_PARAMS)
        )
        return func

    @classmethod
    def on_bot_disconnect(cls, func: T_BotDisconnectionHook) -> T_BotDisconnectionHook:
        """装饰一个函数使他在 bot 连接断开时执行。

        钩子函数参数:

        - bot: 当前连接上的 Bot 对象
        """
        cls._bot_disconnection_hook.add(
            Dependent[Any].parse(call=func, allow_types=BOT_HOOK_PARAMS)
        )
        return func

    def _bot_connect(self, bot: "Bot") -> None:
        """在连接成功后，调用该函数来注册 bot 对象"""
        if bot.self_id in self._bots:
            raise RuntimeError(f"Duplicate bot connection with id {bot.self_id}")
        self._bots[bot.self_id] = bot

        async def _run_hook(bot: "Bot") -> None:
            dependency_cache: T_DependencyCache = {}
            async with AsyncExitStack() as stack:
                if coros := [
                    run_coro_with_catch(
                        hook(bot=bot, stack=stack, dependency_cache=dependency_cache),
                        (SkippedException,),
                    )
                    for hook in self._bot_connection_hook
                ]:
                    try:
                        await asyncio.gather(*coros)
                    except Exception as e:
                        logger.opt(colors=True, exception=e).error(
                            "<r><bg #f8bbd0>"
                            "Error when running WebSocketConnection hook. "
                            "Running cancelled!"
                            "</bg #f8bbd0></r>"
                        )

        asyncio.create_task(_run_hook(bot))

    def _bot_disconnect(self, bot: "Bot") -> None:
        """在连接断开后，调用该函数来注销 bot 对象"""
        if bot.self_id in self._bots:
            del self._bots[bot.self_id]

        async def _run_hook(bot: "Bot") -> None:
            dependency_cache: T_DependencyCache = {}
            async with AsyncExitStack() as stack:
                if coros := [
                    run_coro_with_catch(
                        hook(bot=bot, stack=stack, dependency_cache=dependency_cache),
                        (SkippedException,),
                    )
                    for hook in self._bot_disconnection_hook
                ]:
                    try:
                        await asyncio.gather(*coros)
                    except Exception as e:
                        logger.opt(colors=True, exception=e).error(
                            "<r><bg #f8bbd0>"
                            "Error when running WebSocketDisConnection hook. "
                            "Running cancelled!"
                            "</bg #f8bbd0></r>"
                        )

        asyncio.create_task(_run_hook(bot))


class ForwardMixin(abc.ABC):
    """客户端混入基类。"""

    @property
    @abc.abstractmethod
    def type(self) -> str:
        """客户端驱动类型名称"""
        raise NotImplementedError

    @abc.abstractmethod
    async def request(self, setup: Request) -> Response:
        """发送一个 HTTP 请求"""
        raise NotImplementedError

    @abc.abstractmethod
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator[WebSocket, None]:
        """发起一个 WebSocket 连接"""
        raise NotImplementedError
        yield  # used for static type checking's generator detection


class ForwardDriver(Driver, ForwardMixin):
    """客户端基类。将客户端框架封装，以满足适配器使用。"""


class ReverseDriver(Driver):
    """服务端基类。将后端框架封装，以满足适配器使用。"""

    @property
    @abc.abstractmethod
    def server_app(self) -> Any:
        """驱动 APP 对象"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def asgi(self) -> Any:
        """驱动 ASGI 对象"""
        raise NotImplementedError

    @abc.abstractmethod
    def setup_http_server(self, setup: "HTTPServerSetup") -> None:
        """设置一个 HTTP 服务器路由配置"""
        raise NotImplementedError

    @abc.abstractmethod
    def setup_websocket_server(self, setup: "WebSocketServerSetup") -> None:
        """设置一个 WebSocket 服务器路由配置"""
        raise NotImplementedError


def combine_driver(driver: Type[Driver], *mixins: Type[ForwardMixin]) -> Type[Driver]:
    """将一个驱动器和多个混入类合并。"""
    # check first
    assert issubclass(driver, Driver), "`driver` must be subclass of Driver"
    assert all(
        issubclass(m, ForwardMixin) for m in mixins
    ), "`mixins` must be subclass of ForwardMixin"

    if not mixins:
        return driver

    def type_(self: ForwardDriver) -> str:
        return (
            driver.type.__get__(self)
            + "+"
            + "+".join(x.type.__get__(self) for x in mixins)
        )

    return type(
        "CombinedDriver", (*mixins, driver, ForwardDriver), {"type": property(type_)}
    )  # type: ignore
