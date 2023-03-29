---
sidebar_position: 1
description: 存储数据文件到本地
---

# 数据存储

在使用插件的过程中，难免会需要存储一些持久化数据，例如用户的个人信息、群组的信息等。除了使用数据库等第三方存储之外，还可以使用本地文件来自行管理数据。NoneBot 提供了 `nonebot-plugin-localstore` 插件，可用于获取正确的数据存储路径并写入数据。

## 安装插件

在使用前请先安装 `nonebot-plugin-localstore` 插件至项目环境中，可参考[获取商店插件](../tutorial/store.mdx#安装插件)来了解并选择安装插件的方式。如：

在**项目目录**下执行以下命令：

```bash
nb plugin install nonebot-plugin-localstore
```

## 使用插件

`nonebot-plugin-localstore` 插件兼容 Windows、Linux 和 macOS 等操作系统，使用时无需关心操作系统的差异。同时插件提供 `nb-cli` 脚本，可以使用 `nb localstore` 命令来检查数据存储路径。

在使用本插件前同样需要使用 `require` 方法进行**加载**并**导入**需要使用的方法，可参考 [跨插件访问](../advanced/requiring.md) 一节进行了解，如：

```python
from nonebot import require

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store

# 获取插件缓存目录
cache_dir = store.get_cache_dir("plugin_name")
# 获取插件缓存文件
cache_file = store.get_cache_file("plugin_name", "file_name")
# 获取插件数据目录
data_dir = store.get_data_dir("plugin_name")
# 获取插件数据文件
data_file = store.get_data_file("plugin_name", "file_name")
# 获取插件配置目录
config_dir = store.get_config_dir("plugin_name")
# 获取插件配置文件
config_file = store.get_config_file("plugin_name", "file_name")
```

:::danger 警告
在 Windows 和 macOS 系统下，插件的数据目录和配置目录是同一个目录，因此在使用时需要注意避免文件名冲突。
:::

插件提供的方法均返回一个 `pathlib.Path` 路径，可以参考 [pathlib 文档](https://docs.python.org/zh-cn/3/library/pathlib.html)来了解如何使用。常用的方法有：

```python
from pathlib import Path

data_file = store.get_data_file("plugin_name", "file_name")
# 写入文件内容
data_file.write_text("Hello World!")
# 读取文件内容
data = data_file.read_text()
```
