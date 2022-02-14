"""本模块为 NoneBot 插件开发提供便携的定义函数。

## 快捷导入

为方便使用，本模块从子模块导入了部分内容，以下内容可以直接通过本模块导入:

- `on` => {ref}``on` <nonebot.plugin.on.on>`
- `on_metaevent` => {ref}``on_metaevent` <nonebot.plugin.on.on_metaevent>`
- `on_message` => {ref}``on_message` <nonebot.plugin.on.on_message>`
- `on_notice` => {ref}``on_notice` <nonebot.plugin.on.on_notice>`
- `on_request` => {ref}``on_request` <nonebot.plugin.on.on_request>`
- `on_startswith` => {ref}``on_startswith` <nonebot.plugin.on.on_startswith>`
- `on_endswith` => {ref}``on_endswith` <nonebot.plugin.on.on_endswith>`
- `on_keyword` => {ref}``on_keyword` <nonebot.plugin.on.on_keyword>`
- `on_command` => {ref}``on_command` <nonebot.plugin.on.on_command>`
- `on_shell_command` => {ref}``on_shell_command` <nonebot.plugin.on.on_shell_command>`
- `on_regex` => {ref}``on_regex` <nonebot.plugin.on.on_regex>`
- `CommandGroup` => {ref}``CommandGroup` <nonebot.plugin.on.CommandGroup>`
- `Matchergroup` => {ref}``MatcherGroup` <nonebot.plugin.on.MatcherGroup>`
- `load_plugin` => {ref}``load_plugin` <nonebot.plugin.load.load_plugin>`
- `load_plugins` => {ref}``load_plugins` <nonebot.plugin.load.load_plugins>`
- `load_all_plugins` => {ref}``load_all_plugins` <nonebot.plugin.load.load_all_plugins>`
- `load_from_json` => {ref}``load_from_json` <nonebot.plugin.load.load_from_json>`
- `load_from_toml` => {ref}``load_from_toml` <nonebot.plugin.load.load_from_toml>`
- `load_builtin_plugin` => {ref}``load_builtin_plugin` <nonebot.plugin.load.load_builtin_plugin>`
- `load_builtin_plugins` => {ref}``load_builtin_plugins` <nonebot.plugin.load.load_builtin_plugins>`
- `get_plugin` => {ref}``get_plugin` <nonebot.plugin.plugin.get_plugin>`
- `get_loaded_plugins` => {ref}``get_loaded_plugins` <nonebot.plugin.plugin.get_loaded_plugins>`
- `export` => {ref}``export` <nonebot.plugin.export.export>`
- `require` => {ref}``require` <nonebot.plugin.load.require>`

FrontMatter:
    sidebar_position: 0
    description: nonebot.plugin 模块
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
from .load import load_builtin_plugin as load_builtin_plugin
from .plugin import get_loaded_plugins as get_loaded_plugins
from .load import load_builtin_plugins as load_builtin_plugins
