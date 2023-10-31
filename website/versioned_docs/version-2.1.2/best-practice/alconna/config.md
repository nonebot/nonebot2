---
sidebar_position: 4
description: 配置项
---

# 配置项

## alconna_auto_send_output

- **类型**: `bool`
- **默认值**: `False`

是否全局启用输出信息自动发送，不启用则会在触特殊内置选项后仍然将解析结果传递至响应器。

## alconna_use_command_start

- **类型**: `bool`
- **默认值**: `False`

是否读取 Nonebot 的配置项 `COMMAND_START` 来作为全局的 Alconna 命令前缀

## alconna_auto_completion

- **类型**: `bool`
- **默认值**: `False`

是否全局启用命令自动补全，启用后会在参数缺失或触发 `--comp` 选项时自自动启用交互式补全。

## alconna_use_origin

- **类型**: `bool`
- **默认值**: `False`

是否全局使用原始消息 (即未经过 to_me 等处理的), 该选项会影响到 Alconna 的匹配行为。

## alconna_use_param

- **类型**: `bool`
- **默认值**: `True`

是否使用特制的 Param 提供更好的依赖注入，该选项不会对使用依赖注入函数形式造成影响

## alconna_use_command_sep

- **类型**: `bool`
- **默认值**: `False`

是否读取 Nonebot 的配置项 `COMMAND_SEP` 来作为全局的 Alconna 命令分隔符

## alconna_global_extensions

- **类型**: `List[str]`
- **默认值**: `[]`

全局加载的扩展, 路径以 . 分隔, 如 foo.bar.baz:DemoExtension
