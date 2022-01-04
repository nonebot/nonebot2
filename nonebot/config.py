"""
配置
====

NoneBot 使用 `pydantic`_ 以及 `python-dotenv`_ 来读取配置。

配置项需符合特殊格式或 json 序列化格式。详情见 `pydantic Field Type`_ 文档。

.. _pydantic:
    https://pydantic-docs.helpmanual.io/
.. _python-dotenv:
    https://saurabh-kumar.com/python-dotenv/
.. _pydantic Field Type:
    https://pydantic-docs.helpmanual.io/usage/types/
"""
import os
from pathlib import Path
from datetime import timedelta
from ipaddress import IPv4Address
from typing import Any, Set, Dict, Tuple, Union, Mapping, Optional

from pydantic import BaseSettings, IPvAnyAddress
from pydantic.env_settings import (
    SettingsError,
    EnvSettingsSource,
    InitSettingsSource,
    SettingsSourceCallable,
    read_env_file,
    env_file_sentinel,
)

from nonebot.log import logger
from nonebot.utils import escape_tag


class CustomEnvSettings(EnvSettingsSource):
    def __call__(self, settings: BaseSettings) -> Dict[str, Any]:
        """
        Build environment variables suitable for passing to the Model.
        """
        d: Dict[str, Optional[str]] = {}

        if settings.__config__.case_sensitive:
            env_vars: Mapping[str, Optional[str]] = os.environ  # pragma: no cover
        else:
            env_vars = {k.lower(): v for k, v in os.environ.items()}

        env_file_vars: Dict[str, Optional[str]] = {}
        env_file = (
            self.env_file
            if self.env_file != env_file_sentinel
            else settings.__config__.env_file
        )
        env_file_encoding = (
            self.env_file_encoding
            if self.env_file_encoding is not None
            else settings.__config__.env_file_encoding
        )
        if env_file is not None:
            env_path = Path(env_file)
            if env_path.is_file():
                env_file_vars = read_env_file(
                    env_path,
                    encoding=env_file_encoding,
                    case_sensitive=settings.__config__.case_sensitive,
                )
                env_vars = {**env_file_vars, **env_vars}

        for field in settings.__fields__.values():
            env_val: Optional[str] = None
            for env_name in field.field_info.extra["env_names"]:
                env_val = env_vars.get(env_name)
                if env_name in env_file_vars:
                    del env_file_vars[env_name]
                if env_val is not None:
                    break

            if env_val is None:
                continue

            if field.is_complex():
                try:
                    env_val = settings.__config__.json_loads(env_val)
                except ValueError as e:  # pragma: no cover
                    raise SettingsError(
                        f'error parsing JSON for "{env_name}"'  # type: ignore
                    ) from e
            d[field.alias] = env_val

        if env_file_vars:
            for env_name, env_val in env_file_vars.items():
                if (env_val is None or len(env_val) == 0) and env_name in env_vars:
                    env_val = env_vars[env_name]
                try:
                    if env_val:
                        env_val = settings.__config__.json_loads(env_val.strip())
                except ValueError as e:
                    logger.opt(colors=True, exception=e).trace(
                        f"Error while parsing JSON for {escape_tag(env_name)}. Assumed as string."
                    )

                d[env_name] = env_val

        return d


class BaseConfig(BaseSettings):
    # dummy getattr for pylance checking, actually not used
    def __getattr__(self, name: str) -> Any:  # pragma: no cover
        return self.__dict__.get(name)

    class Config:
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
                    env_settings.env_file, env_settings.env_file_encoding
                ),
                InitSettingsSource(common_config),
                file_secret_settings,
            )


class Env(BaseConfig):
    """
    运行环境配置。大小写不敏感。

    将会从 ``nonebot.init 参数`` > ``环境变量`` > ``.env 环境配置文件`` 的优先级读取配置。
    """

    environment: str = "prod"
    """
    - **类型**: ``str``
    - **默认值**: ``"prod"``

    :说明:
      当前环境名。 NoneBot 将从 ``.env.{environment}`` 文件中加载配置。
    """

    class Config:
        extra = "allow"
        env_file = ".env"


