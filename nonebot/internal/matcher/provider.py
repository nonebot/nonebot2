import abc
from collections import defaultdict
from collections.abc import Mapping, MutableMapping
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .matcher import Matcher


class MatcherProvider(abc.ABC, MutableMapping[int, list[type["Matcher"]]]):
    """事件响应器存储器基类

    参数:
        matchers: 当前存储器中已有的事件响应器
    """

    @abc.abstractmethod
    def __init__(self, matchers: Mapping[int, list[type["Matcher"]]]):
        raise NotImplementedError


class _DictProvider(defaultdict[int, list[type["Matcher"]]], MatcherProvider):  # type: ignore
    def __init__(self, matchers: Mapping[int, list[type["Matcher"]]]):
        super().__init__(list, matchers)


DEFAULT_PROVIDER_CLASS = _DictProvider
"""默认存储器类型"""
