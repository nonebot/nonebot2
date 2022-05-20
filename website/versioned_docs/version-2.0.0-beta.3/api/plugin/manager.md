---
sidebar_position: 5
description: nonebot.plugin.manager 模块
---

# nonebot.plugin.manager

本模块实现插件加载流程。

参考: [import hooks](https://docs.python.org/3/reference/import.html#import-hooks), [PEP302](https://www.python.org/dev/peps/pep-0302/)

## _class_ `PluginManager(plugins=None, search_path=None)` {#PluginManager}

- **参数**

  - `plugins` (Iterable[str] | None)

  - `search_path` (Iterable[str] | None)

### _method_ `list_plugins(self)` {#PluginManager-list_plugins}

- **返回**

  - set[str]

### _method_ `load_all_plugins(self)` {#PluginManager-load_all_plugins}

- **返回**

  - set[[Plugin](./plugin.md#Plugin)]

### _method_ `load_plugin(self, name)` {#PluginManager-load_plugin}

- **参数**

  - `name` (str)

- **返回**

  - [Plugin](./plugin.md#Plugin) | None

## _class_ `PluginFinder()` {#PluginFinder}

### _method_ `find_spec(self, fullname, path, target=None)` {#PluginFinder-find_spec}

- **参数**

  - `fullname` (str)

  - `path` (Sequence[bytes | str] | None)

  - `target` (module | None)

- **返回**

  - Unknown

## _class_ `PluginLoader(manager, fullname, path)` {#PluginLoader}

- **参数**

  - `manager` ([PluginManager](#PluginManager))

  - `fullname` (str)

  - `path`

### _method_ `create_module(self, spec)` {#PluginLoader-create_module}

- **参数**

  - `spec`

- **返回**

  - module | None

### _method_ `exec_module(self, module)` {#PluginLoader-exec_module}

- **参数**

  - `module` (module)

- **返回**

  - None
