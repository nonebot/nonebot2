from collections.abc import ItemsView, Iterator, KeysView, MutableMapping, ValuesView
from typing import TYPE_CHECKING, Optional, TypeVar, Union, overload

from .provider import DEFAULT_PROVIDER_CLASS, MatcherProvider

if TYPE_CHECKING:
    from .matcher import Matcher

T = TypeVar("T")


class MatcherManager(MutableMapping[int, list[type["Matcher"]]]):
    """事件响应器管理器

    实现了常用字典操作，用于管理事件响应器。
    """

    def __init__(self):
        self.provider: MatcherProvider = DEFAULT_PROVIDER_CLASS({})

    def __repr__(self) -> str:
        return f"MatcherManager(provider={self.provider!r})"

    def __contains__(self, o: object) -> bool:
        return o in self.provider

    def __iter__(self) -> Iterator[int]:
        return iter(self.provider)

    def __len__(self) -> int:
        return len(self.provider)

    def __getitem__(self, key: int) -> list[type["Matcher"]]:
        return self.provider[key]

    def __setitem__(self, key: int, value: list[type["Matcher"]]) -> None:
        self.provider[key] = value

    def __delitem__(self, key: int) -> None:
        del self.provider[key]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MatcherManager) and self.provider == other.provider

    def keys(self) -> KeysView[int]:
        return self.provider.keys()

    def values(self) -> ValuesView[list[type["Matcher"]]]:
        return self.provider.values()

    def items(self) -> ItemsView[int, list[type["Matcher"]]]:
        return self.provider.items()

    @overload
    def get(self, key: int) -> Optional[list[type["Matcher"]]]: ...

    @overload
    def get(
        self, key: int, default: list[type["Matcher"]]
    ) -> list[type["Matcher"]]: ...

    @overload
    def get(self, key: int, default: T) -> Union[list[type["Matcher"]], T]: ...

    def get(
        self, key: int, default: Optional[T] = None
    ) -> Optional[Union[list[type["Matcher"]], T]]:
        return self.provider.get(key, default)

    def pop(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, key: int
    ) -> list[type["Matcher"]]:
        return self.provider.pop(key)

    def popitem(self) -> tuple[int, list[type["Matcher"]]]:
        return self.provider.popitem()

    def clear(self) -> None:
        self.provider.clear()

    def update(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, m: MutableMapping[int, list[type["Matcher"]]], /
    ) -> None:
        self.provider.update(m)

    def setdefault(
        self, key: int, default: list[type["Matcher"]]
    ) -> list[type["Matcher"]]:
        return self.provider.setdefault(key, default)

    def set_provider(self, provider_class: type[MatcherProvider]) -> None:
        """设置事件响应器存储器

        参数:
            provider_class: 事件响应器存储器类
        """
        self.provider = provider_class(self.provider)
