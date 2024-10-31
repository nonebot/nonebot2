---
mdx:
  format: md
sidebar_position: 16
description: nonebot.compat 模块
---

# nonebot.compat

本模块为 Pydantic 版本兼容层模块

为兼容 Pydantic V1 与 V2 版本，定义了一系列兼容函数与类供使用。

## _var_ `Required` {#Required}

- **类型:** untyped

- **说明:** Alias of Ellipsis for compatibility with pydantic v1

## _library-attr_ `PydanticUndefined` {#PydanticUndefined}

- **说明:** Pydantic Undefined object

## _library-attr_ `PydanticUndefinedType` {#PydanticUndefinedType}

- **说明:** Pydantic Undefined type

## _var_ `DEFAULT_CONFIG` {#DEFAULT-CONFIG}

- **类型:** untyped

- **说明:** Default config for validations

## _class_ `FieldInfo(default=PydanticUndefined, **kwargs)` {#FieldInfo}

- **说明:** FieldInfo class with extra property for compatibility with pydantic v1

- **参数**

  - `default` (Any)

  - `**kwargs` (Any)

### _property_ `extra` {#FieldInfo-extra}

- **类型:** dict[str, Any]

- **说明**

  Extra data that is not part of the standard pydantic fields.

  For compatibility with pydantic v1.

## _class_ `ModelField(<auto>)` {#ModelField}

- **说明:** ModelField class for compatibility with pydantic v1

- **参数**

  auto

### _instance-var_ `name` {#ModelField-name}

- **类型:** str

- **说明:** The name of the field.

### _instance-var_ `annotation` {#ModelField-annotation}

- **类型:** Any

- **说明:** The annotation of the field.

### _instance-var_ `field_info` {#ModelField-field-info}

- **类型:** FieldInfo

- **说明:** The FieldInfo of the field.

### _classmethod_ `construct(name, annotation, field_info=None)` {#ModelField-construct}

- **说明:** Construct a ModelField from given infos.

- **参数**

  - `name` (str)

  - `annotation` (Any)

  - `field_info` (FieldInfo | None)

- **返回**

  - Self

### _method_ `get_default()` {#ModelField-get-default}

- **说明:** Get the default value of the field.

- **参数**

  empty

- **返回**

  - Any

### _method_ `validate_value(value)` {#ModelField-validate-value}

- **说明:** Validate the value pass to the field.

- **参数**

  - `value` (Any)

- **返回**

  - Any

## _def_ `extract_field_info(field_info)` {#extract-field-info}

- **说明:** Get FieldInfo init kwargs from a FieldInfo instance.

- **参数**

  - `field_info` (BaseFieldInfo)

- **返回**

  - dict[str, Any]

## _def_ `model_fields(model)` {#model-fields}

- **说明:** Get field list of a model.

- **参数**

  - `model` (type[BaseModel])

- **返回**

  - list[ModelField]

## _def_ `model_config(model)` {#model-config}

- **说明:** Get config of a model.

- **参数**

  - `model` (type[BaseModel])

- **返回**

  - Any

## _def_ `model_dump(model, include=None, exclude=None, by_alias=False, exclude_unset=False, exclude_defaults=False, exclude_none=False)` {#model-dump}

- **参数**

  - `model` (BaseModel)

  - `include` (set[str] | None)

  - `exclude` (set[str] | None)

  - `by_alias` (bool)

  - `exclude_unset` (bool)

  - `exclude_defaults` (bool)

  - `exclude_none` (bool)

- **返回**

  - dict[str, Any]

## _def_ `type_validate_python(type_, data)` {#type-validate-python}

- **说明:** Validate data with given type.

- **参数**

  - `type_` (type[T])

  - `data` (Any)

- **返回**

  - T

## _def_ `type_validate_json(type_, data)` {#type-validate-json}

- **说明:** Validate JSON with given type.

- **参数**

  - `type_` (type[T])

  - `data` (str | bytes)

- **返回**

  - T

## _def_ `custom_validation(class_)` {#custom-validation}

- **说明:** Use pydantic v1 like validator generator in pydantic v2

- **参数**

  - `class_` (type[CVC])

- **返回**

  - type[CVC]
