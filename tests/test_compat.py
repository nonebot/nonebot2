from typing import Any, Optional
from dataclasses import dataclass

import pytest
from pydantic import BaseModel

from nonebot.compat import (
    DEFAULT_CONFIG,
    Required,
    FieldInfo,
    PydanticUndefined,
    model_dump,
    custom_validation,
    type_validate_json,
    type_validate_python,
)


@pytest.mark.asyncio
async def test_default_config():
    assert DEFAULT_CONFIG.get("extra") == "allow"
    assert DEFAULT_CONFIG.get("arbitrary_types_allowed") is True


@pytest.mark.asyncio
async def test_field_info():
    # required should be convert to PydanticUndefined
    assert FieldInfo(Required).default is PydanticUndefined

    # field info should allow extra attributes
    assert FieldInfo(test="test").extra["test"] == "test"


@pytest.mark.asyncio
async def test_model_dump():
    class TestModel(BaseModel):
        test1: int
        test2: int

    assert model_dump(TestModel(test1=1, test2=2), include={"test1"}) == {"test1": 1}
    assert model_dump(TestModel(test1=1, test2=2), exclude={"test1"}) == {"test2": 2}


@pytest.mark.asyncio
async def test_custom_validation():
    called = []

    @custom_validation
    @dataclass
    class TestModel:
        test: int

        @classmethod
        def __get_validators__(cls):
            yield cls._validate_1
            yield cls._validate_2

        @classmethod
        def _validate_1(cls, v: Any) -> Any:
            called.append(1)
            return v

        @classmethod
        def _validate_2(cls, v: Any) -> Any:
            called.append(2)
            return cls(test=v["test"])

    assert type_validate_python(TestModel, {"test": 1}) == TestModel(test=1)
    assert called == [1, 2]


@pytest.mark.asyncio
async def test_validate_json():
    class TestModel(BaseModel):
        test1: int
        test2: str
        test3: bool
        test4: dict
        test5: list
        test6: Optional[int]

    assert (
        type_validate_json(
            TestModel,
            "{"
            '  "test1": 1,'
            '  "test2": "2",'
            '  "test3": true,'
            '  "test4": {},'
            '  "test5": [],'
            '  "test6": null'
            '}',
        )
        == TestModel(test1=1, test2="2", test3=True, test4={}, test5=[], test6=None)
    )
