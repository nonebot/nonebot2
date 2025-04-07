"""本模块定义了 NoneBot 本身运行所需的配置项。

NoneBot 使用 [`pydantic`](https://pydantic-docs.helpmanual.io/) 以及
[`python-dotenv`](https://saurabh-kumar.com/python-dotenv/) 来读取配置。

配置项需符合特殊格式或 json 序列化格式
详情见 [`pydantic Field Type`](https://pydantic-docs.helpmanual.io/usage/types/) 文档。

FrontMatter:
    mdx:
        format: md
    sidebar_position: 1
    description: nonebot.config 模块
"""

import abc
from collections.abc import Mapping
from datetime import timedelta
from ipaddress import IPv4Address
import json
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Union
from typing_extensions import TypeAlias, get_args, get_origin

from dotenv import dotenv_values
from pydantic import BaseModel, Field
from pydantic.networks import IPvAnyAddress

from nonebot.compat import (
    PYDANTIC_V2,
    ConfigDict,
    ModelField,
    PydanticUndefined,
    PydanticUndefinedType,
    model_config,
    model_fields,
)
from nonebot.log import logger
from nonebot.typing import origin_is_union
from nonebot.utils import deep_update, lenient_issubclass, type_is_complex

DOTENV_TYPE: TypeAlias = Union[
    Path, str, list[Union[Path, str]], tuple[Union[Path, str], ...]
]

ENV_FILE_SENTINEL = Path("")


class SettingsError(ValueError): ...


class BaseSettingsSource(abc.ABC):
    def __init__(self, settings_cls: type["BaseSettings"]) -> None:
        self.settings_cls = settings_cls

    @property
    def config(self) -> "SettingsConfig":
        return model_config(self.settings_cls)

    @abc.abstractmethod
    def __call__(self) -> dict[str, Any]:
        raise NotImplementedError


class InitSettingsSource(BaseSettingsSource):
    __slots__ = ("init_kwargs",)

    def __init__(
        self, settings_cls: type["BaseSettings"], init_kwargs: dict[str, Any]
    ) -> None:
        self.init_kwargs = init_kwargs
        super().__init__(settings_cls)

    def __call__(self) -> dict[str, Any]:
        return self.init_kwargs

    def __repr__(self) -> str:
        return f"InitSettingsSource(init_kwargs={self.init_kwargs!r})"


