import asyncio
import logging
from typing import Any, Optional

import aiocqhttp.message
from aiocqhttp import CQHttp

from .log import logger
from .sched import Scheduler

if Scheduler:
    scheduler = Scheduler()
else:
    scheduler = None


class NoneBot(CQHttp):
    def __init__(self, config_object: Optional[Any] = None):
        if config_object is None:
            from . import default_config as config_object

        config_dict = {k: v for k, v in config_object.__dict__.items()
                       if k.isupper() and not k.startswith('_')}
        logger.debug(f'Loaded configurations: {config_dict}')
        super().__init__(message_class=aiocqhttp.message.Message,
                         **{k.lower(): v for k, v in config_dict.items()})

        self.config = config_object
        self.asgi.debug = self.config.DEBUG

        from .message import handle_message
        from .notice_request import handle_notice_or_request

        @self.on_message
        async def _(ctx):
            asyncio.ensure_future(handle_message(self, ctx))

        @self.on_notice
        async def _(ctx):
            asyncio.ensure_future(handle_notice_or_request(self, ctx))

        @self.on_request
        async def _(ctx):
            asyncio.ensure_future(handle_notice_or_request(self, ctx))

    def run(self, host: Optional[str] = None, port: Optional[int] = None,
            *args, **kwargs) -> None:
        host = host or self.config.HOST
        port = port or self.config.PORT
        if 'debug' not in kwargs:
            kwargs['debug'] = self.config.DEBUG

        logger.info(f'Running on {host}:{port}')
        super().run(host=host, port=port, loop=asyncio.get_event_loop(),
                    *args, **kwargs)


_bot: Optional[NoneBot] = None


def init(config_object: Optional[Any] = None) -> None:
    """
    Initialize NoneBot instance.

    This function must be called at the very beginning of code,
    otherwise the get_bot() function will return None and nothing
    is gonna work properly.

    :param config_object: configuration object
    """
    global _bot
    _bot = NoneBot(config_object)

    if _bot.config.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if scheduler and not scheduler.running:
        scheduler.configure(_bot.config.APSCHEDULER_CONFIG)
        scheduler.start()


def get_bot() -> NoneBot:
    """
    Get the NoneBot instance.

    The result is ensured to be not None, otherwise an exception will
    be raised.

    :raise ValueError: instance not initialized
    """
    if _bot is None:
        raise ValueError('NoneBot instance has not been initialized')
    return _bot


def run(host: Optional[str] = None, port: Optional[int] = None,
        *args, **kwargs) -> None:
    """Run the NoneBot instance."""
    get_bot().run(host=host, port=port, *args, **kwargs)


from .exceptions import *
from .plugin import (load_plugin, load_plugins, load_builtin_plugins,
                     get_loaded_plugins)
from .message import message_preprocessor, Message, MessageSegment
from .command import on_command, CommandSession, CommandGroup
from .natural_language import on_natural_language, NLPSession, NLPResult
from .notice_request import (on_notice, NoticeSession,
                             on_request, RequestSession)

__all__ = [
    'NoneBot', 'scheduler', 'init', 'get_bot', 'run',
    'CQHttpError',
    'load_plugin', 'load_plugins', 'load_builtin_plugins',
    'get_loaded_plugins',
    'message_preprocessor', 'Message', 'MessageSegment',
    'on_command', 'CommandSession', 'CommandGroup',
    'on_natural_language', 'NLPSession', 'NLPResult',
    'on_notice', 'NoticeSession', 'on_request', 'RequestSession',
]
