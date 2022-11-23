---
sidebar_position: 1
description: nonebot.dependencies.utils 模块
---

# nonebot.dependencies.utils

## _def_ `get_typed_signature(call)` {#get_typed_signature}

- **说明**

  获取可调用对象签名

- **参数**

  - `call` ((\*Any, \*\*Any) -> Any)

- **返回**

  - inspect.Signature

## _def_ `get_typed_annotation(param, globalns)` {#get_typed_annotation}

- **说明**

  获取参数的类型注解

- **参数**

  - `param` (inspect.Parameter)

  - `globalns` (dict[str, Any])

- **返回**

  - Any

## _def_ `check_field_type(field, value)` {#check_field_type}

- **参数**

  - `field` (pydantic.fields.ModelField)

  - `value` ((~ V))

- **返回**

  - (~ V)
