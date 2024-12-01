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
- `on_fullmatch` => {ref}``on_fullmatch` <nonebot.plugin.on.on_fullmatch>`
- `on_keyword` => {ref}``on_keyword` <nonebot.plugin.on.on_keyword>`
- `on_command` => {ref}``on_command` <nonebot.plugin.on.on_command>`
- `on_shell_command` => {ref}``on_shell_command` <nonebot.plugin.on.on_shell_command>`
- `on_regex` => {ref}``on_regex` <nonebot.plugin.on.on_regex>`
- `on_type` => {ref}``on_type` <nonebot.plugin.on.on_type>`
- `CommandGroup` => {ref}``CommandGroup` <nonebot.plugin.on.CommandGroup>`
- `Matchergroup` => {ref}``MatcherGroup` <nonebot.plugin.on.MatcherGroup>`
- `load_plugin` => {ref}``load_plugin` <nonebot.plugin.load.load_plugin>`
- `load_plugins` => {ref}``load_plugins` <nonebot.plugin.load.load_plugins>`
- `load_all_plugins` => {ref}``load_all_plugins` <nonebot.plugin.load.load_all_plugins>`
- `load_from_json` => {ref}``load_from_json` <nonebot.plugin.load.load_from_json>`
- `load_from_toml` => {ref}``load_from_toml` <nonebot.plugin.load.load_from_toml>`
- `load_builtin_plugin` =>
  {ref}``load_builtin_plugin` <nonebot.plugin.load.load_builtin_plugin>`
- `load_builtin_plugins` =>
  {ref}``load_builtin_plugins` <nonebot.plugin.load.load_builtin_plugins>`
- `require` => {ref}``require` <nonebot.plugin.load.require>`
- `PluginMetadata` => {ref}``PluginMetadata` <nonebot.plugin.model.PluginMetadata>`

FrontMatter:
    mdx:
        format: md
    sidebar_position: 0
    description: nonebot.plugin 模块
"""

from contextvars import ContextVar
from itertools import chain
from types import ModuleType
from typing import Optional, TypeVar

from pydantic import BaseModel

from nonebot import get_driver
from nonebot.compat import model_dump, type_validate_python

C = TypeVar("C", bound=BaseModel)

_plugins: dict[str, "Plugin"] = {}
_managers: list["PluginManager"] = []
_current_plugin: ContextVar[Optional["Plugin"]] = ContextVar(
    "_current_plugin", default=None
)


def _module_name_to_plugin_name(module_name: str) -> str:
    return module_name.rsplit(".", 1)[-1]


def _controlled_modules() -> dict[str, str]:
    return {
        plugin_id: module_name
        for manager in _managers
        for plugin_id, module_name in manager.controlled_modules.items()
    }


def _find_parent_plugin_id(
    module_name: str, controlled_modules: Optional[dict[str, str]] = None
) -> Optional[str]:
    if controlled_modules is None:
        controlled_modules = _controlled_modules()
    available = {
        module_name: plugin_id for plugin_id, module_name in controlled_modules.items()
    }
    while "." in module_name:
        module_name, _ = module_name.rsplit(".", 1)
        if module_name in available:
            return available[module_name]


def _module_name_to_plugin_id(
    module_name: str, controlled_modules: Optional[dict[str, str]] = None
) -> str:
    plugin_name = _module_name_to_plugin_name(module_name)
    if parent_plugin_id := _find_parent_plugin_id(module_name, controlled_modules):
        return f"{parent_plugin_id}:{plugin_name}"
    return plugin_name


def _new_plugin(
    module_name: str, module: ModuleType, manager: "PluginManager"
) -> "Plugin":
    plugin_id = _module_name_to_plugin_id(module_name)
    if plugin_id in _plugins:
        raise RuntimeError(
            f"Plugin {plugin_id} already exists! Check your plugin name."
        )

    parent_plugin_id = _find_parent_plugin_id(module_name)
    if parent_plugin_id is not None and parent_plugin_id not in _plugins:
        raise RuntimeError(
            f"Parent plugin {parent_plugin_id} must "
            f"be loaded before loading {plugin_id}."
        )
    parent_plugin = _plugins[parent_plugin_id] if parent_plugin_id is not None else None

    plugin = Plugin(
        name=_module_name_to_plugin_name(module_name),
        module=module,
        module_name=module_name,
        manager=manager,
        parent_plugin=parent_plugin,
    )
    if parent_plugin:
        parent_plugin.sub_plugins.add(plugin)

    _plugins[plugin_id] = plugin
    return plugin


def _revert_plugin(plugin: "Plugin") -> None:
    if plugin.id_ not in _plugins:
        raise RuntimeError("Plugin not found!")
    del _plugins[plugin.id_]
    if parent_plugin := plugin.parent_plugin:
        parent_plugin.sub_plugins.discard(plugin)


def get_plugin(plugin_id: str) -> Optional["Plugin"]:
    """获取已经导入的某个插件。

    如果为 `load_plugins` 文件夹导入的插件，则为文件(夹)名。

    如果为嵌套的子插件，标识符为 `父插件标识符:子插件文件(夹)名`。

    参数:
        plugin_id: 插件标识符，即 {ref}`nonebot.plugin.model.Plugin.id_`。
    """
    return _plugins.get(plugin_id)


def get_plugin_by_module_name(module_name: str) -> Optional["Plugin"]:
    """通过模块名获取已经导入的某个插件。

    如果提供的模块名为某个插件的子模块，同样会返回该插件。

    参数:
        module_name: 模块名，即 {ref}`nonebot.plugin.model.Plugin.module_name`。
    """
    loaded = {plugin.module_name: plugin for plugin in _plugins.values()}
    has_parent = True
    while has_parent:
        if module_name in loaded:
            return loaded[module_name]
        module_name, *has_parent = module_name.rsplit(".", 1)


def get_loaded_plugins() -> set["Plugin"]:
    """获取当前已导入的所有插件。"""
    return set(_plugins.values())


def get_available_plugin_names() -> set[str]:
    """获取当前所有可用的插件标识符（包含尚未加载的插件）。"""
    return {*chain.from_iterable(manager.available_plugins for manager in _managers)}


def get_plugin_config(config: type[C]) -> C:
    """从全局配置获取当前插件需要的配置项。"""
    return type_validate_python(config, model_dump(get_driver().config))


from .load import inherit_supported_adapters as inherit_supported_adapters
from .load import load_all_plugins as load_all_plugins
from .load import load_builtin_plugin as load_builtin_plugin
from .load import load_builtin_plugins as load_builtin_plugins
from .load import load_from_json as load_from_json
from .load import load_from_toml as load_from_toml
from .load import load_plugin as load_plugin
from .load import load_plugins as load_plugins
from .load import require as require
from .manager import PluginManager
from .model import Plugin as Plugin
from .model import PluginMetadata as PluginMetadata
from .on import CommandGroup as CommandGroup
from .on import MatcherGroup as MatcherGroup
from .on import on as on
from .on import on_command as on_command
from .on import on_endswith as on_endswith
from .on import on_fullmatch as on_fullmatch
from .on import on_keyword as on_keyword
from .on import on_message as on_message
from .on import on_metaevent as on_metaevent
from .on import on_notice as on_notice
from .on import on_regex as on_regex
from .on import on_request as on_request
from .on import on_shell_command as on_shell_command
from .on import on_startswith as on_startswith
from .on import on_type as on_type
