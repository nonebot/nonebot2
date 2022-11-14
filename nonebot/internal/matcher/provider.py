import abc
from collections import defaultdict
from typing import TYPE_CHECKING, List, Type, Mapping, MutableMapping

if TYPE_CHECKING:
    from .matcher import Matcher


class MatcherProvider(abc.ABC, MutableMapping[int, List[Type["Matcher"]]]):
    @abc.abstractmethod
    def __init__(self, matchers: Mapping[int, List[Type["Matcher"]]]):
        raise NotImplementedError


class _DictProvider(defaultdict, MatcherProvider):
    def __init__(self, matchers: Mapping[int, List[Type["Matcher"]]]):
        super().__init__(list, matchers)


DEFAULT_PROVIDER = _DictProvider({})