class Config(BaseConfig):
    """
    NoneBot 主要配置。大小写不敏感。

    除了 NoneBot 的配置项外，还可以自行添加配置项到 ``.env.{environment}`` 文件中。
    这些配置将会在 json 反序列化后一起带入 ``Config`` 类中。
    """

    _common_config: dict
    _env_file: str

    # nonebot configs
    driver: str = "~fastapi"
    """
    - **类型**: ``str``
    - **默认值**: ``"~fastapi"``

    :说明:

      NoneBot 运行所使用的 ``Driver`` 。继承自 ``nonebot.drivers.Driver`` 。

      配置格式为 ``<module>[:<Driver>][+<module>[:<Mixin>]]*``。

      ``~`` 为 ``nonebot.drivers.`` 的缩写。
    """
    host: IPvAnyAddress = IPv4Address("127.0.0.1")  # type: ignore
    """
    - **类型**: ``IPvAnyAddress``
    - **默认值**: ``127.0.0.1``

    :说明:

      NoneBot 的 HTTP 和 WebSocket 服务端监听的 IP/主机名。
    """
    port: int = 8080
    """
    - **类型**: ``int``
    - **默认值**: ``8080``

    :说明:

      NoneBot 的 HTTP 和 WebSocket 服务端监听的端口。
    """
    log_level: Union[int, str] = "INFO"
    """
    - **类型**: ``Union[int, str]``
    - **默认值**: ``INFO``

    :说明:

      配置 NoneBot 日志输出等级，可以为 ``int`` 类型等级或等级名称，参考 `loguru 日志等级`_。

    :示例:

    .. code-block:: default

        LOG_LEVEL=25
        LOG_LEVEL=INFO

    .. _loguru 日志等级:
        https://loguru.readthedocs.io/en/stable/api/logger.html#levels
    """

    # bot connection configs
    api_timeout: Optional[float] = 30.0
    """
    - **类型**: ``Optional[float]``
    - **默认值**: ``30.``

    :说明:

      API 请求超时时间，单位: 秒。
    """

    # bot runtime configs
    superusers: Set[str] = set()
    """
    - **类型**: ``Set[str]``
    - **默认值**: ``set()``

    :说明:

      机器人超级用户。

    :示例:

    .. code-block:: default

        SUPERUSERS=["12345789"]
    """
    nickname: Set[str] = set()
    """
    - **类型**: ``Set[str]``
    - **默认值**: ``set()``

    :说明:

      机器人昵称。
    """
    command_start: Set[str] = {"/"}
    """
    - **类型**: ``Set[str]``
    - **默认值**: ``{"/"}``

    :说明:

      命令的起始标记，用于判断一条消息是不是命令。
    """
    command_sep: Set[str] = {"."}
    """
    - **类型**: ``Set[str]``
    - **默认值**: ``{"."}``

    :说明:

      命令的分隔标记，用于将文本形式的命令切分为元组（实际的命令名）。
    """
    session_expire_timeout: timedelta = timedelta(minutes=2)
    """
    - **类型**: ``timedelta``
    - **默认值**: ``timedelta(minutes=2)``

    :说明:

      等待用户回复的超时时间。

    :示例:

    .. code-block:: default

        SESSION_EXPIRE_TIMEOUT=120  # 单位: 秒
        SESSION_EXPIRE_TIMEOUT=[DD ][HH:MM]SS[.ffffff]
        SESSION_EXPIRE_TIMEOUT=P[DD]DT[HH]H[MM]M[SS]S  # ISO 8601
    """

    # adapter configs
    # adapter configs are defined in adapter/config.py

    # custom configs
    # custom configs can be assigned during nonebot.init
    # or from env file using json loads

    class Config:
        extra = "allow"
        env_file = ".env.prod"
