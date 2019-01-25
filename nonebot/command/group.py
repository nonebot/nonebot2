from typing import Union, Callable

from nonebot.command import on_command
from nonebot.typing import CommandName_T


class CommandGroup:
    """
    Group a set of commands with same name prefix.
    """

    __slots__ = ('basename', 'base_kwargs')

    def __init__(self, name: Union[str, CommandName_T], **kwargs):
        self.basename = (name,) if isinstance(name, str) else name
        if 'aliases' in kwargs:
            del kwargs['aliases']  # ensure there is no aliases here
        self.base_kwargs = kwargs

    def command(self, name: Union[str, CommandName_T], **kwargs) -> Callable:
        sub_name = (name,) if isinstance(name, str) else name
        name = self.basename + sub_name

        final_kwargs = self.base_kwargs.copy()
        final_kwargs.update(kwargs)
        return on_command(name, **final_kwargs)
