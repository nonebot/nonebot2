"""本模块定义了 NoneBot 本身运行所需的配置项。

NoneBot 使用 [`pydantic`](https://pydantic-docs.helpmanual.io/) 以及
[`python-dotenv`](https://saurabh-kumar.com/python-dotenv/) 来读取配置。

配置项需符合特殊格式或 json 序列化格式
详情见 [`pydantic Field Type`](https://pydantic-docs.helpmanual.io/usage/types/) 文档。

FrontMatter:
    sidebar_position: 1
    description: nonebot.config 模块
"""

import os
from datetime import timedelta
from ipaddress import IPv4Address
from typing import TYPE_CHECKING, Any, Set, Dict, Tuple, Union, Mapping, Optional

from pydantic.utils import deep_update
from pydantic.fields import Undefined, UndefinedType
from pydantic import Extra, Field, BaseSettings, IPvAnyAddress
from pydantic.env_settings import (
    DotenvType,
    SettingsError,
    EnvSettingsSource,
    InitSettingsSource,
    SettingsSourceCallable,
)

from nonebot.log import logger


class CustomEnvSettings(EnvSettingsSource):
    def __call__(self, settings: BaseSettings) -> Dict[str, Any]:
        """从环境变量和 dotenv 配置文件中读取配置项。"""

        d: Dict[str, Any] = {}

        if settings.__config__.case_sensitive:
            env_vars: Mapping[str, Optional[str]] = os.environ  # pragma: no cover
        else:
            env_vars = {k.lower(): v for k, v in os.environ.items()}

        env_file_vars = self._read_env_files(settings.__config__.case_sensitive)
        env_vars = {**env_file_vars, **env_vars}

        for field in settings.__fields__.values():
            env_val: Union[str, None, UndefinedType] = Undefined
            for env_name in field.field_info.extra["env_names"]:
                env_val = env_vars.get(env_name, Undefined)
                if env_name in env_file_vars:
                    del env_file_vars[env_name]
                if env_val is not Undefined:
                    break

            is_complex, allow_parse_failure = self.field_is_complex(field)
            if is_complex:
                if isinstance(env_val, UndefinedType):
                    # field is complex but no value found so far, try explode_env_vars
                    if env_val_built := self.explode_env_vars(field, env_vars):
                        d[field.alias] = env_val_built
                elif env_val is None:
                    d[field.alias] = env_val
                else:
                    # field is complex and there's a value
                    # decode that as JSON, then add explode_env_vars
                    try:
                        env_val = settings.__config__.parse_env_var(field.name, env_val)
                    except ValueError as e:
                        if not allow_parse_failure:
                            raise SettingsError(
                                f'error parsing env var "{env_name}"'  # type: ignore
                            ) from e

                    if isinstance(env_val, dict):
                        d[field.alias] = deep_update(
                            env_val, self.explode_env_vars(field, env_vars)
                        )
                    else:
                        d[field.alias] = env_val
            elif not isinstance(env_val, UndefinedType):
                # simplest case, field is not complex
                # we only need to add the value if it was found
                d[field.alias] = env_val

        # remain user custom config
        for env_name in env_file_vars:
            env_val = env_vars[env_name]
            if env_val and (val_striped := env_val.strip()):
                # there's a value, decode that as JSON
                try:
                    env_val = settings.__config__.parse_env_var(env_name, val_striped)
                except ValueError:
                    logger.trace(
                        "Error while parsing JSON for "
                        f"{env_name!r}={val_striped!r}. "
                        "Assumed as string."
                    )

            # explode value when it's a nested dict
            env_name, *nested_keys = env_name.split(self.env_nested_delimiter)
            if nested_keys and (env_name not in d or isinstance(d[env_name], dict)):
                result = {}
                *keys, last_key = nested_keys
                _tmp = result
                for key in keys:
                    _tmp = _tmp.setdefault(key, {})
                _tmp[last_key] = env_val
                d[env_name] = deep_update(d.get(env_name, {}), result)
            elif not nested_keys:
                d[env_name] = env_val

        return d


