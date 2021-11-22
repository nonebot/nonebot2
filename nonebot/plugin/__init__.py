"""
插件
====

为 NoneBot 插件开发提供便携的定义函数。
"""

from typing import List, Optional
from contextvars import ContextVar

_managers: List["PluginManager"] = []
_current_plugin: ContextVar[Optional["Plugin"]] = ContextVar(
    "_current_plugin", default=None
)

from .on import on as on
from .manager import PluginManager
from .export import Export as Export
from .export import export as export
from .load import require as require
from .on import on_regex as on_regex
from .plugin import Plugin as Plugin
from .on import on_notice as on_notice
from .on import on_command as on_command
from .on import on_keyword as on_keyword
from .on import on_message as on_message
from .on import on_request as on_request
from .on import on_endswith as on_endswith
from .load import load_plugin as load_plugin
from .on import CommandGroup as CommandGroup
from .on import MatcherGroup as MatcherGroup
from .on import on_metaevent as on_metaevent
from .plugin import get_plugin as get_plugin
from .load import load_plugins as load_plugins
from .on import on_startswith as on_startswith
from .load import load_from_json as load_from_json
from .load import load_from_toml as load_from_toml
from .on import on_shell_command as on_shell_command
from .load import load_all_plugins as load_all_plugins
from .plugin import get_loaded_plugins as get_loaded_plugins
from .load import load_builtin_plugins as load_builtin_plugins
