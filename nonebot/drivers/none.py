"""None 驱动适配

:::tip 提示
本驱动不支持任何服务器或客户端连接
:::

FrontMatter:
    mdx:
        format: md
    sidebar_position: 6
    description: nonebot.drivers.none 模块
"""

import signal
from typing import Optional
from typing_extensions import override

import anyio
from anyio.abc import TaskGroup
from exceptiongroup import BaseExceptionGroup, catch

from nonebot.config import Config, Env
from nonebot.consts import WINDOWS
from nonebot.drivers import Driver as BaseDriver
from nonebot.log import logger
from nonebot.utils import flatten_exception_group

HANDLED_SIGNALS = (
    signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
    signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
)
if WINDOWS:  # pragma: py-win32
    HANDLED_SIGNALS += (signal.SIGBREAK,)  # Windows signal 21. Sent by Ctrl+Break.


class Driver(BaseDriver):
    """None 驱动框架"""

    def __init__(self, env: Env, config: Config):
        super().__init__(env, config)

        self.should_exit: anyio.Event = anyio.Event()
        self.force_exit: anyio.Event = anyio.Event()

    @property
    @override
    def type(self) -> str:
        """驱动名称: `none`"""
        return "none"

    @property
    @override
    def logger(self):
        """none driver 使用的 logger"""
        return logger

    @override
    def run(self, *args, **kwargs):
        """启动 none driver"""
        super().run(*args, **kwargs)
        anyio.run(self._serve)

    async def _serve(self):
        async with anyio.create_task_group() as driver_tg:
            driver_tg.start_soon(self._handle_signals)
            driver_tg.start_soon(self._listen_force_exit, driver_tg)
            driver_tg.start_soon(self._handle_lifespan, driver_tg)

    async def _handle_signals(self):
        try:
            with anyio.open_signal_receiver(*HANDLED_SIGNALS) as signal_receiver:
                async for sig in signal_receiver:
                    self.exit(force=self.should_exit.is_set())
        except NotImplementedError:
            # Windows
            for sig in HANDLED_SIGNALS:
                signal.signal(sig, self._handle_legacy_signal)

    # backport for Windows signal handling
    def _handle_legacy_signal(self, sig, frame):
        self.exit(force=self.should_exit.is_set())

    async def _handle_lifespan(self, tg: TaskGroup):
        try:
            await self._startup()

            if self.should_exit.is_set():
                return

            await self._listen_exit()

            await self._shutdown()
        finally:
            tg.cancel_scope.cancel()

    async def _startup(self):
        def handle_exception(exc_group: BaseExceptionGroup[Exception]) -> None:
            self.should_exit.set()

            for exc in flatten_exception_group(exc_group):
                logger.opt(colors=True, exception=exc).error(
                    "<r><bg #f8bbd0>Error occurred while running startup hook."
                    "</bg #f8bbd0></r>"
                )
            logger.error(
                "<r><bg #f8bbd0>Application startup failed. Exiting.</bg #f8bbd0></r>"
            )

        with catch({Exception: handle_exception}):
            await self._lifespan.startup()

        if not self.should_exit.is_set():
            logger.info("Application startup completed.")

    async def _listen_exit(self, tg: Optional[TaskGroup] = None):
        await self.should_exit.wait()

        if tg is not None:
            tg.cancel_scope.cancel()

    async def _shutdown(self):
        logger.info("Shutting down")
        logger.info("Waiting for application shutdown. (CTRL+C to force quit)")

        error_occurred: bool = False

        def handle_exception(exc_group: BaseExceptionGroup[Exception]) -> None:
            nonlocal error_occurred

            error_occurred = True

            for exc in flatten_exception_group(exc_group):
                logger.opt(colors=True, exception=exc).error(
                    "<r><bg #f8bbd0>Error occurred while running shutdown hook."
                    "</bg #f8bbd0></r>"
                )
            logger.error(
                "<r><bg #f8bbd0>Application shutdown failed. Exiting.</bg #f8bbd0></r>"
            )

        with catch({Exception: handle_exception}):
            await self._lifespan.shutdown()

        if not error_occurred:
            logger.info("Application shutdown complete.")

    async def _listen_force_exit(self, tg: TaskGroup):
        await self.force_exit.wait()
        tg.cancel_scope.cancel()

    def exit(self, force: bool = False):
        """退出 none driver

        参数:
            force: 强制退出
        """
        if not self.should_exit.is_set():
            self.should_exit.set()
        if force:
            self.force_exit.set()
