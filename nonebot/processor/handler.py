"""
事件处理函数
============

该模块实现事件处理函数的封装，以实现动态参数等功能。
"""

import asyncio
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Callable, Optional

from .models import Depends, Dependent
from nonebot.utils import get_name, run_sync
from nonebot.typing import T_State, T_Handler
from . import get_dependent, solve_dependencies, get_parameterless_sub_dependant

if TYPE_CHECKING:
    from .matcher import Matcher
    from nonebot.adapters import Bot, Event


class Handler:
    """事件处理函数类"""

    def __init__(self,
                 func: T_Handler,
                 *,
                 name: Optional[str] = None,
                 dependencies: Optional[List[Depends]] = None,
                 dependency_overrides_provider: Optional[Any] = None):
        """装饰事件处理函数以便根据动态参数运行"""
        self.func: T_Handler = func
        """
        :类型: ``T_Handler``
        :说明: 事件处理函数
        """
        self.name = get_name(func) if name is None else name

        self.dependencies = dependencies or []
        self.sub_dependents: Dict[Tuple[Callable[..., Any]], Dependent] = {}
        if dependencies:
            for depends in dependencies:
                if not depends.dependency:
                    raise ValueError(f"{depends} has no dependency")
                if (depends.dependency,) in self.sub_dependents:
                    raise ValueError(f"{depends} is already in dependencies")
                sub_dependant = get_parameterless_sub_dependant(depends=depends)
                self.sub_dependents[(depends.dependency,)] = sub_dependant
        self.dependency_overrides_provider = dependency_overrides_provider
        self.dependent = get_dependent(func=func)

    async def __call__(self, matcher: "Matcher", bot: Bot, event: Event,
                       state: T_State):
        values, _ = await solve_dependencies(
            dependent=self.dependent,
            bot=bot,
            event=event,
            state=state,
            matcher=matcher,
            sub_dependents=[
                self.sub_dependents[(dependency.dependency,)]  # type: ignore
                for dependency in self.dependencies
            ],
            dependency_overrides_provider=self.dependency_overrides_provider)

        if asyncio.iscoroutinefunction(self.func):
            await self.func(**values)
        else:
            await run_sync(self.func)(**values)

    def cache_dependent(self, dependency: Depends):
        if not dependency.dependency:
            raise ValueError(f"{dependency} has no dependency")
        if (dependency.dependency,) in self.sub_dependents:
            raise ValueError(f"{dependency} is already in dependencies")
        sub_dependant = get_parameterless_sub_dependant(depends=dependency)
        self.sub_dependents[(dependency.dependency,)] = sub_dependant

    def prepend_dependency(self, dependency: Depends):
        self.cache_dependent(dependency)
        self.dependencies.insert(0, dependency)

    def append_dependency(self, dependency: Depends):
        self.cache_dependent(dependency)
        self.dependencies.append(dependency)

    def remove_dependency(self, dependency: Depends):
        if not dependency.dependency:
            raise ValueError(f"{dependency} has no dependency")
        if (dependency.dependency,) in self.sub_dependents:
            del self.sub_dependents[(dependency.dependency,)]
        if dependency in self.dependencies:
            self.dependencies.remove(dependency)
