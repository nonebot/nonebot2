---
mdx:
  format: md
sidebar_position: 5
description: nonebot.plugin.manager 模块
---

# nonebot.plugin.manager

本模块实现插件加载流程。

参考: [import hooks](https://docs.python.org/3/reference/import.html#import-hooks), [PEP302](https://www.python.org/dev/peps/pep-0302/)

## _class_ `PluginManager(plugins=None, search_path=None)` {#PluginManager}

- **说明:** 插件管理器。

- **参数**

  - `plugins` (Iterable[str] | None): 独立插件模块名集合。

  - `search_path` (Iterable[str] | None): 插件搜索路径（文件夹），相对于当前工作目录。

### _property_ `third_party_plugins` {#PluginManager-third-party-plugins}

- **类型:** set[str]

- **说明:** 返回所有独立插件标识符。

### _property_ `searched_plugins` {#PluginManager-searched-plugins}

- **类型:** set[str]

- **说明:** 返回已搜索到的插件标识符。

### _property_ `available_plugins` {#PluginManager-available-plugins}

- **类型:** set[str]

- **说明:** 返回当前插件管理器中可用的插件标识符。

### _property_ `controlled_modules` {#PluginManager-controlled-modules}

- **类型:** dict[str, str]

- **说明:** 返回当前插件管理器中控制的插件标识符与模块路径映射字典。

### _method_ `load_plugin(name)` {#PluginManager-load-plugin}

- **说明**

  加载指定插件。

  可以使用完整插件模块名或者插件标识符加载。

- **参数**

  - `name` (str): 插件名称或插件标识符。

- **返回**

  - [Plugin](model.md#Plugin) | None

### _method_ `load_all_plugins()` {#PluginManager-load-all-plugins}

- **说明:** 加载所有可用插件。

- **参数**

  empty

- **返回**

  - set[[Plugin](model.md#Plugin)]

## _class_ `PluginFinder(<auto>)` {#PluginFinder}

- **参数**

  auto

### _method_ `find_spec(fullname, path, target=None)` {#PluginFinder-find-spec}

- **参数**

  - `fullname` (str)

  - `path` (Sequence[str] | None)

  - `target` (ModuleType | None)

- **返回**

  - untyped

## _class_ `PluginLoader(manager, fullname, path)` {#PluginLoader}

- **参数**

  - `manager` (PluginManager)

  - `fullname` (str)

  - `path` (str)

### _method_ `create_module(spec)` {#PluginLoader-create-module}

- **参数**

  - `spec`

- **返回**

  - ModuleType | None

### _method_ `exec_module(module)` {#PluginLoader-exec-module}

- **参数**

  - `module` (ModuleType)

- **返回**

  - None