class BaseConfig(BaseSettings):
    if TYPE_CHECKING:
        # dummy getattr for pylance checking, actually not used
        def __getattr__(self, name: str) -> Any:  # pragma: no cover
            return self.__dict__.get(name)

    class Config:
        extra = Extra.allow
        env_nested_delimiter = "__"

        @classmethod
        def customise_sources(
            cls,
            init_settings: InitSettingsSource,
            env_settings: EnvSettingsSource,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            common_config = init_settings.init_kwargs.pop("_common_config", {})
            return (
                init_settings,
                CustomEnvSettings(
                    env_settings.env_file,
                    env_settings.env_file_encoding,
                    env_settings.env_nested_delimiter,
                    env_settings.env_prefix_len,
                ),
                InitSettingsSource(common_config),
                file_secret_settings,
            )


class Env(BaseConfig):
    """运行环境配置。大小写不敏感。

    将会从 **环境变量** > **dotenv 配置文件** 的优先级读取环境信息。
    """

    environment: str = "prod"
    """当前环境名。

    NoneBot 将从 `.env.{environment}` 文件中加载配置。
    """

    class Config:
        env_file = ".env"


class Config(BaseConfig):
    """NoneBot 主要配置。大小写不敏感。

    除了 NoneBot 的配置项外，还可以自行添加配置项到 `.env.{environment}` 文件中。
    这些配置将会在 json 反序列化后一起带入 `Config` 类中。

    配置方法参考: [配置](https://nonebot.dev/docs/appendices/config)
    """

    _env_file: DotenvType = ".env", ".env.prod"

    # nonebot configs
    driver: str = "~fastapi"
    """NoneBot 运行所使用的 `Driver` 。继承自 {ref}`nonebot.drivers.Driver` 。

    配置格式为 `<module>[:<Driver>][+<module>[:<Mixin>]]*`。

    `~` 为 `nonebot.drivers.` 的缩写。

    配置方法参考: [配置驱动器](https://nonebot.dev/docs/advanced/driver#%E9%85%8D%E7%BD%AE%E9%A9%B1%E5%8A%A8%E5%99%A8)
    """
    host: IPvAnyAddress = IPv4Address("127.0.0.1")  # type: ignore
    """NoneBot {ref}`nonebot.drivers.ReverseDriver` 服务端监听的 IP/主机名。"""
    port: int = Field(default=8080, ge=1, le=65535)
    """NoneBot {ref}`nonebot.drivers.ReverseDriver` 服务端监听的端口。"""
    log_level: Union[int, str] = "INFO"
    """NoneBot 日志输出等级，可以为 `int` 类型等级或等级名称。

    参考 [记录日志](https://nonebot.dev/docs/appendices/log)，[loguru 日志等级](https://loguru.readthedocs.io/en/stable/api/logger.html#levels)。

    :::tip 提示
    日志等级名称应为大写，如 `INFO`。
    :::

    用法:
        ```conf
        LOG_LEVEL=25
        LOG_LEVEL=INFO
        ```
    """

    # bot connection configs
    api_timeout: Optional[float] = 30.0
    """API 请求超时时间，单位: 秒。"""

    # bot runtime configs
    superusers: Set[str] = set()
    """机器人超级用户。

    用法:
        ```conf
        SUPERUSERS=["12345789"]
        ```
    """
    nickname: Set[str] = set()
    """机器人昵称。"""
    command_start: Set[str] = {"/"}
    """命令的起始标记，用于判断一条消息是不是命令。

    参考[命令响应规则](https://nonebot.dev/docs/advanced/matcher#command)。

    用法:
        ```conf
        COMMAND_START=["/", ""]
        ```
    """
    command_sep: Set[str] = {"."}
    """命令的分隔标记，用于将文本形式的命令切分为元组（实际的命令名）。

    参考[命令响应规则](https://nonebot.dev/docs/advanced/matcher#command)。

    用法:
        ```conf
        COMMAND_SEP=["."]
        ```
    """
    session_expire_timeout: timedelta = timedelta(minutes=2)
    """等待用户回复的超时时间。

    用法:
        ```conf
        SESSION_EXPIRE_TIMEOUT=120  # 单位: 秒
        SESSION_EXPIRE_TIMEOUT=[DD ][HH:MM]SS[.ffffff]
        SESSION_EXPIRE_TIMEOUT=P[DD]DT[HH]H[MM]M[SS]S  # ISO 8601
        ```
    """

    # adapter configs
    # adapter configs are defined in adapter/config.py

    # custom configs
    # custom configs can be assigned during nonebot.init
    # or from env file using json loads

    class Config:
        env_file = ".env", ".env.prod"


__autodoc__ = {
    "CustomEnvSettings": False,
    "BaseConfig": False,
}
