import importlib
import os
import re
from typing import Any, Set, NamedTuple, Optional

from .log import logger


class Plugin(NamedTuple):
    module: Any
    name: Optional[str] = None
    usage: Optional[Any] = None


_plugins: Set[Plugin] = set()


def load_plugin(module_name: str) -> bool:
    """
    Load a module as a plugin.

    :param module_name: name of module to import
    :return: successful or not
    """
    try:
        module = importlib.import_module(module_name)
        name = getattr(module, '__plugin_name__', None)
        usage = getattr(module, '__plugin_usage__', None)
        _plugins.add(Plugin(module, name, usage))
        logger.info(f'Succeeded to import "{module_name}"')
        return True
    except Exception as e:
        logger.error(f'Failed to import "{module_name}", error: {e}')
        logger.exception(e)
        return False


def load_plugins(plugin_dir: str, module_prefix: str) -> int:
    """
    Find all non-hidden modules or packages in a given directory,
    and import them with the given module prefix.

    :param plugin_dir: plugin directory to search
    :param module_prefix: module prefix used while importing
    :return: number of plugins successfully loaded
    """
    count = 0
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

        if load_plugin(f'{module_prefix}.{m.group(1)}'):
            count += 1
    return count


def load_builtin_plugins() -> int:
    """
    Load built-in plugins distributed along with "nonebot" package.
    """
    plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
    return load_plugins(plugin_dir, 'nonebot.plugins')


def get_loaded_plugins() -> Set[Plugin]:
    """
    Get all plugins loaded.

    :return: a set of Plugin objects
    """
    return _plugins
