import os
import re
import sys
import shlex
import warnings
import importlib
from types import ModuleType
from typing import Any, Set, Dict, Union, Optional, Iterable, Callable

from .log import logger
from nonebot import permission as perm
from .command import Command, CommandManager
from .notice_request import _bus, EventHandler
from .natural_language import NLProcessor, NLPManager
from .typing import CommandName_T, CommandHandler_T

_tmp_command: Set[Command] = set()
_tmp_nl_processor: Set[NLProcessor] = set()
_tmp_event_handler: Set[EventHandler] = set()


class Plugin:
    __slots__ = ('module', 'name', 'usage', 'commands', 'nl_processors',
                 'event_handlers')

    def __init__(self,
                 module: ModuleType,
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

    def __init__(self):
        self.cmd_manager = CommandManager()
        self.nlp_manager = NLPManager()

    @classmethod
    def add_plugin(cls, module_path: str, plugin: Plugin) -> None:
        """Register a plugin
        
        Args:
            module_path (str): module path
            plugin (Plugin): Plugin object
        """
        if module_path in cls._plugins:
            warnings.warn(f"Plugin {module_path} already exists")
            return
        cls._plugins[module_path] = plugin

    @classmethod
    def get_plugin(cls, module_path: str) -> Optional[Plugin]:
        """Get plugin object by plugin module path
        
        Args:
            module_path (str): Plugin module path
        
        Returns:
            Optional[Plugin]: Plugin object
        """
        return cls._plugins.get(module_path, None)

    @classmethod
    def remove_plugin(cls, module_path: str) -> bool:
        """Remove a plugin by plugin module path
        
        ** Warning: This function not remove plugin actually! **
        ** Just remove command, nlprocessor and event handlers **

        Args:
            module_path (str): Plugin module path

        Returns:
            bool: Success or not
        """
        plugin = cls.get_plugin(module_path)
        if not plugin:
            warnings.warn(f"Plugin {module_path} not exists")
            return False
        for command in plugin.commands:
            CommandManager.remove_command(command.name)
        for nl_processor in plugin.nl_processors:
            NLPManager.remove_nl_processor(nl_processor)
        for event_handler in plugin.event_handlers:
            for event in event_handler.events:
                _bus.unsubscribe(event, event_handler.func)
        del cls._plugins[module_path]
        return True

    @classmethod
    def switch_plugin_global(cls,
                             module_path: str,
                             state: Optional[bool] = None) -> None:
        """Change plugin state globally or simply switch it if `state` is None
        
        Args:
            module_path (str): Plugin module path
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = cls.get_plugin(module_path)
        if not plugin:
            warnings.warn(f"Plugin {module_path} not found")
            return
        for command in plugin.commands:
            CommandManager.switch_command_global(command.name, state)
        for nl_processor in plugin.nl_processors:
            NLPManager.switch_nlprocessor_global(nl_processor, state)
        for event_handler in plugin.event_handlers:
            for event in event_handler.events:
                if event_handler.func in _bus._subscribers[event] and not state:
                    _bus.unsubscribe(event, event_handler.func)
                elif event_handler.func not in _bus._subscribers[
                        event] and state != False:
                    _bus.subscribe(event, event_handler.func)

    @classmethod
    def switch_command_global(cls,
                              module_path: str,
                              state: Optional[bool] = None) -> None:
        """Change plugin command state globally or simply switch it if `state` is None
        
        Args:
            module_path (str): Plugin module path
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = cls.get_plugin(module_path)
        if not plugin:
            warnings.warn(f"Plugin {module_path} not found")
            return
        for command in plugin.commands:
            CommandManager.switch_command_global(command.name, state)

    @classmethod
    def switch_nlprocessor_global(cls,
                                  module_path: str,
                                  state: Optional[bool] = None) -> None:
        """Change plugin nlprocessor state globally or simply switch it if `state` is None
        
        Args:
            module_path (str): Plugin module path
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = cls.get_plugin(module_path)
        if not plugin:
            warnings.warn(f"Plugin {module_path} not found")
            return
        for processor in plugin.nl_processors:
            NLPManager.switch_nlprocessor_global(processor, state)

    @classmethod
    def switch_eventhandler_global(cls,
                                   module_path: str,
                                   state: Optional[bool] = None) -> None:
        """Change plugin event handler state globally or simply switch it if `state` is None
        
        Args:
            module_path (str): Plugin module path
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = cls.get_plugin(module_path)
        if not plugin:
            warnings.warn(f"Plugin {module_path} not found")
            return
        for event_handler in plugin.event_handlers:
            for event in event_handler.events:
                if event_handler.func in _bus._subscribers[event] and not state:
                    _bus.unsubscribe(event, event_handler.func)
                elif event_handler.func not in _bus._subscribers[
                        event] and state != False:
                    _bus.subscribe(event, event_handler.func)

    def switch_plugin(self, module_path: str,
                      state: Optional[bool] = None) -> None:
        """Change plugin state or simply switch it if `state` is None
        
        Tips:
            This method will only change the state of the plugin's
            commands and natural language processors since change 
            state of the event handler for message is meaningless.
        
        Args:
            module_path (str): Plugin module path
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = self.get_plugin(module_path)
        if not plugin:
            warnings.warn(f"Plugin {module_path} not found")
            return
        for command in plugin.commands:
            self.cmd_manager.switch_command(command.name, state)
        for nl_processor in plugin.nl_processors:
            self.nlp_manager.switch_nlprocessor(nl_processor, state)

    def switch_command(self, module_path: str,
                       state: Optional[bool] = None) -> None:
        """Change plugin command state or simply switch it if `state` is None
        
        Args:
            module_path (str): Plugin module path
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = self.get_plugin(module_path)
        if not plugin:
            warnings.warn(f"Plugin {module_path} not found")
            return
        for command in plugin.commands:
            self.cmd_manager.switch_command(command.name, state)

    def switch_nlprocessor(self, module_path: str,
                           state: Optional[bool] = None) -> None:
        """Change plugin nlprocessor state or simply switch it if `state` is None
        
        Args:
            module_path (str): Plugin module path
            state (Optional[bool]): State to change to. Defaults to None.
        """
        plugin = self.get_plugin(module_path)
        if not plugin:
            warnings.warn(f"Plugin {module_path} not found")
            return
        for processor in plugin.nl_processors:
            self.nlp_manager.switch_nlprocessor(processor, state)


def load_plugin(module_path: str) -> Optional[Plugin]:
    """Load a module as a plugin
    
    Args:
        module_path (str): path of module to import
    
    Returns:
        Optional[Plugin]: Plugin object loaded
    """
    # Make sure tmp is clean
    _tmp_command.clear()
    _tmp_nl_processor.clear()
    _tmp_event_handler.clear()
    try:
        module = importlib.import_module(module_path)
        name = getattr(module, '__plugin_name__', None)
        usage = getattr(module, '__plugin_usage__', None)
        commands = _tmp_command.copy()
        nl_processors = _tmp_nl_processor.copy()
        event_handlers = _tmp_event_handler.copy()
        plugin = Plugin(module, name, usage, commands, nl_processors,
                        event_handlers)
        PluginManager.add_plugin(module_path, plugin)
        logger.info(f'Succeeded to import "{module_path}"')
        return plugin
    except Exception as e:
        logger.error(f'Failed to import "{module_path}", error: {e}')
        logger.exception(e)
        return None


def reload_plugin(module_path: str) -> Optional[Plugin]:
    result = PluginManager.remove_plugin(module_path)
    if not result:
        return None

    for module in list(
            filter(lambda x: x.startswith(module_path), sys.modules.keys())):
        del sys.modules[module]

    _tmp_command.clear()
    _tmp_nl_processor.clear()
    _tmp_event_handler.clear()
    try:
        module = importlib.import_module(module_path)
        name = getattr(module, '__plugin_name__', None)
        usage = getattr(module, '__plugin_usage__', None)
        commands = _tmp_command.copy()
        nl_processors = _tmp_nl_processor.copy()
        event_handlers = _tmp_event_handler.copy()
        plugin = Plugin(module, name, usage, commands, nl_processors,
                        event_handlers)
        PluginManager.add_plugin(module_path, plugin)
        logger.info(f'Succeeded to reload "{module_path}"')
        return plugin
    except Exception as e:
        logger.error(f'Failed to reload "{module_path}", error: {e}')
        logger.exception(e)
        return None


def load_plugins(plugin_dir: str, module_prefix: str) -> Set[Plugin]:
    """Find all non-hidden modules or packages in a given directory,
    and import them with the given module prefix.

    Args:
        plugin_dir (str): Plugin directory to search
        module_prefix (str): Module prefix used while importing

    Returns:
        Set[Plugin]: Set of plugin objects successfully loaded
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
    return set(PluginManager._plugins.values())


def on_command(name: Union[str, CommandName_T],
               *,
               aliases: Union[Iterable[str], str] = (),
               permission: int = perm.EVERYBODY,
               only_to_me: bool = True,
               privileged: bool = False,
               shell_like: bool = False) -> Callable:
    """
    Decorator to register a function as a command.

    :param name: command name (e.g. 'echo' or ('random', 'number'))
    :param aliases: aliases of command name, for convenient access
    :param permission: permission required by the command
    :param only_to_me: only handle messages to me
    :param privileged: can be run even when there is already a session
    :param shell_like: use shell-like syntax to split arguments
    """

    def deco(func: CommandHandler_T) -> CommandHandler_T:
        if not isinstance(name, (str, tuple)):
            raise TypeError('the name of a command must be a str or tuple')
        if not name:
            raise ValueError('the name of a command must not be empty')

        cmd_name = (name,) if isinstance(name, str) else name

        cmd = Command(name=cmd_name,
                      func=func,
                      permission=permission,
                      only_to_me=only_to_me,
                      privileged=privileged)

        if shell_like:

            async def shell_like_args_parser(session):
                session.args['argv'] = shlex.split(session.current_arg)

            cmd.args_parser_func = shell_like_args_parser

        CommandManager.add_command(cmd_name, cmd)
        CommandManager.add_aliases(aliases, cmd)

        _tmp_command.add(cmd)
        func.args_parser = cmd.args_parser

        return func

    return deco


def on_natural_language(
        keywords: Union[Optional[Iterable], str, Callable] = None,
        *,
        permission: int = perm.EVERYBODY,
        only_to_me: bool = True,
        only_short_message: bool = True,
        allow_empty_message: bool = False) -> Callable:
    """
    Decorator to register a function as a natural language processor.

    :param keywords: keywords to respond to, if None, respond to all messages
    :param permission: permission required by the processor
    :param only_to_me: only handle messages to me
    :param only_short_message: only handle short messages
    :param allow_empty_message: handle empty messages
    """

    def deco(func: Callable) -> Callable:
        nl_processor = NLProcessor(
            func=func,
            keywords=keywords,  # type: ignore
            permission=permission,
            only_to_me=only_to_me,
            only_short_message=only_short_message,
            allow_empty_message=allow_empty_message)
        NLPManager.add_nl_processor(nl_processor)
        _tmp_nl_processor.add(nl_processor)
        return func

    if isinstance(keywords, Callable):
        # here "keywords" is the function to be decorated
        return on_natural_language()(keywords)
    else:
        if isinstance(keywords, str):
            keywords = (keywords,)
        return deco


def _make_event_deco(post_type: str) -> Callable:

    def deco_deco(arg: Optional[Union[str, Callable]] = None,
                  *events: str) -> Callable:

        def deco(func: Callable) -> Callable:
            if isinstance(arg, str):
                events_tmp = list(
                    map(lambda x: f"{post_type}.{x}", [arg] + list(events)))
                for e in events_tmp:
                    _bus.subscribe(e, func)
                handler = EventHandler(events_tmp, func)
            else:
                _bus.subscribe(post_type, func)
                handler = EventHandler([post_type], func)
            _tmp_event_handler.add(handler)
            return func

        if isinstance(arg, Callable):
            return deco(arg)  # type: ignore
        return deco

    return deco_deco


on_notice = _make_event_deco('notice')
on_request = _make_event_deco('request')
