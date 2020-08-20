# NoneBot.config 模块


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

除了 NoneBot 的配置项外，还可以自行添加配置项到 `.env.{environment}` 文件中。这些配置将会一起带入 `Config` 类中。


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
