from typing import TYPE_CHECKING, TypeVar, Union, overload

from .abstract import Driver, Mixin

D = TypeVar("D", bound="Driver")

if TYPE_CHECKING:

    class CombinedDriver(Driver, Mixin): ...


@overload
def combine_driver(driver: type[D]) -> type[D]: ...


@overload
def combine_driver(
    driver: type[D], __m: type[Mixin], /, *mixins: type[Mixin]
) -> type["CombinedDriver"]: ...


def combine_driver(
    driver: type[D], *mixins: type[Mixin]
) -> Union[type[D], type["CombinedDriver"]]:
    """将一个驱动器和多个混入类合并。"""
    # check first
    if not issubclass(driver, Driver):
        raise TypeError("`driver` must be subclass of Driver")
    if not all(issubclass(m, Mixin) for m in mixins):
        raise TypeError("`mixins` must be subclass of Mixin")

    if not mixins:
        return driver

    def type_(self: "CombinedDriver") -> str:
        return (
            driver.type.__get__(self)  # type: ignore
            + "+"
            + "+".join(x.type.__get__(self) for x in mixins)  # type: ignore
        )

    return type("CombinedDriver", (*mixins, driver), {"type": property(type_)})  # type: ignore
