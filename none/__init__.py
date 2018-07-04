import asyncio
import importlib
import logging
import os
import re
from typing import Any, Optional

from aiocqhttp import CQHttp
from aiocqhttp.message import Message

from . import default_config
from .log import logger


class NoneBot(CQHttp):
    def __init__(self, config_object: Any = None):
        if config_object is None:
            config_object = default_config

        super_kwargs = {k.lower(): v for k, v in config_object.__dict__.items()
                        if k.isupper() and not k.startswith('_')}
        super().__init__(message_class=Message, **super_kwargs)

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

    def run(self, host=None, port=None, *args, **kwargs):
        super().run(host=host, port=port, loop=asyncio.get_event_loop(),
                    *args, **kwargs)

    def get_data_folder(self,
                        *sub_folder: str) -> Optional[str]:
        folder = self.config.DATA_FOLDER
        if not folder:
            return None

        if sub_folder:
            folder = os.path.join(folder, *sub_folder)

        if not os.path.isdir(folder):
            os.makedirs(folder, 0o755, exist_ok=True)
        return folder

    def get_data_file(self, path: str, *others: str) -> Optional[str]:
        rel_path = os.path.join(path, *others)
        parent = self.get_data_folder(os.path.dirname(rel_path))
        if not parent:
            return None
        return os.path.join(parent, os.path.basename(rel_path))


_bot = None


def init(config_object: Any = None) -> None:
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


def get_bot() -> NoneBot:
    """
    Get the NoneBot instance.

    :raise ValueError: instance not initialized
    """
    if _bot is None:
        raise ValueError('NoneBot instance has not been initialized')
    # noinspection PyTypeChecker
    return _bot


def run(host: str = None, port: int = None, *args, **kwargs) -> None:
    """Run the NoneBot instance."""
    get_bot().run(host=host, port=port, *args, **kwargs)


_plugins = set()


def clear_plugins() -> None:
    _plugins.clear()


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
