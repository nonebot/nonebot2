---
sidebar_position: 0
description: nonebot.dependencies 模块
---

# nonebot.dependencies

本模块模块实现了依赖注入的定义与处理。

## _abstract class_ `Param(*args, validate=False, **kwargs)` {#Param}

- **说明**

  依赖注入的基本单元 —— 参数。

  继承自 `pydantic.fields.FieldInfo`，用于描述参数信息（不包括参数名）。

- **参数**

  - `*args`

  - `validate` (bool)

  - `**kwargs` (Any)

## _class_ `Dependent(<auto>)` {#Dependent}

- **说明:** 依赖注入容器

- **参数**

  - `call`: 依赖注入的可调用对象，可以是任何 Callable 对象

  - `pre_checkers`: 依赖注入解析前的参数检查

  - `params`: 具名参数列表

  - `parameterless`: 匿名参数列表

  - `allow_types`: 允许的参数类型

### _staticmethod_ `parse_params(call, allow_types)` {#Dependent-parse-params}

- **参数**

  - `call` (\_DependentCallable[R])

  - `allow_types` (tuple[type[Param], ...])

- **返回**

  - tuple[ModelField, ...]

### _staticmethod_ `parse_parameterless(parameterless, allow_types)` {#Dependent-parse-parameterless}

- **参数**

  - `parameterless` (tuple[Any, ...])

  - `allow_types` (tuple[type[Param], ...])

- **返回**

  - tuple[Param, ...]

### _classmethod_ `parse(*, call, parameterless=None, allow_types)` {#Dependent-parse}

- **参数**

  - `call` (\_DependentCallable[R])

  - `parameterless` (Iterable[Any] | None)

  - `allow_types` (Iterable[type[Param]])

- **返回**

  - Dependent[R]

### _async method_ `check(**params)` {#Dependent-check}

- **参数**

  - `**params` (Any)

- **返回**

  - None

### _async method_ `solve(**params)` {#Dependent-solve}

- **参数**

  - `**params` (Any)

- **返回**

  - dict[str, Any]
