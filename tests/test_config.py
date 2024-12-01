from typing import TYPE_CHECKING, Optional, Union

from pydantic import BaseModel, Field
import pytest

from nonebot.compat import PYDANTIC_V2
from nonebot.config import DOTENV_TYPE, BaseSettings, SettingsConfig, SettingsError


class Simple(BaseModel):
    a: int = 0
    b: int = 0
    c: dict = {}
    complex: list = []


class Example(BaseSettings):
    if TYPE_CHECKING:
        _env_file: Optional[DOTENV_TYPE] = ".env", ".env.example"
        _env_nested_delimiter: Optional[str] = "__"

    if PYDANTIC_V2:
        model_config = SettingsConfig(
            env_file=(".env", ".env.example"), env_nested_delimiter="__"
        )
    else:

        class Config(  # pyright: ignore[reportIncompatibleVariableOverride]
            SettingsConfig
        ):
            env_file = ".env", ".env.example"
            env_nested_delimiter = "__"

    simple: str = ""
    complex: list[int] = Field(default=[1])
    complex_none: Optional[list[int]] = None
    complex_union: Union[int, list[int]] = 1
    nested: Simple = Simple()
    nested_inner: Simple = Simple()


class ExampleWithoutDelimiter(Example):
    if PYDANTIC_V2:
        model_config = SettingsConfig(env_nested_delimiter=None)
    else:

        class Config(  # pyright: ignore[reportIncompatibleVariableOverride]
            SettingsConfig
        ):
            env_nested_delimiter = None


def test_config_no_env():
    config = Example(_env_file=None)
    assert config.simple == ""
    with pytest.raises(AttributeError):
        config.common_config


def test_config_with_env():
    config = Example(_env_file=(".env", ".env.example"))
    assert config.simple == "simple"

    assert config.complex == [1, 2, 3]

    assert config.complex_none is None

    assert config.complex_union == [1, 2, 3]

    assert config.nested.a == 1
    assert config.nested.b == 2
    assert config.nested.c == {"c": "3"}
    assert config.nested.complex == [1, 2, 3]
    with pytest.raises(AttributeError):
        config.nested__b
    with pytest.raises(AttributeError):
        config.nested__c__c
    with pytest.raises(AttributeError):
        config.nested__complex

    assert config.nested_inner.a == 1
    assert config.nested_inner.b == 2
    with pytest.raises(AttributeError):
        config.nested_inner__a
    with pytest.raises(AttributeError):
        config.nested_inner__b

    assert config.common_config == "common"

    assert config.other_simple == "simple"

    assert config.other_nested == {"a": 1, "b": 2}
    with pytest.raises(AttributeError):
        config.other_nested__b

    assert config.other_nested_inner == {"a": 1, "b": 2}
    with pytest.raises(AttributeError):
        config.other_nested_inner__a
    with pytest.raises(AttributeError):
        config.other_nested_inner__b


def test_config_error_env():
    with pytest.MonkeyPatch().context() as m:
        m.setenv("COMPLEX", "not json")

        with pytest.raises(SettingsError):
            Example(_env_file=(".env", ".env.example"))


def test_config_without_delimiter():
    config = ExampleWithoutDelimiter()
    assert config.nested.a == 1
    assert config.nested.b == 0
    assert config.nested__b == 2
    assert config.nested.c == {}
    assert config.nested__c__c == 3
    assert config.nested.complex == []
    assert config.nested__complex == [1, 2, 3]

    assert config.nested_inner.a == 0
    assert config.nested_inner.b == 0

    assert config.other_nested == {"a": 1}
    assert config.other_nested__b == 2

    with pytest.raises(AttributeError):
        config.other_nested_inner
    assert config.other_nested_inner__a == 1
    assert config.other_nested_inner__b == 2
