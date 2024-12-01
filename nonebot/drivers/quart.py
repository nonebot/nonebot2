"""[Quart](https://pgjones.gitlab.io/quart/index.html) 驱动适配

```bash
nb driver install quart
# 或者
pip install nonebot2[quart]
```

:::tip 提示
本驱动仅支持服务端连接
:::

FrontMatter:
    mdx:
        format: md
    sidebar_position: 5
    description: nonebot.drivers.quart 模块
"""

import asyncio
from functools import wraps
from typing import Any, Optional, Union, cast
from typing_extensions import override

from pydantic import BaseModel

from nonebot.compat import model_dump, type_validate_python
from nonebot.config import Config as NoneBotConfig
from nonebot.config import Env
from nonebot.drivers import ASGIMixin, HTTPServerSetup, WebSocketServerSetup
from nonebot.drivers import Driver as BaseDriver
from nonebot.drivers import Request as BaseRequest
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.exception import WebSocketClosed
from nonebot.internal.driver import FileTypes

try:
    from quart import Quart, Request, Response
    from quart import Websocket as QuartWebSocket
    from quart import request as _request
    from quart.ctx import WebsocketContext
    from quart.datastructures import FileStorage
    from quart.globals import websocket_ctx
    import uvicorn
except ModuleNotFoundError as e:  # pragma: no cover
    raise ImportError(
        "Please install Quart first to use this driver. "
        "Install with pip: `pip install nonebot2[quart]`"
    ) from e


def catch_closed(func):
    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except asyncio.CancelledError:
            raise WebSocketClosed(1000)

    return decorator


class Config(BaseModel):
    """Quart 驱动框架设置"""

    quart_reload: bool = False
    """开启/关闭冷重载"""
    quart_reload_dirs: Optional[list[str]] = None
    """重载监控文件夹列表，默认为 uvicorn 默认值"""
    quart_reload_delay: float = 0.25
    """重载延迟，默认为 uvicorn 默认值"""
    quart_reload_includes: Optional[list[str]] = None
    """要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值"""
    quart_reload_excludes: Optional[list[str]] = None
    """不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值"""
    quart_extra: dict[str, Any] = {}
    """传递给 `Quart` 的其他参数。"""


class Driver(BaseDriver, ASGIMixin):
    """Quart 驱动框架"""

    def __init__(self, env: Env, config: NoneBotConfig):
        super().__init__(env, config)

        self.quart_config = type_validate_python(Config, model_dump(config))

        self._server_app = Quart(
            self.__class__.__qualname__, **self.quart_config.quart_extra
        )
        self._server_app.before_serving(self._lifespan.startup)
        self._server_app.after_serving(self._lifespan.shutdown)

    @property
    @override
    def type(self) -> str:
        """驱动名称: `quart`"""
        return "quart"

    @property
    @override
    def server_app(self) -> Quart:
        """`Quart` 对象"""
        return self._server_app

    @property
    @override
    def asgi(self):
        """`Quart` 对象"""
        return self._server_app

    @property
    @override
    def logger(self):
        """Quart 使用的 logger"""
        return self._server_app.logger

    @override
    def setup_http_server(self, setup: HTTPServerSetup):
        async def _handle() -> Response:
            return await self._handle_http(setup)

        self._server_app.add_url_rule(
            setup.path.path,
            endpoint=setup.name,
            methods=[setup.method],
            view_func=_handle,
        )

    @override
    def setup_websocket_server(self, setup: WebSocketServerSetup) -> None:
        async def _handle() -> None:
            return await self._handle_ws(setup)

        self._server_app.add_websocket(
            setup.path.path,
            endpoint=setup.name,
            view_func=_handle,
        )

    @override
    def run(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        *args,
        app: Optional[str] = None,
        **kwargs,
    ):
        """使用 `uvicorn` 启动 Quart"""
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

        json = await request.get_json() if request.is_json else None

        data = await request.form
        files_dict = await request.files
        files: list[tuple[str, FileTypes]] = []
        key: str
        value: FileStorage
        for key, value in files_dict.items():
            files.append((key, (value.filename, value.stream, value.content_type)))

        http_request = BaseRequest(
            request.method,
            request.url,
            headers=list(request.headers.items()),
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
        ctx = cast(WebsocketContext, websocket_ctx.copy())
        websocket = websocket_ctx.websocket

        http_request = BaseRequest(
            websocket.method,
            websocket.url,
            headers=list(websocket.headers.items()),
            cookies=list(websocket.cookies.items()),
            version=websocket.http_version,
        )

        ws = WebSocket(request=http_request, websocket_ctx=ctx)

        await setup.handle_func(ws)


class WebSocket(BaseWebSocket):
    """Quart WebSocket Wrapper"""

    def __init__(self, *, request: BaseRequest, websocket_ctx: WebsocketContext):
        super().__init__(request=request)
        self.websocket_ctx = websocket_ctx

    @property
    def websocket(self) -> QuartWebSocket:
        return self.websocket_ctx.websocket

    @property
    @override
    def closed(self):
        # FIXME
        return True

    @override
    async def accept(self):
        await self.websocket.accept()

    @override
    async def close(self, code: int = 1000, reason: str = ""):
        await self.websocket.close(code, reason)

    @override
    @catch_closed
    async def receive(self) -> Union[str, bytes]:
        return await self.websocket.receive()

    @override
    @catch_closed
    async def receive_text(self) -> str:
        msg = await self.websocket.receive()
        if isinstance(msg, bytes):
            raise TypeError("WebSocket received unexpected frame type: bytes")
        return msg

    @override
    @catch_closed
    async def receive_bytes(self) -> bytes:
        msg = await self.websocket.receive()
        if isinstance(msg, str):
            raise TypeError("WebSocket received unexpected frame type: str")
        return msg

    @override
    async def send_text(self, data: str):
        await self.websocket.send(data)

    @override
    async def send_bytes(self, data: bytes):
        await self.websocket.send(data)


__autodoc__ = {"catch_closed": False}
