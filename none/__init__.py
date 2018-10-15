import asyncio
import importlib
import logging
import os
import re
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


_plugins = set()


def load_plugins(plugin_dir: str, module_prefix: str) -> None:
    """
    Find all non-hidden modules or packages in a given directory,
    and import them with the given module prefix.

    :param plugin_dir: plugin directory to search
    :param module_prefix: module prefix used while importing
    """
    for name in os.listdir(plugin_dir):
        path = os.path.join(plugin_dir, name)
        if os.path.isfile(path) and \
                (name.startswith('_') or not name.endswith('.py')):
            continue
        if os.path.isdir(path) and \
                (name.startswith('_') or not os.path.exists(
                    os.path.join(path, '__init__.py'))):
            continue

        m = re.match(r'([_A-Z0-9a-z]+)(.py)?', name)
        if not m:
            continue

        mod_name = f'{module_prefix}.{m.group(1)}'
        try:
            _plugins.add(importlib.import_module(mod_name))
            logger.info(f'Succeeded to import "{mod_name}"')
        except ImportError:
            logger.warning(f'Failed to import "{mod_name}"')


def load_builtin_plugins() -> None:
    """
    Load built-in plugins distributed along with "none" package.
    """
    plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
    load_plugins(plugin_dir, 'none.plugins')


from .exceptions import *
from .message import message_preprocessor, Message, MessageSegment
from .command import on_command, CommandSession, CommandGroup
from .natural_language import on_natural_language, NLPSession, NLPResult
from .notice_request import (on_notice, NoticeSession,
                             on_request, RequestSession)
