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
cache_dir = store.get_plugin_cache_dir()
# 获取插件缓存文件
cache_file = store.get_plugin_cache_file("file_name")
# 获取插件数据目录
data_dir = store.get_plugin_data_dir()
# 获取插件数据文件
data_file = store.get_plugin_data_file("file_name")
# 获取插件配置目录
config_dir = store.get_plugin_config_dir()
# 获取插件配置文件
config_file = store.get_plugin_config_file("file_name")
```

:::danger 警告
在 Windows 和 macOS 系统下，插件的数据目录和配置目录是同一个目录，因此在使用时需要注意避免文件名冲突。
:::

插件提供的方法均返回一个 `pathlib.Path` 路径，可以参考 [pathlib 文档](https://docs.python.org/zh-cn/3/library/pathlib.html)来了解如何使用。常用的方法有：

```python
from pathlib import Path

data_file = store.get_plugin_data_file("file_name")
# 写入文件内容
data_file.write_text("Hello World!")
# 读取文件内容
data = data_file.read_text()
```

:::note 提示

对于嵌套插件，子插件的存储目录将位于父插件存储目录下。

:::

## 配置项

### localstore_use_cwd

使用当前工作目录作为数据存储目录，以下数据目录配置项默认值将会对应变更

默认值：`False`

```dotenv
LOCALSTORE_USE_CWD=true
```

### localstore_cache_dir

自定义缓存目录

默认值：

当 `localstore_use_cwd` 为 `True` 时，缓存目录为 `<current_working_directory>/cache`，否则：

- macOS: `~/Library/Caches/nonebot2`
- Unix: `~/.cache/nonebot2` (XDG default)
- Windows: `C:\Users\<username>\AppData\Local\nonebot2\Cache`

```dotenv
LOCALSTORE_CACHE_DIR=/tmp/cache
```

### localstore_data_dir

自定义数据目录

默认值：

当 `localstore_use_cwd` 为 `True` 时，数据目录为 `<current_working_directory>/data`，否则：

- macOS: `~/Library/Application Support/nonebot2`
- Unix: `~/.local/share/nonebot2` or in $XDG_DATA_HOME, if defined
- Win XP (not roaming): `C:\Documents and Settings\<username>\Application Data\nonebot2`
- Win 7 (not roaming): `C:\Users\<username>\AppData\Local\nonebot2`

```dotenv
LOCALSTORE_DATA_DIR=/tmp/data
```

### localstore_config_dir

自定义配置目录

默认值：

当 `localstore_use_cwd` 为 `True` 时，配置目录为 `<current_working_directory>/config`，否则：

- macOS: same as user_data_dir
- Unix: `~/.config/nonebot2`
- Win XP (roaming): `C:\Documents and Settings\<username>\Local Settings\Application Data\nonebot2`
- Win 7 (roaming): `C:\Users\<username>\AppData\Roaming\nonebot2`

```dotenv
LOCALSTORE_CONFIG_DIR=/tmp/config
```

### localstore_plugin_cache_dir

自定义插件缓存目录

默认值：`{}`

```dotenv
LOCALSTORE_PLUGIN_CACHE_DIR='
{
  "plugin_id": "/tmp/plugin_cache"
}
'
```

### localstore_plugin_data_dir

自定义插件数据目录

默认值：`{}`

```dotenv
LOCALSTORE_PLUGIN_DATA_DIR='
{
  "plugin_id": "/tmp/plugin_data"
}
'
```

### localstore_plugin_config_dir

自定义插件配置目录

默认值：`{}`

```dotenv
LOCALSTORE_PLUGIN_CONFIG_DIR='
{
  "plugin_id": "/tmp/plugin_config"
}
'
```