class DotEnvSettingsSource(BaseSettingsSource):
    def __init__(
        self,
        settings_cls: type["BaseSettings"],
        env_file: Optional[DOTENV_TYPE] = ENV_FILE_SENTINEL,
        env_file_encoding: Optional[str] = None,
        case_sensitive: Optional[bool] = None,
        env_nested_delimiter: Optional[str] = None,
    ) -> None:
        super().__init__(settings_cls)
        self.env_file = (
            env_file
            if env_file is not ENV_FILE_SENTINEL
            else self.config.get("env_file", (".env",))
        )
        self.env_file_encoding = (
            env_file_encoding
            if env_file_encoding is not None
            else self.config.get("env_file_encoding", "utf-8")
        )
        self.case_sensitive = (
            case_sensitive
            if case_sensitive is not None
            else self.config.get("case_sensitive", False)
        )
        self.env_nested_delimiter = (
            env_nested_delimiter
            if env_nested_delimiter is not None
            else self.config.get("env_nested_delimiter", None)
        )

    def _apply_case_sensitive(self, var_name: str) -> str:
        return var_name if self.case_sensitive else var_name.lower()

    def _field_is_complex(self, field: ModelField) -> tuple[bool, bool]:
        if type_is_complex(field.annotation):
            return True, False
        elif origin_is_union(get_origin(field.annotation)) and any(
            type_is_complex(arg) for arg in get_args(field.annotation)
        ):
            return True, True
        return False, False

    def _parse_env_vars(
        self, env_vars: Mapping[str, Optional[str]]
    ) -> dict[str, Optional[str]]:
        return {
            self._apply_case_sensitive(key): value for key, value in env_vars.items()
        }

    def _read_env_file(self, file_path: Path) -> dict[str, Optional[str]]:
        file_vars = dotenv_values(file_path, encoding=self.env_file_encoding)
        return self._parse_env_vars(file_vars)

    def _read_env_files(self) -> dict[str, Optional[str]]:
        env_files = self.env_file
        if env_files is None:
            return {}

        if isinstance(env_files, (str, os.PathLike)):
            env_files = [env_files]

        dotenv_vars: dict[str, Optional[str]] = {}
        for env_file in env_files:
            env_path = Path(env_file).expanduser()
            if env_path.is_file():
                dotenv_vars.update(self._read_env_file(env_path))
        return dotenv_vars

    def _next_field(
        self, field: Optional[ModelField], key: str
    ) -> Optional[ModelField]:
        if not field or origin_is_union(get_origin(field.annotation)):
            return None
        elif field.annotation and lenient_issubclass(field.annotation, BaseModel):
            for field in model_fields(field.annotation):
                if field.name == key:
                    return field
        return None

    def _explode_env_vars(
        self,
        field: ModelField,
        env_vars: dict[str, Optional[str]],
        env_file_vars: dict[str, Optional[str]],
    ) -> dict[str, Any]:
        if self.env_nested_delimiter is None:
            return {}

        prefix = f"{field.name}{self.env_nested_delimiter}"
        result: dict[str, Any] = {}
        for env_name, env_val in env_vars.items():
            if not env_name.startswith(prefix):
                continue

            # delete from file vars when used
            env_file_vars.pop(env_name, None)

            _, *keys, last_key = env_name.split(self.env_nested_delimiter)
            env_var = result
            target_field: Optional[ModelField] = field
            for key in keys:
                target_field = self._next_field(target_field, key)
                env_var = env_var.setdefault(key, {})

            target_field = self._next_field(target_field, last_key)
            if target_field and env_val:
                is_complex, allow_parse_failure = self._field_is_complex(target_field)
                if is_complex:
                    try:
                        env_val = json.loads(env_val)
                    except ValueError as e:
                        if not allow_parse_failure:
                            raise SettingsError(
                                f'error parsing env var "{env_name}"'
                            ) from e

            env_var[last_key] = env_val

        return result

    def __call__(self) -> dict[str, Any]:
        """从环境变量和 dotenv 配置文件中读取配置项。"""

        d: dict[str, Any] = {}

        env_vars = self._parse_env_vars(os.environ)
        env_file_vars = self._read_env_files()
        env_vars = {**env_file_vars, **env_vars}

        for field in model_fields(self.settings_cls):
            field_name = field.name
            env_name = self._apply_case_sensitive(field_name)

            # try get values from env vars
            env_val = env_vars.get(env_name, PydanticUndefined)
            # delete from file vars when used
            if env_name in env_file_vars:
                del env_file_vars[env_name]

            is_complex, allow_parse_failure = self._field_is_complex(field)
            if is_complex:
                if isinstance(env_val, PydanticUndefinedType):
                    # field is complex but no value found so far, try explode_env_vars
                    if env_val_built := self._explode_env_vars(
                        field, env_vars, env_file_vars
                    ):
                        d[field_name] = env_val_built
                elif env_val is None:
                    d[field_name] = env_val
                else:
                    # field is complex and there's a value
                    # decode that as JSON, then add explode_env_vars
                    try:
                        env_val = json.loads(env_val)
                    except ValueError as e:
                        if not allow_parse_failure:
                            raise SettingsError(
                                f'error parsing env var "{env_name}"'
                            ) from e

                    if isinstance(env_val, dict):
                        # field value is a dict
                        # try explode_env_vars to find more sub-values
                        d[field_name] = deep_update(
                            env_val,
                            self._explode_env_vars(field, env_vars, env_file_vars),
                        )
                    else:
                        d[field_name] = env_val
            elif env_val is not PydanticUndefined:
                # simplest case, field is not complex
                # we only need to add the value if it was found
                d[field_name] = env_val

        # remain user custom config
        for env_name in env_file_vars:
            env_val = env_vars[env_name]
            if env_val and (val_striped := env_val.strip()):
                # there's a value, decode that as JSON
                try:
                    env_val = json.loads(val_striped)
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


if PYDANTIC_V2:  # pragma: pydantic-v2

    class SettingsConfig(ConfigDict, total=False):
        env_file: Optional[DOTENV_TYPE]
        env_file_encoding: str
        case_sensitive: bool
        env_nested_delimiter: Optional[str]

