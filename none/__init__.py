import os
import sys
import importlib
import logging
import re
import asyncio
from typing import Any

from aiocqhttp import CQHttp
from aiocqhttp.message import Message

logger = logging.getLogger('none')
default_handler = logging.StreamHandler(sys.stdout)
default_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(message)s'
))
logger.addHandler(default_handler)

from .plugin import handle_message, handle_notice, handle_request
from .command import on_command


def create_bot(config_object: Any = None):
    if config_object is None:
        from . import default_config as config_object

    kwargs = {k.lower(): v for k, v in config_object.__dict__.items()
              if k.isupper() and not k.startswith('_')}

    bot = CQHttp(message_class=Message, **kwargs)
    bot.config = config_object
    if bot.config.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    bot.asgi.debug = bot.config.DEBUG

    @bot.on_message
    async def _(ctx):
        asyncio.ensure_future(handle_message(bot, ctx))

    @bot.on_notice
    async def _(ctx):
        asyncio.ensure_future(handle_notice(bot, ctx))

    @bot.on_request
    async def _(ctx):
        asyncio.ensure_future(handle_request(bot, ctx))

    return bot


_plugins = set()


def load_plugins():
    _plugins.clear()
    root_dir = os.path.dirname(__path__[0])
    plugins_dir = os.path.join(root_dir, 'plugins')
    saved_cwd = os.getcwd()
    os.chdir(root_dir)
    for item in os.listdir(plugins_dir):
        path = os.path.join(plugins_dir, item)
        if os.path.isfile(path) and \
                (path.startswith('_') or not path.endswith('.py')):
            continue
        if os.path.isdir(path) and \
                (path.startswith('_') or not os.path.exists(
                    os.path.join(path, '__init__.py'))):
            continue

        m = re.match(r'([_A-Z0-9a-z]+)(.py)?', item)
        if not m:
            continue

        mod_name = 'plugins.' + m.group(1)
        try:
            _plugins.add(importlib.import_module(mod_name))
            logger.info('Succeeded to import "{}"'.format(mod_name))
        except ImportError:
            logger.warning('Failed to import "{}"'.format(mod_name))
    os.chdir(saved_cwd)
