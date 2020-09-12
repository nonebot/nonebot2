---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.config 模块

## 配置

NoneBot 使用 [pydantic](https://pydantic-docs.helpmanual.io/) 以及 [python-dotenv](https://saurabh-kumar.com/python-dotenv/) 来读取配置。

配置项需符合特殊格式或 json 序列化格式。详情见 [pydantic Field Type](https://pydantic-docs.helpmanual.io/usage/types/) 文档。


## _class_ `Env`

基类：`pydantic.env_settings.BaseSettings`

运行环境配置。大小写不敏感。

将会从 `nonebot.init 参数` > `环境变量` > `.env 环境配置文件` 的优先级读取配置。


### `environment`


* 类型: `str`


* 默认值: `"prod"`


* 说明:
当前环境名。 NoneBot 将从 `.env.{environment}` 文件中加载配置。


## _class_ `Config`

基类：`nonebot.config.BaseConfig`

NoneBot 主要配置。大小写不敏感。

除了 NoneBot 的配置项外，还可以自行添加配置项到 `.env.{environment}` 文件中。
这些配置将会在 json 反序列化后一起带入 `Config` 类中。


### `driver`


* 类型: `str`


* 默认值: `"nonebot.drivers.fastapi"`


* 说明:
NoneBot 运行所使用的 `Driver` 。继承自 `nonebot.driver.BaseDriver` 。


### `host`


* 类型: `IPvAnyAddress`


* 默认值: `127.0.0.1`


* 说明:
NoneBot 的 HTTP 和 WebSocket 服务端监听的 IP／主机名。


### `port`


* 类型: `int`


* 默认值: `8080`


* 说明:
NoneBot 的 HTTP 和 WebSocket 服务端监听的端口。


### `secret`


* 类型: `Optional[str]`


* 默认值: `None`


* 说明:
上报连接 NoneBot 所需的密钥。


* 示例:

```http
POST /cqhttp/ HTTP/1.1
Authorization: Bearer kSLuTF2GC2Q4q4ugm3
```


### `debug`


* 类型: `bool`


* 默认值: `False`


* 说明:
是否以调试模式运行 NoneBot。


### `api_root`


* 类型: `Dict[str, str]`


* 默认值: `{}`


* 说明:
以机器人 ID 为键，上报地址为值的字典，环境变量或文件中应使用 json 序列化。


* 示例:

```plain
API_ROOT={"123456": "http://127.0.0.1:5700"}
```


### `api_timeout`


* 类型: `Optional[float]`


* 默认值: `30.`


* 说明:
API 请求超时时间，单位: 秒。


### `access_token`


* 类型: `Optional[str]`


* 默认值: `None`


* 说明:
API 请求所需密钥，会在调用 API 时在请求头中携带。


### `superusers`


* 类型: `Set[int]`


* 默认值: `set()`


* 说明:
机器人超级用户。


* 示例:

```plain
SUPER_USERS=[12345789]
```


### `nickname`


* 类型: `Union[str, Set[str]]`


* 默认值: `""`


* 说明:
机器人昵称。


### `command_start`


* 类型: `Set[str]`


* 默认值: `{"/"}`


* 说明:
命令的起始标记，用于判断一条消息是不是命令。


### `command_sep`


* 类型: `Set[str]`


* 默认值: `{"."}`


* 说明:
命令的分隔标记，用于将文本形式的命令切分为元组（实际的命令名）。


### `session_expire_timeout`


* 类型: `timedelta`


* 默认值: `timedelta(minutes=2)`


* 说明:
等待用户回复的超时时间。


* 示例:

```plain
SESSION_EXPIRE_TIMEOUT=120  # 单位: 秒
SESSION_EXPIRE_TIMEOUT=[DD ][HH:MM]SS[.ffffff]
SESSION_EXPIRE_TIMEOUT=P[DD]DT[HH]H[MM]M[SS]S  # ISO 8601
```


### `apscheduler_config`


* 类型: `dict`


* 默认值: `{"apscheduler.timezone": "Asia/Shanghai"}`


* 说明:
APScheduler 的配置对象，见 [Configuring the Scheduler](https://apscheduler.readthedocs.io/en/latest/userguide.html#configuring-the-scheduler)
