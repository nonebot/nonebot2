import sys
import pkgutil
import importlib
from pathlib import Path
from itertools import chain
from types import ModuleType
from importlib.abc import MetaPathFinder
from importlib.machinery import PathFinder, SourceFileLoader
from typing import Set, Dict, List, Union, Iterable, Optional, Sequence

from nonebot.log import logger
from nonebot.utils import escape_tag
from .plugin import Plugin, _new_plugin
from . import _managers, _current_plugin


class PluginManager:
    def __init__(
        self,
        plugins: Optional[Iterable[str]] = None,
        search_path: Optional[Iterable[str]] = None,
    ):

        # simple plugin not in search path
        self.plugins: Set[str] = set(plugins or [])
        self.search_path: Set[str] = set(search_path or [])
        # cache plugins
        self.searched_plugins: Dict[str, Path] = {}
        self.list_plugins()

    def _path_to_module_name(self, path: Path) -> str:
        rel_path = path.resolve().relative_to(Path(".").resolve())
        if rel_path.stem == "__init__":
            return ".".join(rel_path.parts[:-1])
        else:
            return ".".join(rel_path.parts[:-1] + (rel_path.stem,))

    def _previous_plugins(self) -> List[str]:
        _pre_managers: List[PluginManager]
        if self in _managers:
            _pre_managers = _managers[: _managers.index(self)]
        else:
            _pre_managers = _managers[:]

        return [
            *chain.from_iterable(
                [*manager.plugins, *manager.searched_plugins.keys()]
                for manager in _pre_managers
            )
        ]

    def list_plugins(self) -> Set[str]:
        # get all previous ready to load plugins
        previous_plugins = self._previous_plugins()
        searched_plugins: Dict[str, Path] = {}
        third_party_plugins: Set[str] = set()

        for plugin in self.plugins:
            name = plugin.rsplit(".", 1)[-1] if "." in plugin else plugin
            if name in third_party_plugins or name in previous_plugins:
                raise RuntimeError(
                    f"Plugin already exists: {name}! Check your plugin name"
                )
            third_party_plugins.add(plugin)

        for module_info in pkgutil.iter_modules(self.search_path):
            if module_info.name.startswith("_"):
                continue
            if (
                module_info.name in searched_plugins.keys()
                or module_info.name in previous_plugins
                or module_info.name in third_party_plugins
            ):
                raise RuntimeError(
                    f"Plugin already exists: {module_info.name}! Check your plugin name"
                )
            module_spec = module_info.module_finder.find_spec(module_info.name, None)
            if not module_spec:
                continue
            module_path = module_spec.origin
            if not module_path:
                continue
            searched_plugins[module_info.name] = Path(module_path).resolve()

        self.searched_plugins = searched_plugins

        return third_party_plugins | set(self.searched_plugins.keys())

    def load_plugin(self, name) -> Optional[Plugin]:
        try:
            if name in self.plugins:
                module = importlib.import_module(name)
            elif name not in self.searched_plugins:
                raise RuntimeError(f"Plugin not found: {name}! Check your plugin name")
            else:
                module = importlib.import_module(
                    self._path_to_module_name(self.searched_plugins[name])
                )

            logger.opt(colors=True).success(
                f'Succeeded to import "<y>{escape_tag(name)}</y>"'
            )
            return getattr(module, "__plugin__", None)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f'<r><bg #f8bbd0>Failed to import "{escape_tag(name)}"</bg #f8bbd0></r>'
            )

    def load_all_plugins(self) -> Set[Plugin]:
        return set(
            filter(None, (self.load_plugin(name) for name in self.list_plugins()))
        )


class PluginFinder(MetaPathFinder):
    def find_spec(
        self,
        fullname: str,
        path: Optional[Sequence[Union[bytes, str]]],
        target: Optional[ModuleType] = None,
    ):
        if _managers:
            index = -1
            module_spec = PathFinder.find_spec(fullname, path, target)
            if not module_spec:
                return
            module_origin = module_spec.origin
            if not module_origin:
                return
            module_path = Path(module_origin).resolve()

            while -index <= len(_managers):
                manager = _managers[index]

                if (
                    fullname in manager.plugins
                    or module_path in manager.searched_plugins.values()
                ):
                    module_spec.loader = PluginLoader(manager, fullname, module_origin)
                    return module_spec

                index -= 1
        return


class PluginLoader(SourceFileLoader):
    def __init__(self, manager: PluginManager, fullname: str, path) -> None:
        self.manager = manager
        self.loaded = False
        super().__init__(fullname, path)

    def create_module(self, spec) -> Optional[ModuleType]:
        if self.name in sys.modules:
            self.loaded = True
            return sys.modules[self.name]
        # return None to use default module creation
        return super().create_module(spec)

    def exec_module(self, module: ModuleType) -> None:
        if self.loaded:
            return

        plugin = _new_plugin(self.name, module, self.manager)
        parent_plugin = _current_plugin.get()
        if parent_plugin and _managers.index(parent_plugin.manager) < _managers.index(
            self.manager
        ):
            plugin.parent_plugin = parent_plugin
            parent_plugin.sub_plugins.add(plugin)

        _plugin_token = _current_plugin.set(plugin)

        setattr(module, "__plugin__", plugin)

        # try:
        #     super().exec_module(module)
        # except Exception as e:
        #     raise ImportError(
        #         f"Error when executing module {module_name} from {module.__file__}."
        #     ) from e
        super().exec_module(module)

        _current_plugin.reset(_plugin_token)
        return


sys.meta_path.insert(0, PluginFinder())
