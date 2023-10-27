import json
from typing import Dict, List, Union, Literal, TypeVar, ClassVar

from utils import FakeMessage, FakeMessageSegment
from nonebot.utils import (
    DataclassEncoder,
    escape_tag,
    is_gen_callable,
    is_async_gen_callable,
    is_coroutine_callable,
    generic_check_issubclass,
)


def test_loguru_escape_tag():
    assert escape_tag("<red>red</red>") == r"\<red>red\</red>"
    assert escape_tag("<fg #fff>white</fg #fff>") == r"\<fg #fff>white\</fg #fff>"
    assert escape_tag("<fg\n#fff>white</fg\n#fff>") == "\\<fg\n#fff>white\\</fg\n#fff>"
    assert escape_tag("<bg #fff>white</bg #fff>") == r"\<bg #fff>white\</bg #fff>"
    assert escape_tag("<bg\n#fff>white</bg\n#fff>") == "\\<bg\n#fff>white\\</bg\n#fff>"


def test_generic_check_issubclass():
    assert generic_check_issubclass(int, (int, float))
    assert not generic_check_issubclass(str, (int, float))
    assert generic_check_issubclass(Union[int, float, None], (int, float))
    assert generic_check_issubclass(Literal[1, 2, 3], int)
    assert not generic_check_issubclass(Literal[1, 2, "3"], int)
    assert generic_check_issubclass(List[int], list)
    assert generic_check_issubclass(Dict[str, int], dict)
    assert not generic_check_issubclass(ClassVar[int], int)
    assert generic_check_issubclass(TypeVar("T", int, float), (int, float))
    assert generic_check_issubclass(TypeVar("T", bound=int), (int, float))


def test_is_coroutine_callable():
    async def test1():
        ...

    def test2():
        ...

    class TestClass1:
        async def __call__(self):
            ...

    class TestClass2:
        def __call__(self):
            ...

    assert is_coroutine_callable(test1)
    assert not is_coroutine_callable(test2)
    assert not is_coroutine_callable(TestClass1)
    assert is_coroutine_callable(TestClass1())
    assert not is_coroutine_callable(TestClass2)


def test_is_gen_callable():
    def test1():
        yield

    async def test2():
        yield

    def test3():
        ...

    class TestClass1:
        def __call__(self):
            yield

    class TestClass2:
        async def __call__(self):
            yield

    class TestClass3:
        def __call__(self):
            ...

    assert is_gen_callable(test1)
    assert not is_gen_callable(test2)
    assert not is_gen_callable(test3)
    assert is_gen_callable(TestClass1())
    assert not is_gen_callable(TestClass2())
    assert not is_gen_callable(TestClass3())


def test_is_async_gen_callable():
    async def test1():
        yield

    def test2():
        yield

    async def test3():
        ...

    class TestClass1:
        async def __call__(self):
            yield

    class TestClass2:
        def __call__(self):
            yield

    class TestClass3:
        async def __call__(self):
            ...

    assert is_async_gen_callable(test1)
    assert not is_async_gen_callable(test2)
    assert not is_async_gen_callable(test3)
    assert is_async_gen_callable(TestClass1())
    assert not is_async_gen_callable(TestClass2())
    assert not is_async_gen_callable(TestClass3())


def test_dataclass_encoder():
    simple = json.dumps("123", cls=DataclassEncoder)
    assert simple == '"123"'

    ms = FakeMessageSegment.nested(FakeMessage(FakeMessageSegment.text("text")))
    s = json.dumps(ms, cls=DataclassEncoder)
    assert s == (
        "{"
        '"type": "node", '
        '"data": {"content": [{"type": "text", "data": {"text": "text"}}]}'
        "}"
    )
