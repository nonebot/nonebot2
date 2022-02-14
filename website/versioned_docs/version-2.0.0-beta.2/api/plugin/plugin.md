---
sidebar_position: 3
description: nonebot.plugin.plugin 模块
---

# nonebot.plugin.plugin

本模块定义插件对象。

## _var_ `plugins` {#plugins}

- **类型:** dict[str, Plugin]

- **说明:** 已加载的插件

## _class_ `Plugin(name, module, module_name, manager, export=<factory>, matcher=<factory>, parent_plugin=None, sub_plugins=<factory>)` {#Plugin}

- **说明**

  存储插件信息

- **参数**

  - `name` (str)

  - `module` (module)

  - `module_name` (str)

  - `manager` (PluginManager)

  - `export` ([Export](./export.md#Export))

  - `matcher` (set[Type[nonebot.internal.matcher.Matcher]])

  - `parent_plugin` (Plugin | None)

  - `sub_plugins` (set[Plugin])

### _class-var_ `parent_plugin` {#Plugin-parent_plugin}

- **类型:** Plugin | None

- **说明:** 父插件

### _instance-var_ `name` {#Plugin-name}

- **类型:** str

- **说明:** 插件名称，使用 文件/文件夹 名称作为插件名

### _instance-var_ `module` {#Plugin-module}

- **类型:** module

- **说明:** 插件模块对象

### _instance-var_ `module_name` {#Plugin-module_name}

- **类型:** str

- **说明:** 点分割模块路径

### _instance-var_ `manager` {#Plugin-manager}

- **类型:** PluginManager

- **说明:** 导入该插件的插件管理器

### _instance-var_ `export` {#Plugin-export}

- **类型:** nonebot.plugin.export.Export

- **说明:** 插件内定义的导出内容

### _instance-var_ `matcher` {#Plugin-matcher}

- **类型:** set[Type[nonebot.internal.matcher.Matcher]]

- **说明:** 插件内定义的 `Matcher`

### _instance-var_ `sub_plugins` {#Plugin-sub_plugins}

- **类型:** set[Plugin]

- **说明:** 子插件集合

## _def_ `get_plugin(name)` {#get_plugin}

- **说明**

  获取已经导入的某个插件。

  如果为 `load_plugins` 文件夹导入的插件，则为文件(夹)名。

- **参数**

  - `name` (str): 插件名，即 [Plugin.name](#Plugin-name)。

- **返回**

  - [Plugin](#Plugin) | None

## _def_ `get_loaded_plugins()` {#get_loaded_plugins}

- **说明**

  获取当前已导入的所有插件。

- **返回**

  - set[[Plugin](#Plugin)]
