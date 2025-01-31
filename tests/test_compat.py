from dataclasses import dataclass
from typing import Annotated, Any, Optional

from pydantic import BaseModel, ValidationError
import pytest

from nonebot.compat import (
    DEFAULT_CONFIG,
    FieldInfo,
    PydanticUndefined,
    Required,
    TypeAdapter,
    custom_validation,
    field_validator,
    model_dump,
    model_validator,
    type_validate_json,
    type_validate_python,
)


def test_default_config():
    assert DEFAULT_CONFIG.get("extra") == "allow"
    assert DEFAULT_CONFIG.get("arbitrary_types_allowed") is True


def test_field_info():
    # required should be convert to PydanticUndefined
    assert FieldInfo(Required).default is PydanticUndefined

    # field info should allow extra attributes
    assert FieldInfo(test="test").extra["test"] == "test"


def test_field_validator():
    class TestModel(BaseModel):
        foo: int
        bar: str

        @field_validator("foo")
        @classmethod
        def test_validator(cls, v: Any) -> Any:
            if v > 0:
                return v
            raise ValueError("test must be greater than 0")

        @field_validator("bar", mode="before")
        @classmethod
        def test_validator_before(cls, v: Any) -> Any:
            if not isinstance(v, str):
                v = str(v)
            return v

    assert type_validate_python(TestModel, {"foo": 1, "bar": "test"}).foo == 1
    assert type_validate_python(TestModel, {"foo": 1, "bar": 123}).bar == "123"

    with pytest.raises(ValidationError):
        TestModel(foo=0, bar="test")


def test_type_adapter():
    t = TypeAdapter(Annotated[int, FieldInfo(ge=1)])

    assert t.validate_python(2) == 2

    with pytest.raises(ValidationError):
        t.validate_python(0)

    assert t.validate_json("2") == 2

    with pytest.raises(ValidationError):
        t.validate_json("0")


def test_model_dump():
    class TestModel(BaseModel):
        test1: int
        test2: int

    assert model_dump(TestModel(test1=1, test2=2), include={"test1"}) == {"test1": 1}
    assert model_dump(TestModel(test1=1, test2=2), exclude={"test1"}) == {"test2": 2}


def test_model_validator():
    class TestModel(BaseModel):
        foo: int
        bar: str

        @model_validator(mode="before")
        @classmethod
        def test_validator_before(cls, data: Any) -> Any:
            if isinstance(data, dict):
                if "foo" not in data:
                    data["foo"] = 1
            return data

        @model_validator(mode="after")
        @classmethod
        def test_validator_after(cls, data: Any) -> Any:
            if isinstance(data, dict):
                if data["bar"] == "test":
                    raise ValueError("bar should not be test")
            elif data.bar == "test":
                raise ValueError("bar should not be test")
            return data

    assert type_validate_python(TestModel, {"bar": "aaa"}).foo == 1

    with pytest.raises(ValidationError):
        type_validate_python(TestModel, {"foo": 1, "bar": "test"})


def test_custom_validation():
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


def test_validate_json():
    class TestModel(BaseModel):
        test1: int
        test2: str
        test3: bool
        test4: dict
        test5: list
        test6: Optional[int]

    assert type_validate_json(
        TestModel,
        "{"
        '  "test1": 1,'
        '  "test2": "2",'
        '  "test3": true,'
        '  "test4": {},'
        '  "test5": [],'
        '  "test6": null'
        "}",
    ) == TestModel(test1=1, test2="2", test3=True, test4={}, test5=[], test6=None)
