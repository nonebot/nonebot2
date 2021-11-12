"""
事件处理函数
============

该模块实现事件处理函数的封装，以实现动态参数等功能。
"""
from typing import TYPE_CHECKING, List, Optional

from .models import Depends
from nonebot.utils import get_name
from nonebot.typing import T_State, T_Handler
from . import get_dependent, get_parameterless_sub_dependant

if TYPE_CHECKING:
    from .matcher import Matcher
    from nonebot.adapters import Bot, Event


class Handler:
    """事件处理函数类"""

    def __init__(self,
                 func: T_Handler,
                 *,
                 name: Optional[str] = None,
                 dependencies: Optional[List[Depends]] = None):
        """装饰事件处理函数以便根据动态参数运行"""
        self.func: T_Handler = func
        """
        :类型: ``T_Handler``
        :说明: 事件处理函数
        """
        self.name = get_name(func) if name is None else name

        self.dependencies = dependencies or []
        self.dependent = get_dependent(func=func)
        for depends in self.dependencies[::-1]:
            self.dependent.dependencies.insert(
                0, get_parameterless_sub_dependant(depends=depends))

    def __call__(self, bot: Bot, event: Event, state: T_State,
                 matcher: "Matcher"):
        ...
