"""
Quart 驱动适配
================

后端使用方法请参考: `Quart 文档`_

.. _Quart 文档:
    https://pgjones.gitlab.io/quart/index.html
"""

import asyncio
from functools import wraps
from typing import List, Tuple, TypeVar, Callable, Optional, Coroutine

import uvicorn
from pydantic import BaseSettings

from ._model import FileTypes
from nonebot.config import Env
from nonebot.typing import overrides
from nonebot.exception import WebSocketClosed
from nonebot.config import Config as NoneBotConfig
from nonebot.drivers import Request as BaseRequest
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers import ReverseDriver, HTTPServerSetup, WebSocketServerSetup

try:
    from quart import request as _request
    from quart import websocket as _websocket
    from quart import Quart, Request, Response
    from quart.datastructures import FileStorage
    from quart import Websocket as QuartWebSocket
except ImportError:
    raise ValueError(
        "Please install Quart by using `pip install nonebot2[quart]`"
    ) from None

_AsyncCallable = TypeVar("_AsyncCallable", bound=Callable[..., Coroutine])


def catch_closed(func):
    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except asyncio.CancelledError:
            raise WebSocketClosed(1000)

    return decorator


class Config(BaseSettings):
    """
    Quart 驱动框架设置
    """

    quart_reload: bool = False
    """
    :类型:

      ``bool``

    :说明:

      开启/关闭冷重载
    """
    quart_reload_dirs: Optional[List[str]] = None
    """
    :类型:

      ``Optional[List[str]]``

    :说明:

      重载监控文件夹列表，默认为 uvicorn 默认值
    """
    quart_reload_delay: Optional[float] = None
    """
    :类型:

      ``Optional[float]``

    :说明:

      重载延迟，默认为 uvicorn 默认值
    """
    quart_reload_includes: Optional[List[str]] = None
    """
    :类型:

      ``Optional[List[str]]``

    :说明:

      要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值
    """
    quart_reload_excludes: Optional[List[str]] = None
    """
    :类型:

      ``Optional[List[str]]``

    :说明:

      不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值
    """

    class Config:
        extra = "ignore"


class Driver(ReverseDriver):
    """
    Quart 驱动框架
    """

    def __init__(self, env: Env, config: NoneBotConfig):
        super().__init__(env, config)

        self.quart_config = Config(**config.dict())

        self._server_app = Quart(self.__class__.__qualname__)

    @property
    @overrides(ReverseDriver)
    def type(self) -> str:
        """驱动名称: ``quart``"""
        return "quart"

    @property
    @overrides(ReverseDriver)
    def server_app(self) -> Quart:
        """``Quart`` 对象"""
        return self._server_app

    @property
    @overrides(ReverseDriver)
    def asgi(self):
        """``Quart`` 对象"""
        return self._server_app

    @property
    @overrides(ReverseDriver)
    def logger(self):
        """Quart 使用的 logger"""
        return self._server_app.logger

    @overrides(ReverseDriver)
    def setup_http_server(self, setup: HTTPServerSetup):
        async def _handle() -> Response:
            return await self._handle_http(setup)

        self._server_app.add_url_rule(
            setup.path.path,
            endpoint=setup.name,
            methods=[setup.method],
            view_func=_handle,
        )

    @overrides(ReverseDriver)
    def setup_websocket_server(self, setup: WebSocketServerSetup) -> None:
        async def _handle() -> None:
            return await self._handle_ws(setup)

        self._server_app.add_websocket(
            setup.path.path,
            endpoint=setup.name,
            view_func=_handle,
        )

    @overrides(ReverseDriver)
    def on_startup(self, func: _AsyncCallable) -> _AsyncCallable:
        """参考文档: `Startup and Shutdown`_

        .. _Startup and Shutdown:
            https://pgjones.gitlab.io/quart/how_to_guides/startup_shutdown.html
        """
        return self.server_app.before_serving(func)  # type: ignore

    @overrides(ReverseDriver)
    def on_shutdown(self, func: _AsyncCallable) -> _AsyncCallable:
        """参考文档: `Startup and Shutdown`_"""
        return self.server_app.after_serving(func)  # type: ignore

    @overrides(ReverseDriver)
    def run(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        *,
        app: Optional[str] = None,
        **kwargs,
    ):
        """使用 ``uvicorn`` 启动 Quart"""
        super().run(host, port, app, **kwargs)
        LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "default": {
                    "class": "nonebot.log.LoguruHandler",
                },
            },
            "loggers": {
                "uvicorn.error": {"handlers": ["default"], "level": "INFO"},
                "uvicorn.access": {
                    "handlers": ["default"],
                    "level": "INFO",
                },
            },
        }
        uvicorn.run(
            app or self.server_app,  # type: ignore
            host=host or str(self.config.host),
            port=port or self.config.port,
            reload=self.quart_config.quart_reload,
            reload_dirs=self.quart_config.quart_reload_dirs,
            reload_delay=self.quart_config.quart_reload_delay,
            reload_includes=self.quart_config.quart_reload_includes,
            reload_excludes=self.quart_config.quart_reload_excludes,
            log_config=LOGGING_CONFIG,
            **kwargs,
        )

    async def _handle_http(self, setup: HTTPServerSetup) -> Response:
        request: Request = _request

        json = None
        if request.is_json:
            json = await request.get_json()

        data = await request.form
        files_dict = await request.files
        files: List[Tuple[str, FileTypes]] = []
        key: str
        value: FileStorage
        for key, value in files_dict.items():
            files.append((key, (value.filename, value.stream, value.content_type)))

        http_request = BaseRequest(
            request.method,
            request.url,
            headers=request.headers.items(),
            cookies=list(request.cookies.items()),
            content=await request.get_data(
                cache=False, as_text=False, parse_form_data=False
            ),
            data=data or None,
            json=json,
            files=files or None,
            version=request.http_version,
        )

        response = await setup.handle_func(http_request)

        return Response(
            response.content or "",
            response.status_code or 200,
            headers=dict(response.headers),
        )

    async def _handle_ws(self, setup: WebSocketServerSetup) -> None:
        websocket: QuartWebSocket = _websocket

        http_request = BaseRequest(
            websocket.method,
            websocket.url,
            headers=websocket.headers.items(),
            cookies=list(websocket.cookies.items()),
            version=websocket.http_version,
        )

        ws = WebSocket(request=http_request, websocket=websocket)

        await setup.handle_func(ws)


class WebSocket(BaseWebSocket):
    def __init__(self, *, request: BaseRequest, websocket: QuartWebSocket):
        super().__init__(request=request)
        self.websocket = websocket

    @property
    @overrides(BaseWebSocket)
    def closed(self):
        # FIXME
        return True

    @overrides(BaseWebSocket)
    async def accept(self):
        await self.websocket.accept()

    @overrides(BaseWebSocket)
    async def close(self, code: int = 1000, reason: str = ""):
        await self.websocket.close(code, reason)

    @overrides(BaseWebSocket)
    @catch_closed
    async def receive(self) -> str:
        msg = await self.websocket.receive()
        if isinstance(msg, bytes):
            raise TypeError("WebSocket received unexpected frame type: bytes")
        return msg

    @overrides(BaseWebSocket)
    @catch_closed
    async def receive_bytes(self) -> bytes:
        msg = await self.websocket.receive()
        if isinstance(msg, str):
            raise TypeError("WebSocket received unexpected frame type: str")
        return msg

    @overrides(BaseWebSocket)
    async def send(self, data: str):
        await self.websocket.send(data)

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes):
        await self.websocket.send(data)
