import abc
from collections.abc import AsyncGenerator
from contextlib import AsyncExitStack, asynccontextmanager
from types import TracebackType
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union
from typing_extensions import Self, TypeAlias

from anyio import CancelScope, create_task_group
from anyio.abc import TaskGroup
from exceptiongroup import BaseExceptionGroup, catch

from nonebot.config import Config, Env
from nonebot.dependencies import Dependent
from nonebot.exception import SkippedException
from nonebot.internal.params import BotParam, DefaultParam, DependParam
from nonebot.log import logger
from nonebot.typing import (
    T_BotConnectionHook,
    T_BotDisconnectionHook,
    T_DependencyCache,
)
from nonebot.utils import escape_tag, flatten_exception_group, run_coro_with_catch

from ._lifespan import LIFESPAN_FUNC, Lifespan
from .model import (
    CookieTypes,
    HeaderTypes,
    HTTPServerSetup,
    HTTPVersion,
    QueryTypes,
    Request,
    Response,
    TimeoutTypes,
    WebSocket,
    WebSocketServerSetup,
)

if TYPE_CHECKING:
    from nonebot.internal.adapter import Adapter, Bot


BOT_HOOK_PARAMS = [DependParam, BotParam, DefaultParam]


class Driver(abc.ABC):
    """驱动器基类。

    驱动器控制框架的启动和停止，适配器的注册，以及机器人生命周期管理。

    参数:
        env: 包含环境信息的 Env 对象
        config: 包含配置信息的 Config 对象
    """

    _adapters: ClassVar[dict[str, "Adapter"]] = {}
    """已注册的适配器列表"""
    _bot_connection_hook: ClassVar[set[Dependent[Any]]] = set()
    """Bot 连接建立时执行的函数"""
    _bot_disconnection_hook: ClassVar[set[Dependent[Any]]] = set()
    """Bot 连接断开时执行的函数"""

    def __init__(self, env: Env, config: Config):
        self.env: str = env.environment
        """环境名称"""
        self.config: Config = config
        """全局配置对象"""
        self._bots: dict[str, "Bot"] = {}
        self._lifespan = Lifespan()

    def __repr__(self) -> str:
        return (
            f"Driver(type={self.type!r}, "
            f"adapters={len(self._adapters)}, bots={len(self._bots)})"
        )

    @property
    def bots(self) -> dict[str, "Bot"]:
        """获取当前所有已连接的 Bot"""
        return self._bots

    @property
    def task_group(self) -> TaskGroup:
        return self._lifespan.task_group

    def register_adapter(self, adapter: type["Adapter"], **kwargs) -> None:
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
        logger.opt(colors=True).success(
            f"<g>Loaded adapters: {escape_tag(', '.join(self._adapters))}</g>"
        )

    def on_startup(self, func: LIFESPAN_FUNC) -> LIFESPAN_FUNC:
        """注册一个启动时执行的函数"""
        return self._lifespan.on_startup(func)

    def on_shutdown(self, func: LIFESPAN_FUNC) -> LIFESPAN_FUNC:
        """注册一个停止时执行的函数"""
        return self._lifespan.on_shutdown(func)

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

        if not self._bot_connection_hook:
            return

        def handle_exception(exc_group: BaseExceptionGroup) -> None:
            for exc in flatten_exception_group(exc_group):
                logger.opt(colors=True, exception=exc).error(
                    "<r><bg #f8bbd0>"
                    "Error when running WebSocketConnection hook:"
                    "</bg #f8bbd0></r>"
                )

        async def _run_hook(bot: "Bot") -> None:
            dependency_cache: T_DependencyCache = {}
            with CancelScope(shield=True), catch({Exception: handle_exception}):
                async with AsyncExitStack() as stack, create_task_group() as tg:
                    for hook in self._bot_connection_hook:
                        tg.start_soon(
                            run_coro_with_catch,
                            hook(
                                bot=bot, stack=stack, dependency_cache=dependency_cache
                            ),
                            (SkippedException,),
                        )

        self.task_group.start_soon(_run_hook, bot)

    def _bot_disconnect(self, bot: "Bot") -> None:
        """在连接断开后，调用该函数来注销 bot 对象"""
        if bot.self_id in self._bots:
            del self._bots[bot.self_id]

        if not self._bot_disconnection_hook:
            return

        def handle_exception(exc_group: BaseExceptionGroup) -> None:
            for exc in flatten_exception_group(exc_group):
                logger.opt(colors=True, exception=exc).error(
                    "<r><bg #f8bbd0>"
                    "Error when running WebSocketDisConnection hook:"
                    "</bg #f8bbd0></r>"
                )

        async def _run_hook(bot: "Bot") -> None:
            dependency_cache: T_DependencyCache = {}
            # shield cancellation to ensure bot disconnect hooks are always run
            with CancelScope(shield=True), catch({Exception: handle_exception}):
                async with create_task_group() as tg, AsyncExitStack() as stack:
                    for hook in self._bot_disconnection_hook:
                        tg.start_soon(
                            run_coro_with_catch,
                            hook(
                                bot=bot, stack=stack, dependency_cache=dependency_cache
                            ),
                            (SkippedException,),
                        )

        self.task_group.start_soon(_run_hook, bot)


