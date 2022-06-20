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

## _class_ `Dependent(*, call, pre_checkers=None, params=None, parameterless=None, allow_types=None)` {#Dependent}

- **说明**

  依赖注入容器

- **参数**

  - `call` ((\*Any, \*\*Any) -> Any): 依赖注入的可调用对象，可以是任何 Callable 对象

  - `pre_checkers` (list[[Param](#Param)] | None): 依赖注入解析前的参数检查

  - `params` (list[pydantic.fields.ModelField] | None): 具名参数列表

  - `parameterless` (list[[Param](#Param)] | None): 匿名参数列表

  - `allow_types` (list[Type[[Param](#Param)]] | None): 允许的参数类型

### _method_ `append_parameterless(self, value)` {#Dependent-append_parameterless}

- **参数**

  - `value` (Any)

- **返回**

  - None

### _classmethod_ `parse(cls, *, call, parameterless=None, allow_types=None)` {#Dependent-parse}

- **参数**

  - `call` ((\*Any, \*\*Any) -> Any)

  - `parameterless` (list[Any] | None)

  - `allow_types` (list[Type[[Param](#Param)]] | None)

- **返回**

  - (~ T)

### _method_ `parse_param(self, name, param)` {#Dependent-parse_param}

- **参数**

  - `name` (str)

  - `param` (inspect.Parameter)

- **返回**

  - [Param](#Param)

### _method_ `parse_parameterless(self, value)` {#Dependent-parse_parameterless}

- **参数**

  - `value` (Any)

- **返回**

  - [Param](#Param)

### _method_ `prepend_parameterless(self, value)` {#Dependent-prepend_parameterless}

- **参数**

  - `value` (Any)

- **返回**

  - None

### _async method_ `solve(self, **params)` {#Dependent-solve}

- **参数**

  - `**params` (Any)

- **返回**

  - dict[str, Any]
