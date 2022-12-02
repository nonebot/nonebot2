---
sidebar_position: 0
description: nonebot.dependencies 模块
---

# nonebot.dependencies

本模块模块实现了依赖注入的定义与处理。

## _abstract class_ `Param(default=PydanticUndefined, **kwargs)` {#Param}

- **说明**

  依赖注入的基本单元 —— 参数。

  继承自 `pydantic.fields.FieldInfo`，用于描述参数信息（不包括参数名）。

- **参数**

  - `default` (Any)

  - `**kwargs` (Any)

## _class_ `Dependent(call, params=<factory>, parameterless=<factory>)` {#Dependent}

- **说明**

  依赖注入容器

- **参数**

  - `call` ((*Any, \*\*Any) -> (~ R) | (*Any, \*\*Any) -> Awaitable[(~ R)]): 依赖注入的可调用对象，可以是任何 Callable 对象

  - `params` (tuple[pydantic.fields.ModelField]): 具名参数列表

  - `parameterless` (tuple[[Param](#Param)]): 匿名参数列表

  - `pre_checkers`: 依赖注入解析前的参数检查

  - `allow_types`: 允许的参数类型

### _async method_ `check(self, **params)` {#Dependent-check}

- **参数**

  - `**params` (Any)

- **返回**

  - None

### _classmethod_ `parse(cls, *, call, parameterless=None, allow_types)` {#Dependent-parse}

- **参数**

  - `call` ((*Any, \*\*Any) -> (~ R) | (*Any, \*\*Any) -> Awaitable[(~ R)])

  - `parameterless` (Iterable[Any] | None)

  - `allow_types` (Iterable[Type[[Param](#Param)]])

- **返回**

  - Dependent[R]

### _staticmethod_ `parse_parameterless(parameterless, allow_types)` {#Dependent-parse_parameterless}

- **参数**

  - `parameterless` (tuple[Any, ...])

  - `allow_types` (tuple[Type[[Param](#Param)], ...])

- **返回**

  - tuple[[Param](#Param), ...]

### _staticmethod_ `parse_params(call, allow_types)` {#Dependent-parse_params}

- **参数**

  - `call` ((*Any, \*\*Any) -> (~ R) | (*Any, \*\*Any) -> Awaitable[(~ R)])

  - `allow_types` (tuple[Type[[Param](#Param)], ...])

- **返回**

  - tuple[pydantic.fields.ModelField]

### _async method_ `solve(self, **params)` {#Dependent-solve}

- **参数**

  - `**params` (Any)

- **返回**

  - dict[str, Any]
