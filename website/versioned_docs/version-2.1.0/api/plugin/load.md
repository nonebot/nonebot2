---
sidebar_position: 1
description: nonebot.plugin.load 模块
---

# nonebot.plugin.load

本模块定义插件加载接口。

## _def_ `load_plugin(module_path)` {#load-plugin}

- **说明:** 加载单个插件，可以是本地插件或是通过 `pip` 安装的插件。

- **参数**

  - `module_path` (str | Path): 插件名称 `path.to.your.plugin` 或插件路径 `pathlib.Path(path/to/your/plugin)`

- **返回**

  - [Plugin](plugin.md#Plugin) | None

## _def_ `load_plugins(*plugin_dir)` {#load-plugins}

- **说明:** 导入文件夹下多个插件，以 `_` 开头的插件不会被导入!

- **参数**

  - `*plugin_dir` (str): 文件夹路径

- **返回**

  - set[[Plugin](plugin.md#Plugin)]

## _def_ `load_all_plugins(module_path, plugin_dir)` {#load-all-plugins}

- **说明:** 导入指定列表中的插件以及指定目录下多个插件，以 `_` 开头的插件不会被导入!

- **参数**

  - `module_path` (Iterable[str]): 指定插件集合

  - `plugin_dir` (Iterable[str]): 指定文件夹路径集合

- **返回**

  - set[[Plugin](plugin.md#Plugin)]

## _def_ `load_from_json(file_path, encoding="utf-8")` {#load-from-json}

- **说明:** 导入指定 json 文件中的 `plugins` 以及 `plugin_dirs` 下多个插件。 以 `_` 开头的插件不会被导入!

- **参数**

  - `file_path` (str): 指定 json 文件路径

  - `encoding` (str): 指定 json 文件编码

- **返回**

  - set[[Plugin](plugin.md#Plugin)]

- **用法**

  ```json title=plugins.json
  {
    "plugins": ["some_plugin"],
    "plugin_dirs": ["some_dir"]
  }
  ```

  ```python
  nonebot.load_from_json("plugins.json")
  ```

## _def_ `load_from_toml(file_path, encoding="utf-8")` {#load-from-toml}

- **说明:** 导入指定 toml 文件 `[tool.nonebot]` 中的 `plugins` 以及 `plugin_dirs` 下多个插件。 以 `_` 开头的插件不会被导入!

- **参数**

  - `file_path` (str): 指定 toml 文件路径

  - `encoding` (str): 指定 toml 文件编码

- **返回**

  - set[[Plugin](plugin.md#Plugin)]

- **用法**

  ```toml title=pyproject.toml
  [tool.nonebot]
  plugins = ["some_plugin"]
  plugin_dirs = ["some_dir"]
  ```

  ```python
  nonebot.load_from_toml("pyproject.toml")
  ```

## _def_ `load_builtin_plugin(name)` {#load-builtin-plugin}

- **说明:** 导入 NoneBot 内置插件。

- **参数**

  - `name` (str): 插件名称

- **返回**

  - [Plugin](plugin.md#Plugin) | None

## _def_ `load_builtin_plugins(*plugins)` {#load-builtin-plugins}

- **说明:** 导入多个 NoneBot 内置插件。

- **参数**

  - `*plugins` (str): 插件名称列表

- **返回**

  - set[[Plugin](plugin.md#Plugin)]

## _def_ `require(name)` {#require}

- **说明**

  获取一个插件的导出内容。

  如果为 `load_plugins` 文件夹导入的插件，则为文件(夹)名。

- **参数**

  - `name` (str): 插件名，即 [Plugin.name](plugin.md#Plugin-name)。

- **返回**

  - ModuleType

- **异常**

  - RuntimeError: 插件无法加载

## _def_ `inherit_supported_adapters(*names)` {#inherit-supported-adapters}

- **说明**

  获取已加载插件的适配器支持状态集合。

  如果传入了多个插件名称，返回值会自动取交集。

- **参数**

  - `*names` (str): 插件名称列表。

- **返回**

  - set[str] | None

- **异常**

  - RuntimeError: 插件未加载

  - ValueError: 插件缺少元数据
