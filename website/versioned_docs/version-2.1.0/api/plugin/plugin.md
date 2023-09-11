---
sidebar_position: 3
description: nonebot.plugin.plugin 模块

slug: /api/plugin/plugin
---

# nonebot.plugin.plugin

本模块定义插件相关信息。

## _class_ `PluginMetadata(<auto>)` {#PluginMetadata}

- **说明:** 插件元信息，由插件编写者提供

- **参数**

  auto

### _instance-var_ `name` {#PluginMetadata-name}

- **类型:** str

- **说明:** 插件名称

### _instance-var_ `description` {#PluginMetadata-description}

- **类型:** str

- **说明:** 插件功能介绍

### _instance-var_ `usage` {#PluginMetadata-usage}

- **类型:** str

- **说明:** 插件使用方法

### _class-var_ `type` {#PluginMetadata-type}

- **类型:** str | None

- **说明:** 插件类型，用于商店分类

### _class-var_ `homepage` {#PluginMetadata-homepage}

- **类型:** str | None

- **说明:** 插件主页

### _class-var_ `config` {#PluginMetadata-config}

- **类型:** type[BaseModel] | None

- **说明:** 插件配置项

### _class-var_ `supported_adapters` {#PluginMetadata-supported-adapters}

- **类型:** set[str] | None

- **说明**

  插件支持的适配器模块路径

  格式为 `<module>[:<Adapter>]`，`~` 为 `nonebot.adapters.` 的缩写。

  `None` 表示支持**所有适配器**。

### _class-var_ `extra` {#PluginMetadata-extra}

- **类型:** dict[Any, Any]

- **说明:** 插件额外信息，可由插件编写者自由扩展定义

### _method_ `get_supported_adapters()` {#PluginMetadata-get-supported-adapters}

- **说明:** 获取当前已安装的插件支持适配器类列表

- **参数**

  empty

- **返回**

  - set[type[[Adapter](../adapters/index.md#Adapter)]] | None

## _class_ `Plugin(<auto>)` {#Plugin}

- **说明:** 存储插件信息

- **参数**

  auto

### _instance-var_ `name` {#Plugin-name}

- **类型:** str

- **说明:** 插件索引标识，NoneBot 使用 文件/文件夹 名称作为标识符

### _instance-var_ `module` {#Plugin-module}

- **类型:** ModuleType

- **说明:** 插件模块对象

### _instance-var_ `module_name` {#Plugin-module-name}

- **类型:** str

- **说明:** 点分割模块路径

### _instance-var_ `manager` {#Plugin-manager}

- **类型:** [PluginManager](manager.md#PluginManager)

- **说明:** 导入该插件的插件管理器

### _class-var_ `matcher` {#Plugin-matcher}

- **类型:** set[type[[Matcher](../matcher.md#Matcher)]]

- **说明:** 插件加载时定义的 `Matcher`

### _class-var_ `parent_plugin` {#Plugin-parent-plugin}

- **类型:** Plugin | None

- **说明:** 父插件

### _class-var_ `sub_plugins` {#Plugin-sub-plugins}

- **类型:** set[Plugin]

- **说明:** 子插件集合
