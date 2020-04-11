import os
import re
import warnings
import importlib
from types import ModuleType
from typing import Any, Set, Dict, Optional

from .log import logger
from .command import Command, CommandManager
from .natural_language import NLProcessor, NLPManager
from .notice_request import _bus, EventHandler


class Plugin:
    __slots__ = ('module', 'name', 'usage', 'commands', 'nl_processors', 'event_handlers')

    def __init__(self, module: ModuleType,
                 name: Optional[str] = None,
                 usage: Optional[Any] = None,
                 commands: Set[Command] = set(),
                 nl_processors: Set[NLProcessor] = set(),
                 event_handlers: Set[EventHandler] = set()):
        self.module = module
        self.name = name
        self.usage = usage
        self.commands = commands
        self.nl_processors = nl_processors
        self.event_handlers = event_handlers

class PluginManager:
    _plugins: Dict[str, Plugin] = {}
    _anonymous_plugins: Set[Plugin] = set()
    
    def __init__(self):
        self.cmd_manager = CommandManager()
        self.nlp_manager = NLPManager()
    
    @classmethod
    def add_plugin(cls, plugin: Plugin) -> None:
        """Register a plugin
        
        Args:
            plugin (Plugin): Plugin object
        """
        if plugin.name:
            if plugin.name in cls._plugins:
                warnings.warn(f"Plugin {plugin.name} already exists")
                return
            cls._plugins[plugin.name] = plugin
        else:
            cls._anonymous_plugins.add(plugin)
    
    @classmethod
    def get_plugin(cls, name: str) -> Optional[Plugin]:
        return cls._plugins.get(name)
    
    # TODO: plugin重加载
    @classmethod
    def reload_plugin(cls, plugin: Plugin) -> None:
        pass

    @classmethod
    def switch_plugin_global(cls, name: str, state: Optional[bool] = None) -> None:
        """Change plugin state globally or simply switch it if `state` is None
        
        Args:
            name (str): Plugin name
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = cls.get_plugin(name)
        if not plugin:
            warnings.warn(f"Plugin {name} not found")
            return
        for command in plugin.commands:
            CommandManager.switch_command_global(command.name, state)
        for nl_processor in plugin.nl_processors:
            NLPManager.switch_nlprocessor_global(nl_processor, state)
        for event_handler in plugin.event_handlers:
            for event in event_handler.events:
                if event_handler.func in _bus._subscribers[event] and not state:
                    _bus.unsubscribe(event, event_handler.func)
                elif event_handler.func not in _bus._subscribers[event] and state != False:
                    _bus.subscribe(event, event_handler.func)

    @classmethod
    def switch_command_global(cls, name: str, state: Optional[bool] = None) -> None:
        """Change plugin command state globally or simply switch it if `state` is None
        
        Args:
            name (str): Plugin name
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = cls.get_plugin(name)
        if not plugin:
            warnings.warn(f"Plugin {name} not found")
            return
        for command in plugin.commands:
            CommandManager.switch_command_global(command.name, state)
    
    @classmethod
    def switch_nlprocessor_global(cls, name: str, state: Optional[bool] = None) -> None:
        """Change plugin nlprocessor state globally or simply switch it if `state` is None
        
        Args:
            name (str): Plugin name
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = cls.get_plugin(name)
        if not plugin:
            warnings.warn(f"Plugin {name} not found")
            return
        for processor in plugin.nl_processors:
            NLPManager.switch_nlprocessor_global(processor, state)

    @classmethod
    def switch_eventhandler_global(cls, name: str, state: Optional[bool] = None) -> None:
        """Change plugin event handler state globally or simply switch it if `state` is None
        
        Args:
            name (str): Plugin name
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = cls.get_plugin(name)
        if not plugin:
            warnings.warn(f"Plugin {name} not found")
            return
        for event_handler in plugin.event_handlers:
            for event in event_handler.events:
                if event_handler.func in _bus._subscribers[event] and not state:
                    _bus.unsubscribe(event, event_handler.func)
                elif event_handler.func not in _bus._subscribers[event] and state != False:
                    _bus.subscribe(event, event_handler.func)

    def switch_plugin(self, name: str, state: Optional[bool] = None) -> None:
        """Change plugin state or simply switch it if `state` is None
        
        Tips:
            This method will only change the state of the plugin's
            commands and natural language processors since change 
            state of the event handler partially is meaningless.
        
        Args:
            name (str): Plugin name
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = self.get_plugin(name)
        if not plugin:
            warnings.warn(f"Plugin {name} not found")
            return
        for command in plugin.commands:
            self.cmd_manager.switch_command(command.name, state)
        for nl_processor in plugin.nl_processors:
            self.nlp_manager.switch_nlprocessor(nl_processor, state)
    
    def switch_command(self, name: str, state: Optional[bool] = None) -> None:
        """Change plugin command state or simply switch it if `state` is None
        
        Args:
            name (str): Plugin name
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = self.get_plugin(name)
        if not plugin:
            warnings.warn(f"Plugin {name} not found")
            return
        for command in plugin.commands:
            self.cmd_manager.switch_command(command.name, state)

    def switch_nlprocessor(self, name: str, state: Optional[bool] = None) -> None:
        """Change plugin nlprocessor state or simply switch it if `state` is None
        
        Args:
            name (str): Plugin name
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = self.get_plugin(name)
        if not plugin:
            warnings.warn(f"Plugin {name} not found")
            return
        for processor in plugin.nl_processors:
            self.nlp_manager.switch_nlprocessor(processor, state)


def load_plugin(module_name: str) -> Optional[Plugin]:
    """
    Load a module as a plugin.

    :param module_name: name of module to import
    :return: successful or not
    """
    try:
        module = importlib.import_module(module_name)
        name = getattr(module, '__plugin_name__', None)
        usage = getattr(module, '__plugin_usage__', None)
        commands = set()
        nl_processors = set()
        event_handlers = set()
        for attr in dir(module):
            func = getattr(module, attr)
            if isinstance(func, Command):
                commands.add(func)
            elif isinstance(func, NLProcessor):
                nl_processors.add(func)
            elif isinstance(func, EventHandler):
                event_handlers.add(func)
        plugin = Plugin(module, name, usage, commands, nl_processors, event_handlers)
        PluginManager.add_plugin(plugin)
        logger.info(f'Succeeded to import "{module_name}"')
        return plugin
    except Exception as e:
        logger.error(f'Failed to import "{module_name}", error: {e}')
        logger.exception(e)
        return None


# TODO: plugin重加载
def reload_plugin(module_name: str) -> Optional[Plugin]:
    pass


def load_plugins(plugin_dir: str, module_prefix: str) -> Set[Plugin]:
    """
    Find all non-hidden modules or packages in a given directory,
    and import them with the given module prefix.

    :param plugin_dir: plugin directory to search
    :param module_prefix: module prefix used while importing
    :return: number of plugins successfully loaded
    """
    count = set()
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

        result = load_plugin(f'{module_prefix}.{m.group(1)}')
        if result:
            count.add(result)
    return count


def load_builtin_plugins() -> Set[Plugin]:
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
    return set(PluginManager._plugins.values()) | PluginManager._anonymous_plugins
