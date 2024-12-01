"""[FastAPI](https://fastapi.tiangolo.com/) 驱动适配

```bash
nb driver install fastapi
# 或者
pip install nonebot2[fastapi]
```

:::tip 提示
本驱动仅支持服务端连接
:::

FrontMatter:
    mdx:
        format: md
    sidebar_position: 1
    description: nonebot.drivers.fastapi 模块
"""

import contextlib
from functools import wraps
import logging
from typing import Any, Optional, Union
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
    from fastapi import FastAPI, Request, UploadFile, status
    from fastapi.responses import Response
    from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState
    import uvicorn
except ModuleNotFoundError as e:  # pragma: no cover
    raise ImportError(
        "Please install FastAPI first to use this driver. "
        "Install with pip: `pip install nonebot2[fastapi]`"
    ) from e


def catch_closed(func):
    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except WebSocketDisconnect as e:
            raise WebSocketClosed(e.code)
        except KeyError:
            raise TypeError("WebSocket received unexpected frame type")

    return decorator


class Config(BaseModel):
    """FastAPI 驱动框架设置，详情参考 FastAPI 文档"""

    fastapi_openapi_url: Optional[str] = None
    """`openapi.json` 地址，默认为 `None` 即关闭"""
    fastapi_docs_url: Optional[str] = None
    """`swagger` 地址，默认为 `None` 即关闭"""
    fastapi_redoc_url: Optional[str] = None
    """`redoc` 地址，默认为 `None` 即关闭"""
    fastapi_include_adapter_schema: bool = True
    """是否包含适配器路由的 schema，默认为 `True`"""
    fastapi_reload: bool = False
    """开启/关闭冷重载"""
    fastapi_reload_dirs: Optional[list[str]] = None
    """重载监控文件夹列表，默认为 uvicorn 默认值"""
    fastapi_reload_delay: float = 0.25
    """重载延迟，默认为 uvicorn 默认值"""
    fastapi_reload_includes: Optional[list[str]] = None
    """要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值"""
    fastapi_reload_excludes: Optional[list[str]] = None
    """不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值"""
    fastapi_extra: dict[str, Any] = {}
    """传递给 `FastAPI` 的其他参数。"""


class Driver(BaseDriver, ASGIMixin):
    """FastAPI 驱动框架。"""

    def __init__(self, env: Env, config: NoneBotConfig):
        super().__init__(env, config)

        self.fastapi_config: Config = type_validate_python(Config, model_dump(config))

        self._server_app = FastAPI(
            lifespan=self._lifespan_manager,
            openapi_url=self.fastapi_config.fastapi_openapi_url,
            docs_url=self.fastapi_config.fastapi_docs_url,
            redoc_url=self.fastapi_config.fastapi_redoc_url,
            **self.fastapi_config.fastapi_extra,
        )

    @property
    @override
    def type(self) -> str:
        """驱动名称: `fastapi`"""
        return "fastapi"

    @property
    @override
    def server_app(self) -> FastAPI:
        """`FastAPI APP` 对象"""
        return self._server_app

    @property
    @override
    def asgi(self) -> FastAPI:
        """`FastAPI APP` 对象"""
        return self._server_app

    @property
    @override
    def logger(self) -> logging.Logger:
        """fastapi 使用的 logger"""
        return logging.getLogger("fastapi")

    @override
    def setup_http_server(self, setup: HTTPServerSetup):
        async def _handle(request: Request) -> Response:
            return await self._handle_http(request, setup)

        self._server_app.add_api_route(
            setup.path.path,
            _handle,
            name=setup.name,
            methods=[setup.method],
            include_in_schema=self.fastapi_config.fastapi_include_adapter_schema,
        )

    @override
    def setup_websocket_server(self, setup: WebSocketServerSetup) -> None:
        async def _handle(websocket: WebSocket) -> None:
            await self._handle_ws(websocket, setup)

        self._server_app.add_api_websocket_route(
            setup.path.path,
            _handle,
            name=setup.name,
        )

    @contextlib.asynccontextmanager
    async def _lifespan_manager(self, app: FastAPI):
        await self._lifespan.startup()
        try:
            yield
        finally:
            await self._lifespan.shutdown()

    @override
    def run(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        *args,
        app: Optional[str] = None,
        **kwargs,
    ):
        """使用 `uvicorn` 启动 FastAPI"""
        super().run(host, port, app=app, **kwargs)
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
            reload=self.fastapi_config.fastapi_reload,
            reload_dirs=self.fastapi_config.fastapi_reload_dirs,
            reload_delay=self.fastapi_config.fastapi_reload_delay,
            reload_includes=self.fastapi_config.fastapi_reload_includes,
            reload_excludes=self.fastapi_config.fastapi_reload_excludes,
            log_config=LOGGING_CONFIG,
            **kwargs,
        )

    async def _handle_http(
        self,
        request: Request,
        setup: HTTPServerSetup,
    ) -> Response:
        json: Any = None
        with contextlib.suppress(Exception):
            json = await request.json()

        data: Optional[dict] = None
        files: Optional[list[tuple[str, FileTypes]]] = None
        with contextlib.suppress(Exception):
            form = await request.form()
            data = {}
            files = []
            for key, value in form.multi_items():
                if isinstance(value, UploadFile):
                    files.append(
                        (key, (value.filename, value.file, value.content_type))
                    )
                else:
                    data[key] = value

        http_request = BaseRequest(
            request.method,
            str(request.url),
            headers=request.headers.items(),
            cookies=request.cookies,
            content=await request.body(),
            data=data,
            json=json,
            files=files,
            version=request.scope["http_version"],
        )

        response = await setup.handle_func(http_request)
        return Response(
            response.content, response.status_code, dict(response.headers.items())
        )

    async def _handle_ws(self, websocket: WebSocket, setup: WebSocketServerSetup):
        request = BaseRequest(
            "GET",
            str(websocket.url),
            headers=websocket.headers.items(),
            cookies=websocket.cookies,
            version=websocket.scope.get("http_version", "1.1"),
        )
        ws = FastAPIWebSocket(
            request=request,
            websocket=websocket,
        )

        await setup.handle_func(ws)


class FastAPIWebSocket(BaseWebSocket):
    """FastAPI WebSocket Wrapper"""

    @override
    def __init__(self, *, request: BaseRequest, websocket: WebSocket):
        super().__init__(request=request)
        self.websocket = websocket

    @property
    @override
    def closed(self) -> bool:
        return (
            self.websocket.client_state == WebSocketState.DISCONNECTED
            or self.websocket.application_state == WebSocketState.DISCONNECTED
        )

    @override
    async def accept(self) -> None:
        await self.websocket.accept()

    @override
    async def close(
        self, code: int = status.WS_1000_NORMAL_CLOSURE, reason: str = ""
    ) -> None:
        await self.websocket.close(code, reason)

    @override
    async def receive(self) -> Union[str, bytes]:
        # assert self.websocket.application_state == WebSocketState.CONNECTED
        msg = await self.websocket.receive()
        if msg["type"] == "websocket.disconnect":
            raise WebSocketClosed(msg["code"])
        return msg["text"] if "text" in msg else msg["bytes"]

    @override
    @catch_closed
    async def receive_text(self) -> str:
        return await self.websocket.receive_text()

    @override
    @catch_closed
    async def receive_bytes(self) -> bytes:
        return await self.websocket.receive_bytes()

    @override
    async def send_text(self, data: str) -> None:
        await self.websocket.send({"type": "websocket.send", "text": data})

    @override
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send({"type": "websocket.send", "bytes": data})


__autodoc__ = {"catch_closed": False}
