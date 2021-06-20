"""
"""

import signal
import asyncio
from typing import Set, Union, Callable, Awaitable

import aiohttp

from nonebot.log import logger
from nonebot.typing import overrides
from nonebot.config import Env, Config
from nonebot.drivers import ForwardDriver, HTTPConnection, HTTPRequest, WebSocket

STARTUP_FUNC = Callable[[], Awaitable[None]]
SHUTDOWN_FUNC = Callable[[], Awaitable[None]]
AVAILABLE_REQUEST = Union[HTTPRequest, WebSocket]


class Driver(ForwardDriver):

    def __init__(self, env: Env, config: Config):
        super().__init__(env, config)
        self.startup_funcs: Set[STARTUP_FUNC] = set()
        self.shutdown_funcs: Set[SHUTDOWN_FUNC] = set()
        self.requests: Set[AVAILABLE_REQUEST] = set()

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
    def setup(self, request: HTTPConnection) -> None:
        if not isinstance(request, (HTTPRequest, WebSocket)):
            raise TypeError(f"Request Type {type(request)!r} is not supported!")
        self.requests.add(request)

    @overrides(ForwardDriver)
    def run(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
        for s in signals:
            loop.add_signal_handler(
                s,
                lambda s=s: asyncio.create_task(self.shutdown(loop, signal=s)))

        try:
            asyncio.create_task(self.startup())
            loop.run_forever()
        finally:
            loop.close()

    async def startup(self):
        # TODO: build request

        # run startup
        cors = [startup() for startup in self.startup_funcs]
        if cors:
            try:
                await asyncio.gather(*cors)
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running startup function. "
                    "Ignored!</bg #f8bbd0></r>")

    async def shutdown(self,
                       loop: asyncio.AbstractEventLoop,
                       signal: signal.Signals = None):
        # TODO: shutdown

        # run shutdown
        cors = [shutdown() for shutdown in self.shutdown_funcs]
        if cors:
            try:
                await asyncio.gather(*cors)
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running shutdown function. "
                    "Ignored!</bg #f8bbd0></r>")

        tasks = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

        loop.stop()