class Mixin(abc.ABC):
    """可与其他驱动器共用的混入基类。"""

    @property
    @abc.abstractmethod
    def type(self) -> str:
        """混入驱动类型名称"""
        raise NotImplementedError


class ForwardMixin(Mixin):
    """客户端混入基类。"""


class ReverseMixin(Mixin):
    """服务端混入基类。"""


class HTTPClientSession(abc.ABC):
    """HTTP 客户端会话基类。"""

    @abc.abstractmethod
    def __init__(
        self,
        params: QueryTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        version: Union[str, HTTPVersion] = HTTPVersion.H11,
        timeout: TimeoutTypes = None,
        proxy: Optional[str] = None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def request(self, setup: Request) -> Response:
        """发送一个 HTTP 请求"""
        raise NotImplementedError

    @abc.abstractmethod
    async def stream_request(
        self,
        setup: Request,
        *,
        chunk_size: int = 1024,
    ) -> AsyncGenerator[Response, None]:
        """发送一个 HTTP 流式请求"""
        raise NotImplementedError
        yield  # used for static type checking's generator detection

    @abc.abstractmethod
    async def setup(self) -> None:
        """初始化会话"""
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self) -> None:
        """关闭会话"""
        raise NotImplementedError

    async def __aenter__(self) -> Self:
        await self.setup()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.close()


class HTTPClientMixin(ForwardMixin):
    """HTTP 客户端混入基类。"""

    @abc.abstractmethod
    async def request(self, setup: Request) -> Response:
        """发送一个 HTTP 请求"""
        raise NotImplementedError

    @abc.abstractmethod
    async def stream_request(
        self,
        setup: Request,
        *,
        chunk_size: int = 1024,
    ) -> AsyncGenerator[Response, None]:
        """发送一个 HTTP 流式请求"""
        raise NotImplementedError
        yield  # used for static type checking's generator detection

    @abc.abstractmethod
    def get_session(
        self,
        params: QueryTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        version: Union[str, HTTPVersion] = HTTPVersion.H11,
        timeout: TimeoutTypes = None,
        proxy: Optional[str] = None,
    ) -> HTTPClientSession:
        """获取一个 HTTP 会话"""
        raise NotImplementedError


class WebSocketClientMixin(ForwardMixin):
    """WebSocket 客户端混入基类。"""

    @abc.abstractmethod
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator[WebSocket, None]:
        """发起一个 WebSocket 连接"""
        raise NotImplementedError
        yield  # used for static type checking's generator detection


class ASGIMixin(ReverseMixin):
    """ASGI 服务端基类。

    将后端框架封装，以满足适配器使用。
    """

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


ForwardDriver: TypeAlias = ForwardMixin
"""支持客户端请求的驱动器。

**Deprecated**，请使用 {ref}`nonebot.drivers.ForwardMixin` 或其子类代替。
"""

ReverseDriver: TypeAlias = ReverseMixin
"""支持服务端请求的驱动器。

**Deprecated**，请使用 {ref}`nonebot.drivers.ReverseMixin` 或其子类代替。
"""
