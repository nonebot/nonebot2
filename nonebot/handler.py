"""
事件处理函数
============

该模块实现事件处理函数的封装，以实现动态参数等功能。
"""

import asyncio
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Type, Callable, Optional

from nonebot.utils import get_name, run_sync
from nonebot.dependencies import (
    Param,
    Dependent,
    DependsWrapper,
    get_dependent,
    solve_dependencies,
    get_parameterless_sub_dependant,
)


class Handler:
    """事件处理器类。支持依赖注入。"""

    def __init__(
        self,
        call: Callable[..., Any],
        *,
        name: Optional[str] = None,
        dependencies: Optional[List[DependsWrapper]] = None,
        allow_types: Optional[List[Type[Param]]] = None,
    ):
        """
        :说明:

          装饰一个函数为事件处理器。

        :参数:

          * ``call: Callable[..., Any]``: 事件处理函数。
          * ``name: Optional[str]``: 事件处理器名称。默认为函数名。
          * ``dependencies: Optional[List[DependsWrapper]]``: 额外的非参数依赖注入。
          * ``allow_types: Optional[List[Type[Param]]]``: 允许的参数类型。
        """
        self.call = call
        """
        :类型: ``Callable[..., Any]``
        :说明: 事件处理函数
        """
        self.name = get_name(call) if name is None else name
        """
        :类型: ``str``
        :说明: 事件处理函数名
        """
        self.allow_types = allow_types or []
        """
        :类型: ``List[Type[Param]]``
        :说明: 事件处理器允许的参数类型
        """

        self.dependencies = dependencies or []
        """
        :类型: ``List[DependsWrapper]``
        :说明: 事件处理器的额外依赖
        """
        self.sub_dependents: Dict[Callable[..., Any], Dependent] = {}
        if dependencies:
            for depends in dependencies:
                self.cache_dependent(depends)
        self.dependent = get_dependent(call=call, allow_types=self.allow_types)

    def __repr__(self) -> str:
        return f"<Handler {self.name}({', '.join(map(str, self.dependent.params))})>"

    def __str__(self) -> str:
        return repr(self)

    async def __call__(
        self,
        *,
        _stack: Optional[AsyncExitStack] = None,
        _dependency_cache: Optional[Dict[Callable[..., Any], Any]] = None,
        **params,
    ) -> Any:
        values, _ = await solve_dependencies(
            _dependent=self.dependent,
            _stack=_stack,
            _sub_dependents=[
                self.sub_dependents[dependency.dependency]  # type: ignore
                for dependency in self.dependencies
            ],
            _dependency_cache=_dependency_cache,
            **params,
        )

        if asyncio.iscoroutinefunction(self.call):
            return await self.call(**values)
        else:
            return await run_sync(self.call)(**values)

    def cache_dependent(self, dependency: DependsWrapper):
        if not dependency.dependency:
            raise ValueError(f"{dependency} has no dependency")
        if dependency.dependency in self.sub_dependents:
            raise ValueError(f"{dependency} is already in dependencies")
        sub_dependant = get_parameterless_sub_dependant(
            depends=dependency, allow_types=self.allow_types
        )
        self.sub_dependents[dependency.dependency] = sub_dependant

    def prepend_dependency(self, dependency: DependsWrapper):
        self.cache_dependent(dependency)
        self.dependencies.insert(0, dependency)

    def append_dependency(self, dependency: DependsWrapper):
        self.cache_dependent(dependency)
        self.dependencies.append(dependency)

    def remove_dependency(self, dependency: DependsWrapper):
        if not dependency.dependency:
            raise ValueError(f"{dependency} has no dependency")
        if dependency.dependency in self.sub_dependents:
            del self.sub_dependents[dependency.dependency]
        if dependency in self.dependencies:
            self.dependencies.remove(dependency)
