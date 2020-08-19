# NoneBot.config 模块


### _class_ `BaseConfig(_env_file='<objectobject>', _env_file_encoding=None)`

基类：`pydantic.env_settings.BaseSettings`


### _class_ `Env(_env_file='<objectobject>', _env_file_encoding=None, *, environment='prod')`

基类：`pydantic.env_settings.BaseSettings`


### _class_ `Config(_env_file='<objectobject>', _env_file_encoding=None, *, driver='nonebot.drivers.fastapi', host=IPv4Address('127.0.0.1'), port=8080, secret=None, debug=False, api_root={}, api_timeout=60.0, access_token=None, superusers={}, nickname='', command_start={'/'}, command_sep={'.'}, session_expire_timeout=datetime.timedelta(seconds=120), **values)`

基类：[`nonebot.config.BaseConfig`](#nonebot.config.BaseConfig)

NoneBot Config Object

configs:

### driver


* 类型: str


* 默认值: "nonebot.drivers.fastapi"


* 说明:
nonebot 运行使用后端框架封装 Driver 。继承自 nonebot.driver.BaseDriver 。
