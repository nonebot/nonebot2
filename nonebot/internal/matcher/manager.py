from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Type,
    Tuple,
    Union,
    TypeVar,
    Iterator,
    KeysView,
    Optional,
    ItemsView,
    ValuesView,
    MutableMapping,
    overload,
)

from .provider import DEFAULT_PROVIDER_CLASS, MatcherProvider

if TYPE_CHECKING:
    from .matcher import Matcher

T = TypeVar("T")


class MatcherManager(MutableMapping[int, List[Type["Matcher"]]]):
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

    def __getitem__(self, key: int) -> List[Type["Matcher"]]:
        return self.provider[key]

    def __setitem__(self, key: int, value: List[Type["Matcher"]]) -> None:
        self.provider[key] = value

    def __delitem__(self, key: int) -> None:
        del self.provider[key]

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, MatcherManager) and self.provider == other.provider

    def keys(self) -> KeysView[int]:
        return self.provider.keys()

    def values(self) -> ValuesView[List[Type["Matcher"]]]:
        return self.provider.values()

    def items(self) -> ItemsView[int, List[Type["Matcher"]]]:
        return self.provider.items()

    @overload
    def get(self, key: int) -> Optional[List[Type["Matcher"]]]:
        ...

    @overload
    def get(self, key: int, default: T) -> Union[List[Type["Matcher"]], T]:
        ...

    def get(
        self, key: int, default: Optional[T] = None
    ) -> Optional[Union[List[Type["Matcher"]], T]]:
        return self.provider.get(key, default)

    def pop(self, key: int) -> List[Type["Matcher"]]:
        return self.provider.pop(key)

    def popitem(self) -> Tuple[int, List[Type["Matcher"]]]:
        return self.provider.popitem()

    def clear(self) -> None:
        self.provider.clear()

    def update(self, __m: MutableMapping[int, List[Type["Matcher"]]]) -> None:
        self.provider.update(__m)

    def setdefault(
        self, key: int, default: List[Type["Matcher"]]
    ) -> List[Type["Matcher"]]:
        return self.provider.setdefault(key, default)

    def set_provider(self, provider_class: Type[MatcherProvider]) -> None:
        """设置事件响应器存储器

        参数:
            provider_class: 事件响应器存储器类
        """
        self.provider = provider_class(self.provider)
