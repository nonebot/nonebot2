"""None 驱动适配

:::tip 提示
本驱动不支持任何服务器或客户端连接
:::

FrontMatter:
    sidebar_position: 6
    description: nonebot.drivers.none 模块
"""


import signal
import asyncio
import threading
from typing import Set, Union, Callable, Awaitable, cast

from nonebot.log import logger
from nonebot.typing import overrides
from nonebot.config import Env, Config
from nonebot.drivers import Driver as BaseDriver
from nonebot.utils import run_sync, is_coroutine_callable

HOOK_FUNC = Union[Callable[[], None], Callable[[], Awaitable[None]]]
HANDLED_SIGNALS = (
    signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
    signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
)


class Driver(BaseDriver):
    """None 驱动框架"""

    def __init__(self, env: Env, config: Config):
        super().__init__(env, config)
        self.startup_funcs: Set[HOOK_FUNC] = set()
        self.shutdown_funcs: Set[HOOK_FUNC] = set()
        self.should_exit: asyncio.Event = asyncio.Event()
        self.force_exit: bool = False

    @property
    @overrides(BaseDriver)
    def type(self) -> str:
        """驱动名称: `none`"""
        return "none"

    @property
    @overrides(BaseDriver)
    def logger(self):
        """none driver 使用的 logger"""
        return logger

    @overrides(BaseDriver)
    def on_startup(self, func: HOOK_FUNC) -> HOOK_FUNC:
        """
        注册一个启动时执行的函数
        """
        self.startup_funcs.add(func)
        return func

    @overrides(BaseDriver)
    def on_shutdown(self, func: HOOK_FUNC) -> HOOK_FUNC:
        """
        注册一个停止时执行的函数
        """
        self.shutdown_funcs.add(func)
        return func

    @overrides(BaseDriver)
    def run(self, *args, **kwargs):
        """启动 none driver"""
        super().run(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._serve())

    async def _serve(self):
        self._install_signal_handlers()
        await self._startup()
        if self.should_exit.is_set():
            return
        await self._main_loop()
        await self._shutdown()

    async def _startup(self):
        # run startup
        cors = [
            cast(Callable[..., Awaitable[None]], startup)()
            if is_coroutine_callable(startup)
            else run_sync(startup)()
            for startup in self.startup_funcs
        ]
        if cors:
            try:
                await asyncio.gather(*cors)
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running startup function. "
                    "Ignored!</bg #f8bbd0></r>"
                )

        logger.info("Application startup completed.")

    async def _main_loop(self):
        await self.should_exit.wait()

    async def _shutdown(self):
        logger.info("Shutting down")

        logger.info("Waiting for application shutdown.")
        # run shutdown
        cors = [
            cast(Callable[..., Awaitable[None]], shutdown)()
            if is_coroutine_callable(shutdown)
            else run_sync(shutdown)()
            for shutdown in self.shutdown_funcs
        ]
        if cors:
            try:
                await asyncio.gather(*cors)
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    "<r><bg #f8bbd0>Error when running shutdown function. "
                    "Ignored!</bg #f8bbd0></r>"
                )

        for task in asyncio.all_tasks():
            if task is not asyncio.current_task() and not task.done():
                task.cancel()
        await asyncio.sleep(0.1)

        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        if tasks and not self.force_exit:
            logger.info("Waiting for tasks to finish. (CTRL+C to force quit)")
        while tasks and not self.force_exit:
            await asyncio.sleep(0.1)
            tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

        logger.info("Application shutdown complete.")
        loop = asyncio.get_event_loop()
        loop.stop()

    def _install_signal_handlers(self) -> None:
        if threading.current_thread() is not threading.main_thread():
            # Signals can only be listened to from the main thread.
            return

        loop = asyncio.get_event_loop()

        try:
            for sig in HANDLED_SIGNALS:
                loop.add_signal_handler(sig, self._handle_exit, sig, None)
        except NotImplementedError:
            # Windows
            for sig in HANDLED_SIGNALS:
                signal.signal(sig, self._handle_exit)

    def _handle_exit(self, sig, frame):
        if self.should_exit.is_set():
            self.force_exit = True
        else:
            self.should_exit.set()
