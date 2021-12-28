---
sidebar_position: 1
description: 项目配置方式与配置项

options:
  menu:
    weight: 21
    category: guide
---

# 配置

在上一章节中，我们创建了默认的项目结构，其中 `.env` 和 `.env.*` 均为项目的配置文件，下面将介绍几种 NoneBot 配置方式以及配置项。

:::danger 警告
请勿将敏感信息写入配置文件并提交至开源仓库！
:::

## 配置方式

### .env 文件

NoneBot 在启动时将会从系统环境变量或者 `.env` 文件中寻找变量 `ENVIRONMENT` (大小写不敏感)，默认值为 `prod`。  
这将引导 NoneBot 从系统环境变量或者 `.env.{ENVIRONMENT}` 文件中进一步加载具体配置。

`.env` 文件是基础环境配置文件，该文件中的配置项在不同环境下都会被加载，但会被 `.env.{ENVIRONMENT}` 文件中的配置所覆盖。

NoneBot 使用 [pydantic](https://pydantic-docs.helpmanual.io/) 进行配置处理，并对 `pydantic` 的行为做出了更改，详见下方说明。

现在，我们在 `.env` 文件中写入当前环境信息：

```bash
# .env
ENVIRONMENT=dev
CUSTOM_CONFIG=common config  # 这个配置项在任何环境中都会被加载
```

如你所想，之后 NoneBot 就会从 `.env.dev` 文件中加载环境变量。

:::important 参考文档
`.env` 相关文件的加载使用 `dotenv` 语法，请参考 [`dotenv` 文档](https://saurabh-kumar.com/python-dotenv/)
:::

:::warning 提示
由于 `pydantic` 使用 JSON 解析配置项，请确保配置项值为 JSON 格式的数据。如：

```bash
list=["123456789", "987654321", 1]
test={"hello": "world"}
```

如果配置项值解析失败将作为 **字符串** 处理。

特别的，如果配置项 **为空** ，则会从 **系统环境变量** 中获取值，如果不存在则为空字符串。
:::

### .env.\* 文件

NoneBot 默认会从 `.env.{ENVIRONMENT}` 文件加载配置，但是可以在 NoneBot 初始化时指定加载某个环境配置文件: `nonebot.init(_env_file=".env.dev")`，这将忽略你在 `.env` 中设置的 `ENVIRONMENT` 。

配置语法与 `.env` 文件相同。

示例及说明：

```bash
HOST=0.0.0.0  # 配置 NoneBot 监听的 IP/主机名
PORT=8080  # 配置 NoneBot 监听的端口
SUPERUSERS=["123456789", "987654321"]  # 配置 NoneBot 超级用户
NICKNAME=["awesome", "bot"]  # 配置机器人的昵称
COMMAND_START=["/", ""]  # 配置命令起始字符
COMMAND_SEP=["."]  # 配置命令分割字符

# Custom Configs
CUSTOM_CONFIG1="config in env file"
CUSTOM_CONFIG2=  # 留空则从系统环境变量读取，如不存在则为空字符串
```

详细的配置项可以参考 [配置项](#详细配置项) 。

### 系统环境变量

如果在系统环境变量中定义了配置，则一样会被读取。

### bot.py 文件

配置项也可以在 NoneBot 初始化时传入。此处可以传入任意合法 Python 变量。当然也可以在初始化完成后修改或新增。

示例：

```python
# bot.py
import nonebot

nonebot.init(custom_config3="config on init")

config = nonebot.get_driver().config
config.custom_config3 = "changed after init"
config.custom_config4 = "new config after init"
```

## 配置优先级

`bot.py` 文件( `nonebot.init` ) > 系统环境变量 > `.env`, `.env.*` 文件

## 读取配置项

配置项可以通过三种类型的对象获取：`driver`, `adapter`, `bot`。

```python
import nonebot
# driver
nonebot.get_driver().config.custom_config
# bot
nonebot.get_bot().config.custom_config
# adapter
nonebot.get_driver()._adapters["adapter_name"].config.custom_config
```

## 详细配置项

配置项的 API 文档可以前往 [Class Config](../api/config.md#class-config) 查看。

### Driver

- **类型**: `str`
- **默认值**: `"~fastapi"`

NoneBot 运行所使用的驱动器。主要分为 `ForwardDriver`, `ReverseDriver` 即客户端和服务端两类。

配置格式采用特殊语法：`<module>[:<Driver>][+<module>[:<Mixin>]]*`

其中 `<module>` 为驱动器模块名，可以使用 `~` 作为 `nonebot.drivers.` 的简写；`<Driver>` 为驱动器类名，默认为 `Driver`；`<Mixin>` 为驱动器混入的类名，默认为 `Mixin`。

NoneBot 内置了几个常用驱动器，包括了各类常用功能，常见驱动器配置如下：

```env
DRIVER=~fastapi
DRIVER=~httpx+~websockets
DRIVER=~fastapi+~httpx+~websockets
DRIVER=~fastapi+~aiohttp
```

各驱动器的功能与区别请参考 [选择驱动器](./choose-driver.md) 。

<!-- TODO -->
