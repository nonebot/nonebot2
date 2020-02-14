from typing import Union, Callable, Iterable

from nonebot.typing import CommandName_T


class CommandGroup:
    """
    Group a set of commands with same name prefix.
    """

    __slots__ = ('basename', 'base_kwargs')

    def __init__(self, name: Union[str, CommandName_T], *,
                 permission: int = ...,
                 only_to_me: bool = ...,
                 privileged: bool = ...,
                 shell_like: bool = ...): ...

    def command(self, name: Union[str, CommandName_T], *,
                aliases: Union[Iterable[str], str] = ...,
                permission: int = ...,
                only_to_me: bool = ...,
                privileged: bool = ...,
                shell_like: bool = ...) -> Callable: ...