else:  # pragma: pydantic-v1

    class SettingsConfig(ConfigDict):
        env_file: Optional[DOTENV_TYPE]
        env_file_encoding: str
        case_sensitive: bool
        env_nested_delimiter: Optional[str]


class BaseSettings(BaseModel):
    if TYPE_CHECKING:
        # dummy getattr for pylance checking, actually not used
        def __getattr__(self, name: str) -> Any:  # pragma: no cover
            return self.__dict__.get(name)

    if PYDANTIC_V2:  # pragma: pydantic-v2
        model_config = SettingsConfig(
            extra="allow",
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=False,
            env_nested_delimiter="__",
        )
    else:  # pragma: pydantic-v1

        class Config(SettingsConfig):
            extra = "allow"  # type: ignore
            env_file = ".env"
            env_file_encoding = "utf-8"
            case_sensitive = False
            env_nested_delimiter = "__"

    def __init__(
        __settings_self__,  # pyright: ignore[reportSelfClsParameterName]
        _env_file: Optional[DOTENV_TYPE] = ENV_FILE_SENTINEL,
        _env_file_encoding: Optional[str] = None,
        _env_nested_delimiter: Optional[str] = None,
        **values: Any,
    ) -> None:
        super().__init__(
            **__settings_self__._settings_build_values(
                values,
                env_file=_env_file,
                env_file_encoding=_env_file_encoding,
                env_nested_delimiter=_env_nested_delimiter,
            )
        )

    def _settings_build_values(
        self,
        init_kwargs: dict[str, Any],
        env_file: Optional[DOTENV_TYPE] = None,
        env_file_encoding: Optional[str] = None,
        env_nested_delimiter: Optional[str] = None,
    ) -> dict[str, Any]:
        init_settings = InitSettingsSource(self.__class__, init_kwargs=init_kwargs)
        env_settings = DotEnvSettingsSource(
            self.__class__,
            env_file=env_file,
            env_file_encoding=env_file_encoding,
            env_nested_delimiter=env_nested_delimiter,
        )
        return deep_update(env_settings(), init_settings())


class Env(BaseSettings):
    """运行环境配置。大小写不敏感。

    将会从 **环境变量** > **dotenv 配置文件** 的优先级读取环境信息。
    """

    environment: str = "prod"
    """当前环境名。

    NoneBot 将从 `.env.{environment}` 文件中加载配置。
    """


class Config(BaseSettings):
    """NoneBot 主要配置。大小写不敏感。

    除了 NoneBot 的配置项外，还可以自行添加配置项到 `.env.{environment}` 文件中。
    这些配置将会在 json 反序列化后一起带入 `Config` 类中。

    配置方法参考: [配置](https://nonebot.dev/docs/appendices/config)
    """

    if TYPE_CHECKING:
        _env_file: Optional[DOTENV_TYPE] = ".env", ".env.prod"

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
    superusers: set[str] = set()
    """机器人超级用户。

    用法:
        ```conf
        SUPERUSERS=["12345789"]
        ```
    """
    nickname: set[str] = set()
    """机器人昵称。"""
    command_start: set[str] = {"/"}
    """命令的起始标记，用于判断一条消息是不是命令。

    参考[命令响应规则](https://nonebot.dev/docs/advanced/matcher#command)。

    用法:
        ```conf
        COMMAND_START=["/", ""]
        ```
    """
    command_sep: set[str] = {"."}
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
        SESSION_EXPIRE_TIMEOUT=[-][DD]D[,][HH:MM:]SS[.ffffff]
        SESSION_EXPIRE_TIMEOUT=[±]P[DD]DT[HH]H[MM]M[SS]S  # ISO 8601
        ```
    """

    # adapter configs
    # adapter configs are defined in adapter/config.py

    # custom configs
    # custom configs can be assigned during nonebot.init
    # or from env file using json loads

    if PYDANTIC_V2:  # pragma: pydantic-v2
        model_config = SettingsConfig(env_file=(".env", ".env.prod"))
    else:  # pragma: pydantic-v1

        class Config(  # pyright: ignore[reportIncompatibleVariableOverride]
            SettingsConfig
        ):
            env_file = ".env", ".env.prod"


__autodoc__ = {
    "SettingsError": False,
    "BaseSettingsSource": False,
    "InitSettingsSource": False,
    "DotEnvSettingsSource": False,
    "SettingsConfig": False,
    "BaseSettings": False,
}
