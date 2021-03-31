import sys
import uuid
import pkgutil
import importlib
from hashlib import md5
from types import ModuleType
from collections import Counter
from contextvars import ContextVar
from importlib.abc import MetaPathFinder
from typing import Set, List, Optional, Iterable
from importlib.machinery import PathFinder, SourceFileLoader

from .export import _export, Export

_current_plugin: ContextVar[Optional[str]] = ContextVar("_current_plugin",
                                                        default=None)

_internal_space = ModuleType(__name__ + "._internal")
_internal_space.__path__ = []  # type: ignore
sys.modules[_internal_space.__name__] = _internal_space

_manager_stack: List["PluginManager"] = []


class _NamespaceModule(ModuleType):
    """Simple namespace module to store plugins."""

    @property
    def __path__(self):
        return []

    def __getattr__(self, name: str):
        try:
            return super().__getattr__(name)  # type: ignore
        except AttributeError:
            if name.startswith("__"):
                raise
            raise RuntimeError("Plugin manager not activated!")


class _InternalModule(ModuleType):
    """Internal module for each plugin manager."""

    def __init__(self, prefix: str, plugin_manager: "PluginManager"):
        super().__init__(f"{prefix}.{plugin_manager.internal_id}")
        self.__plugin_manager__ = plugin_manager

    @property
    def __path__(self) -> List[str]:
        return list(self.__plugin_manager__.search_path)


class PluginManager:

    def __init__(self,
                 namespace: Optional[str] = None,
                 plugins: Optional[Iterable[str]] = None,
                 search_path: Optional[Iterable[str]] = None,
                 *,
                 id: Optional[str] = None):
        self.namespace: Optional[str] = namespace
        self.namespace_module: Optional[ModuleType] = self._setup_namespace(
            namespace)

        self.id: str = id or str(uuid.uuid4())
        self.internal_id: str = md5(
            ((self.namespace or "") + self.id).encode()).hexdigest()
        self.internal_module = self._setup_internal_module(self.internal_id)

        # simple plugin not in search path
        self.plugins: Set[str] = set(plugins or [])
        self.search_path: Set[str] = set(search_path or [])
        # ensure can be loaded
        self.list_plugins()

    def _setup_namespace(self,
                         namespace: Optional[str] = None
                        ) -> Optional[ModuleType]:
        if not namespace:
            return None

        try:
            module = importlib.import_module(namespace)
        except ImportError:
            module = _NamespaceModule(namespace)
            if "." in namespace:
                parent = importlib.import_module(namespace.rsplit(".", 1)[0])
                setattr(parent, namespace.rsplit(".", 1)[1], module)

        sys.modules[namespace] = module
        return module

    def _setup_internal_module(self, internal_id: str) -> ModuleType:
        if hasattr(_internal_space, internal_id):
            raise RuntimeError("Plugin manager already exists!")

        prefix = sys._getframe(3).f_globals.get(
            "__name__") or _internal_space.__name__
        if not prefix.startswith(_internal_space.__name__):
            prefix = _internal_space.__name__
        module = _InternalModule(prefix, self)
        sys.modules[module.__name__] = module
        setattr(_internal_space, internal_id, module)
        return module

    def __enter__(self):
        if self in _manager_stack:
            raise RuntimeError("Plugin manager already activated!")
        _manager_stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            _manager_stack.pop()
        except IndexError:
            pass

    def search_plugins(self) -> List[str]:
        return [
            module_info.name
            for module_info in pkgutil.iter_modules(self.search_path)
        ]

    def list_plugins(self) -> Set[str]:
        _pre_managers: List[PluginManager]
        if self in _manager_stack:
            _pre_managers = _manager_stack[:_manager_stack.index(self)]
        else:
            _pre_managers = _manager_stack[:]

        _search_path: Set[str] = set()
        for manager in _pre_managers:
            _search_path |= manager.search_path
        if _search_path & self.search_path:
            raise RuntimeError("Duplicate plugin search path!")

        _search_plugins = self.search_plugins()
        c = Counter([*_search_plugins, *self.plugins])
        conflict = [name for name, num in c.items() if num > 1]
        if conflict:
            raise RuntimeError(
                f"More than one plugin named {' / '.join(conflict)}!")
        return set(_search_plugins) | self.plugins

    def load_plugin(self, name) -> ModuleType:
        if name in self.plugins:
            with self:
                return importlib.import_module(name)

        if "." in name:
            raise ValueError("Plugin name cannot contain '.'")

        with self:
            return importlib.import_module(f"{self.namespace}.{name}")

    def load_all_plugins(self) -> List[ModuleType]:
        return [self.load_plugin(name) for name in self.list_plugins()]

    def _rewrite_module_name(self, module_name) -> Optional[str]:
        prefix = f"{self.internal_module.__name__}."
        if module_name.startswith(self.namespace + "."):
            path = module_name.split(".")
            length = self.namespace.count(".") + 1
            return f"{prefix}{'.'.join(path[length:])}"
        elif module_name in self.plugins or module_name.startswith(prefix):
            return module_name
        elif module_name in self.search_plugins():
            return f"{prefix}{module_name}"
        return None


class PluginFinder(MetaPathFinder):

    def find_spec(self, fullname: str, path, target):
        if _manager_stack:
            index = -1
            while -index <= len(_manager_stack):
                manager = _manager_stack[index]
                newname = manager._rewrite_module_name(fullname)
                if newname:
                    spec = PathFinder.find_spec(
                        newname, [*manager.search_path, *(path or [])], target)
                    if spec:
                        spec.loader = PluginLoader(manager, newname,
                                                   spec.origin)
                        return spec
                index -= 1
        return None


class PluginLoader(SourceFileLoader):

    def __init__(self, manager: PluginManager, fullname: str, path) -> None:
        self.manager = manager
        self.loaded = False
        self._plugin_token = None
        self._export_token = None
        super().__init__(fullname, path)

    def create_module(self, spec) -> Optional[ModuleType]:
        if self.name in sys.modules:
            self.loaded = True
            return sys.modules[self.name]
        prefix = self.manager.internal_module.__name__
        plugin_name = self.name[len(prefix):] if self.name.startswith(
            prefix) else self.name
        self._plugin_token = _current_plugin.set(plugin_name.lstrip("."))
        self._export_token = _export.set(Export())
        # return None to use default module creation
        return super().create_module(spec)

    def exec_module(self, module: ModuleType) -> None:
        if self.loaded:
            return
        # really need?
        # setattr(module, "__manager__", self.manager)
        if self._export_token:
            setattr(module, "__export__", _export.get())

        super().exec_module(module)

        if self._plugin_token:
            _current_plugin.reset(self._plugin_token)
        if self._export_token:
            _export.reset(self._export_token)
        return


sys.meta_path.insert(0, PluginFinder())
