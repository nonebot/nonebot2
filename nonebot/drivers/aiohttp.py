"""
AIOHTTP 驱动适配
================

本驱动仅支持客户端连接
"""

import signal
import asyncio
import threading
from dataclasses import dataclass
from typing import Set, List, cast, Union, Optional, Callable, Awaitable

import aiohttp
from yarl import URL

from nonebot.log import logger
from nonebot.adapters import Bot
from nonebot.typing import overrides
from nonebot.config import Env, Config
from nonebot.drivers import (ForwardDriver, HTTPPollingSetup, WebSocketSetup,
                             HTTPRequest, WebSocket as BaseWebSocket)

STARTUP_FUNC = Callable[[], Awaitable[None]]
SHUTDOWN_FUNC = Callable[[], Awaitable[None]]
HTTPPOLLING_SETUP = Union[HTTPPollingSetup,
                          Callable[[], Awaitable[HTTPPollingSetup]]]
WEBSOCKET_SETUP = Union[WebSocketSetup, Callable[[], Awaitable[WebSocketSetup]]]
HANDLED_SIGNALS = (
    signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
    signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
)


class Driver(ForwardDriver):
    """
    AIOHTTP 驱动框架
    """

    def __init__(self, env: Env, config: Config):
        super().__init__(env, config)
        self.startup_funcs: Set[STARTUP_FUNC] = set()
        self.shutdown_funcs: Set[SHUTDOWN_FUNC] = set()
        self.http_pollings: List[HTTPPOLLING_SETUP] = []
        self.websockets: List[WEBSOCKET_SETUP] = []
        self.connections: List[asyncio.Task] = []
        self.should_exit: asyncio.Event = asyncio.Event()
        self.force_exit: bool = False

    @property
    @overrides(ForwardDriver)
    def type(self) -> str:
        """驱动名称: ``aiohttp``"""
        return "aiohttp"

    @property
    @overrides(ForwardDriver)
    def logger(self):
        """aiohttp driver 使用的 logger"""
        return logger

    @overrides(ForwardDriver)
    def on_startup(self, func: STARTUP_FUNC) -> STARTUP_FUNC:
        """
        :说明:

          注册一个启动时执行的函数

        :参数:

          * ``func: Callable[[], Awaitable[None]]``
        """
        self.startup_funcs.add(func)
        return func

    @overrides(ForwardDriver)
    def on_shutdown(self, func: SHUTDOWN_FUNC) -> SHUTDOWN_FUNC:
        """
        :说明:

          注册一个停止时执行的函数

        :参数:

          * ``func: Callable[[], Awaitable[None]]``
        """
        self.shutdown_funcs.add(func)
        return func

    @overrides(ForwardDriver)
    def setup_http_polling(self, setup: HTTPPOLLING_SETUP) -> None:
        """
        :说明:

          注册一个 HTTP 轮询连接，如果传入一个函数，则该函数会在每次连接时被调用

        :参数:

          * ``setup: Union[HTTPPollingSetup, Callable[[], Awaitable[HTTPPollingSetup]]]``
        """
        self.http_pollings.append(setup)

    @overrides(ForwardDriver)
    def setup_websocket(self, setup: WEBSOCKET_SETUP) -> None:
        """
        :说明:

          注册一个 WebSocket 连接，如果传入一个函数，则该函数会在每次重连时被调用

        :参数:

          * ``setup: Union[WebSocketSetup, Callable[[], Awaitable[WebSocketSetup]]]``
        """
        self.websockets.append(setup)

    @overrides(ForwardDriver)
    def run(self, *args, **kwargs):
        """启动 aiohttp driver"""
        super().run(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.serve())

    async def serve(self):
        self.install_signal_handlers()
        await self.startup()
        if self.should_exit.is_set():
            return
        await self.main_loop()
        await self.shutdown()

    async def startup(self):
        for setup in self.http_pollings:
            self.connections.append(asyncio.create_task(self._http_loop(setup)))
        for setup in self.websockets:
            self.connections.append(asyncio.create_task(self._ws_loop(setup)))

        logger.info("Application startup completed.")

        # run startup
        cors = [startup() for startup in self.startup_funcs]
        if cors:
            try:
                await asyncio.gather(*cors)
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running startup function. "
                    "Ignored!</bg #f8bbd0></r>")

    async def main_loop(self):
        await self.should_exit.wait()

    async def shutdown(self):
        # run shutdown
        cors = [shutdown() for shutdown in self.shutdown_funcs]
        if cors:
            try:
                await asyncio.gather(*cors)
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running shutdown function. "
                    "Ignored!</bg #f8bbd0></r>")

        for task in self.connections:
            if not task.done():
                task.cancel()
        await asyncio.sleep(0.1)

        tasks = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]
        if tasks and not self.force_exit:
            logger.info("Waiting for tasks to finish. (CTRL+C to force quit)")
        while tasks and not self.force_exit:
            await asyncio.sleep(0.1)
            tasks = [
                t for t in asyncio.all_tasks()
                if t is not asyncio.current_task()
            ]

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

        loop = asyncio.get_event_loop()
        loop.stop()

    def install_signal_handlers(self) -> None:
        if threading.current_thread() is not threading.main_thread():
            # Signals can only be listened to from the main thread.
            return

        loop = asyncio.get_event_loop()

        try:
            for sig in HANDLED_SIGNALS:
                loop.add_signal_handler(sig, self.handle_exit, sig, None)
        except NotImplementedError:
            # Windows
            for sig in HANDLED_SIGNALS:
                signal.signal(sig, self.handle_exit)

    def handle_exit(self, sig, frame):
        if self.should_exit.is_set():
            self.force_exit = True
        else:
            self.should_exit.set()

    async def _http_loop(self, setup: HTTPPOLLING_SETUP):

        async def _build_request(
                setup: HTTPPollingSetup) -> Optional[HTTPRequest]:
            url = URL(setup.url)
            if not url.is_absolute() or not url.host:
                logger.opt(colors=True).error(
                    f"<r><bg #f8bbd0>Error parsing url {url}</bg #f8bbd0></r>")
                return
            host = f"{url.host}:{url.port}" if url.port else url.host
            return HTTPRequest(setup.http_version, url.scheme, url.path,
                               url.raw_query_string.encode("latin-1"), {
                                   **setup.headers, "host": host
                               }, setup.method, setup.body)

        bot: Optional[Bot] = None
        request: Optional[HTTPRequest] = None
        setup_: Optional[HTTPPollingSetup] = None

        logger.opt(colors=True).info(
            f"Start http polling for <y>{setup.adapter.upper()} "
            f"Bot {setup.self_id}</y>")

        try:
            async with aiohttp.ClientSession() as session:
                while not self.should_exit.is_set():
                    if not bot:
                        if callable(setup):
                            setup_ = await setup()
                        else:
                            setup_ = setup
                        request = await _build_request(setup_)
                        if not request:
                            return

                        BotClass = self._adapters[setup.adapter]
                        bot = BotClass(setup.self_id, request)
                        self._bot_connect(bot)
                    elif callable(setup):
                        setup_ = await setup()
                        request = await _build_request(setup_)
                        if not request:
                            await asyncio.sleep(setup_.poll_interval)
                            continue
                        bot.request = request

                    request = cast(HTTPRequest, request)
                    setup_ = cast(HTTPPollingSetup, setup_)

                    headers = request.headers
                    timeout = aiohttp.ClientTimeout(30)
                    version: aiohttp.HttpVersion
                    if request.http_version == "1.0":
                        version = aiohttp.HttpVersion10
                    elif request.http_version == "1.1":
                        version = aiohttp.HttpVersion11
                    else:
                        logger.opt(colors=True).error(
                            "<r><bg #f8bbd0>Unsupported HTTP Version "
                            f"{request.http_version}</bg #f8bbd0></r>")
                        return

                    logger.debug(
                        f"Bot {setup_.self_id} from adapter {setup_.adapter} request {setup_.url}"
                    )

                    try:
                        async with session.request(request.method,
                                                   setup_.url,
                                                   data=request.body,
                                                   headers=headers,
                                                   timeout=timeout,
                                                   version=version) as response:
                            response.raise_for_status()
                            data = await response.read()
                            asyncio.create_task(bot.handle_message(data))
                    except aiohttp.ClientResponseError as e:
                        logger.opt(colors=True, exception=e).error(
                            f"<r><bg #f8bbd0>Error occurred while requesting {setup_.url}. "
                            "Try to reconnect...</bg #f8bbd0></r>")

                    await asyncio.sleep(setup_.poll_interval)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Unexpected exception occurred "
                "while http polling</bg #f8bbd0></r>")
        finally:
            if bot:
                self._bot_disconnect(bot)

    async def _ws_loop(self, setup: WEBSOCKET_SETUP):
        bot: Optional[Bot] = None

        try:
            async with aiohttp.ClientSession() as session:
                while True:
                    if callable(setup):
                        setup_ = await setup()
                    else:
                        setup_ = setup

                    url = URL(setup_.url)
                    if not url.is_absolute() or not url.host:
                        logger.opt(colors=True).error(
                            f"<r><bg #f8bbd0>Error parsing url {url}</bg #f8bbd0></r>"
                        )
                        await asyncio.sleep(setup_.reconnect_interval)
                        continue

                    host = f"{url.host}:{url.port}" if url.port else url.host
                    headers = {**setup_.headers, "host": host}

                    logger.debug(
                        f"Bot {setup_.self_id} from adapter {setup_.adapter} connecting to {url}"
                    )
                    try:
                        async with session.ws_connect(url,
                                                      headers=headers,
                                                      timeout=30.) as ws:
                            logger.opt(colors=True).info(
                                f"WebSocket Connection to <y>{setup_.adapter.upper()} "
                                f"Bot {setup_.self_id}</y> succeeded!")
                            request = WebSocket(
                                "1.1", url.scheme, url.path,
                                url.raw_query_string.encode("latin-1"), headers,
                                ws)

                            BotClass = self._adapters[setup_.adapter]
                            bot = BotClass(setup_.self_id, request)
                            self._bot_connect(bot)
                            while not self.should_exit.is_set():
                                msg = await ws.receive()
                                if msg.type == aiohttp.WSMsgType.text:
                                    asyncio.create_task(
                                        bot.handle_message(msg.data.encode()))
                                elif msg.type == aiohttp.WSMsgType.binary:
                                    asyncio.create_task(
                                        bot.handle_message(msg.data))
                                elif msg.type == aiohttp.WSMsgType.error:
                                    logger.opt(colors=True).error(
                                        "<r><bg #f8bbd0>Error while handling websocket frame. "
                                        "Try to reconnect...</bg #f8bbd0></r>")
                                    break
                                else:
                                    logger.opt(colors=True).error(
                                        "<r><bg #f8bbd0>WebSocket connection closed by peer. "
                                        "Try to reconnect...</bg #f8bbd0></r>")
                                    break
                    except (aiohttp.ClientResponseError,
                            aiohttp.ClientConnectionError) as e:
                        logger.opt(colors=True, exception=e).error(
                            f"<r><bg #f8bbd0>Error while connecting to {url}. "
                            "Try to reconnect...</bg #f8bbd0></r>")
                    finally:
                        if bot:
                            self._bot_disconnect(bot)
                        bot = None
                    await asyncio.sleep(setup_.reconnect_interval)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "<r><bg #f8bbd0>Unexpected exception occurred "
                "while websocket loop</bg #f8bbd0></r>")


@dataclass
class WebSocket(BaseWebSocket):
    websocket: aiohttp.ClientWebSocketResponse = None  # type: ignore

    @property
    @overrides(BaseWebSocket)
    def closed(self):
        return self.websocket.closed

    @overrides(BaseWebSocket)
    async def accept(self):
        raise NotImplementedError

    @overrides(BaseWebSocket)
    async def close(self, code: int = 1000):
        await self.websocket.close(code=code)

    @overrides(BaseWebSocket)
    async def receive(self) -> str:
        return await self.websocket.receive_str()

    @overrides(BaseWebSocket)
    async def receive_bytes(self) -> bytes:
        return await self.websocket.receive_bytes()

    @overrides(BaseWebSocket)
    async def send(self, data: str) -> None:
        await self.websocket.send_str(data)

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes) -> None:
        await self.websocket.send_bytes(data)
