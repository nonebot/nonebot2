# 基本配置

到目前为止我们还在使用 NoneBot 的默认行为，在开始编写自己的插件之前，我们先尝试在配置文件上动动手脚，让 NoneBot 表现出不同的行为。

在上一章节中，我们创建了默认的项目结构，其中 `.env`, `.env.*` 均为项目的配置文件，下面将介绍几种 NoneBot 配置方式。

:::danger 警告
请勿将敏感信息写入配置文件并提交至开源仓库！
:::

## .env 文件

NoneBot 在启动时将会从系统环境变量或者 `.env` 文件中寻找变量 `ENVIRONMENT` (大小写不敏感)，默认值为 `prod`。  
这将引导 NoneBot 从系统环境变量或者 `.env.{ENVIRONMENT}` 文件中进一步加载具体配置。

现在，我们在 `.env` 文件中写入当前环境信息

```bash
# .env
ENVIRONMENT=dev
```

## .env.\* 文件

详细配置文件，使用 [pydantic](https://pydantic-docs.helpmanual.io/) 加载配置。在 NoneBot 初始化时可以指定忽略 `.env` 中的环境信息转而加载某个配置文件: `nonebot.init(_env_file=".env.dev")`。

:::warning 提示
由于 `pydantic` 使用 JSON 加载配置项，请确保配置项值为 JSON 能够解析的数据。如果 JSON 解析失败将作为字符串处理。
:::

示例及说明：

```bash
HOST=0.0.0.0  # 配置 NoneBot 监听的 IP/主机名
PORT=8080  # 配置 NoneBot 监听的端口
DEBUG=true  # 开启 debug 模式 **请勿在生产环境开启**
SUPERUSERS=["123456789", "987654321"]  # 配置 NoneBot 超级用户
NICKNAME=["awesome", "bot"]  # 配置机器人的昵称
COMMAND_START=["/", ""]  # 配置命令起始字符
COMMAND_SEP=["."]  # 配置命令分割字符

# Custom Configs
CUSTOM_CONFIG1="config in env file"
CUSTOM_CONFIG2=  # 留空则从系统环境变量读取，如不存在则为空字符串
```

详细的配置项参考 [Config Reference](../api/config.md) 。

## 系统环境变量

如果在系统环境变量中定义了配置，则一样会被读取。

## bot.py 文件

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

## 优先级

`bot.py init` > `system env` > `env file`
