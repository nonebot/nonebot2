"""
插件
====

为 NoneBot 插件开发提供便携的定义函数。
"""

from typing import Optional
from contextvars import ContextVar

_current_plugin: ContextVar[Optional["Plugin"]] = ContextVar("_current_plugin",
                                                             default=None)

from .export import Export as Export
from .export import export as export
from .plugin import Plugin as Plugin
from .plugin import get_plugin as get_plugin
from .plugin import get_loaded_plugins as get_loaded_plugins
