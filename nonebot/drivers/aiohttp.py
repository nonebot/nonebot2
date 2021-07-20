"""
"""

import signal
import asyncio
import threading
from dataclasses import dataclass
from typing import Set, List, Dict, Optional, Callable, Awaitable

import aiohttp
from yarl import URL

from nonebot.log import logger
from nonebot.adapters import Bot
from nonebot.typing import overrides
from nonebot.config import Env, Config
from nonebot.drivers import ForwardDriver, HTTPRequest, WebSocket as BaseWebSocket

STARTUP_FUNC = Callable[[], Awaitable[None]]
SHUTDOWN_FUNC = Callable[[], Awaitable[None]]
HANDLED_SIGNALS = (
    signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
    signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
)


@dataclass
class HTTPPollingSetup:
    adapter: str
    self_id: str
    url: str
    method: str
    body: bytes
    headers: Dict[str, str]
    http_version: str
    poll_interval: float


@dataclass
class WebSocketSetup:
    adapter: str
    self_id: str
    url: str
    headers: Dict[str, str]
    http_version: str
    reconnect_interval: float


class Driver(ForwardDriver):

    def __init__(self, env: Env, config: Config):
        super().__init__(env, config)
        self.startup_funcs: Set[STARTUP_FUNC] = set()
        self.shutdown_funcs: Set[SHUTDOWN_FUNC] = set()
        self.http_pollings: List[HTTPPollingSetup] = []
        self.websockets: List[WebSocketSetup] = []
        self.connections: List[asyncio.Task] = []
        self.should_exit: bool = False
        self.force_exit: bool = False

    @property
    @overrides(ForwardDriver)
    def type(self) -> str:
        """驱动名称: ``aiohttp``"""
        return "aiohttp"

    @property
    @overrides(ForwardDriver)
    def logger(self):
        return logger

    @overrides(ForwardDriver)
    def on_startup(self, func: Callable) -> Callable:
        self.startup_funcs.add(func)
        return func

    @overrides(ForwardDriver)
    def on_shutdown(self, func: Callable) -> Callable:
        self.shutdown_funcs.add(func)
        return func

    @overrides(ForwardDriver)
    def setup_http_polling(self,
                           adapter: str,
                           self_id: str,
                           url: str,
                           polling_interval: float = 3.,
                           method: str = "GET",
                           body: bytes = b"",
                           headers: Dict[str, str] = {},
                           http_version: str = "1.1") -> None:
        self.http_pollings.append(
            HTTPPollingSetup(adapter, self_id, url, method, body, headers,
                             http_version, polling_interval))

    @overrides(ForwardDriver)
    def setup_websocket(self,
                        adapter: str,
                        self_id: str,
                        url: str,
                        reconnect_interval: float = 3.,
                        headers: Dict[str, str] = {},
                        http_version: str = "1.1") -> None:
        self.websockets.append(
            WebSocketSetup(adapter, self_id, url, headers, http_version,
                           reconnect_interval))

    @overrides(ForwardDriver)
    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.serve())

    async def serve(self):
        self.install_signal_handlers()
        await self.startup()
        if self.should_exit:
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
        while not self.should_exit:
            await asyncio.sleep(0.1)

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
        if self.should_exit:
            self.force_exit = True
        else:
            self.should_exit = True

    async def _http_loop(self, setup: HTTPPollingSetup):
        url = URL(setup.url)
        if not url.is_absolute() or not url.host:
            logger.opt(colors=True).error(
                f"<r><bg #f8bbd0>Error parsing url {url}</bg #f8bbd0></r>")
            return
        host = f"{url.host}:{url.port}" if url.port else url.host
        request = HTTPRequest(setup.http_version, url.scheme, url.path,
                              url.raw_query_string.encode("latin-1"), {
                                  **setup.headers, "host": host
                              }, setup.method, setup.body)

        BotClass = self._adapters[setup.adapter]
        bot = BotClass(setup.self_id, request)
        self._bot_connect(bot)

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

        try:
            async with aiohttp.ClientSession(headers=headers,
                                             timeout=timeout,
                                             version=version) as session:
                while not self.should_exit:
                    logger.debug(
                        f"Bot {setup.self_id} from adapter {setup.adapter} request {url}"
                    )
                    try:
                        async with session.request(
                                request.method, url,
                                data=request.body) as response:
                            response.raise_for_status()
                            data = await response.read()
                            asyncio.create_task(bot.handle_message(data))
                    except aiohttp.ClientResponseError as e:
                        logger.opt(colors=True, exception=e).error(
                            f"<r><bg #f8bbd0>Error occurred while requesting {url}. "
                            "Try to reconnect...</bg #f8bbd0></r>")

                    await asyncio.sleep(setup.poll_interval)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "Unexpected exception occurred while http polling")
        finally:
            self._bot_disconnect(bot)

    async def _ws_loop(self, setup: WebSocketSetup):
        url = URL(setup.url)
        if not url.is_absolute() or not url.host:
            logger.opt(colors=True).error(
                f"<r><bg #f8bbd0>Error parsing url {url}</bg #f8bbd0></r>")
            return
        host = f"{url.host}:{url.port}" if url.port else url.host

        headers = {**setup.headers, "host": host}
        timeout = aiohttp.ClientTimeout(30)
        version: aiohttp.HttpVersion
        if setup.http_version == "1.0":
            version = aiohttp.HttpVersion10
        elif setup.http_version == "1.1":
            version = aiohttp.HttpVersion11
        else:
            logger.opt(colors=True).error(
                "<r><bg #f8bbd0>Unsupported HTTP Version "
                f"{setup.http_version}</bg #f8bbd0></r>")
            return

        bot: Optional[Bot] = None
        try:
            async with aiohttp.ClientSession(headers=headers,
                                             timeout=timeout,
                                             version=version) as session:
                while True:
                    logger.debug(
                        f"Bot {setup.self_id} from adapter {setup.adapter} connecting to {url}"
                    )
                    try:
                        async with session.ws_connect(url) as ws:
                            request = WebSocket(
                                setup.http_version, url.scheme, url.path,
                                url.raw_query_string.encode("latin-1"), {
                                    **setup.headers, "host": host
                                }, ws)

                            BotClass = self._adapters[setup.adapter]
                            bot = BotClass(setup.self_id, request)
                            self._bot_connect(bot)
                            while not self.should_exit:
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
                    except aiohttp.WSServerHandshakeError as e:
                        logger.opt(colors=True, exception=e).error(
                            f"<r><bg #f8bbd0>Error while connecting to {url}"
                            "Try to reconnect...</bg #f8bbd0></r>")
                    finally:
                        if bot:
                            self._bot_disconnect(bot)
                        bot = None
                    await asyncio.sleep(setup.reconnect_interval)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                "Unexpected exception occurred while websocket loop")


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
