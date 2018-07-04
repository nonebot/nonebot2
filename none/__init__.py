import asyncio
import importlib
import logging
import os
import re
from typing import Any

from aiocqhttp import CQHttp
from aiocqhttp.message import Message

from . import default_config
from .log import logger


class NoneBot(CQHttp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = default_config


def create_bot(config_object: Any = None) -> NoneBot:
    if config_object is None:
        config_object = default_config

    kwargs = {k.lower(): v for k, v in config_object.__dict__.items()
              if k.isupper() and not k.startswith('_')}

    bot = NoneBot(message_class=Message, **kwargs)
    bot.config = config_object
    if bot.config.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    bot.asgi.debug = bot.config.DEBUG

    from .message import handle_message
    from .notice_request import handle_notice_or_request

    @bot.on_message
    async def _(ctx):
        asyncio.ensure_future(handle_message(bot, ctx))

    @bot.on_notice
    async def _(ctx):
        asyncio.ensure_future(handle_notice_or_request(bot, ctx))

    @bot.on_request
    async def _(ctx):
        asyncio.ensure_future(handle_notice_or_request(bot, ctx))

    return bot


_plugins = set()


def load_plugins(plugin_dir: str, module_prefix: str) -> None:
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
            logger.info('Succeeded to import "{}"'.format(mod_name))
        except ImportError:
            logger.warning('Failed to import "{}"'.format(mod_name))


def load_builtin_plugins() -> None:
    plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
    load_plugins(plugin_dir, 'none.plugins')


from .command import on_command, CommandSession, CommandGroup
from .natural_language import on_natural_language, NLPSession, NLPResult
from .notice_request import (
    on_notice, NoticeSession,
    on_request, RequestSession,
)
