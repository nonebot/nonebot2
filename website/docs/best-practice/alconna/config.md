---
sidebar_position: 4
description: 配置项
---

# 配置项

## alconna_auto_send_output

- **类型**: `bool`
- **默认值**: `False`

是否全局启用输出信息自动发送，不启用则会在触发特殊内置选项后仍然将解析结果传递至响应器。

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

是否全局使用原始消息 (即未经过 to_me 等处理的)，该选项会影响到 Alconna 的匹配行为。

## alconna_use_command_sep

- **类型**: `bool`
- **默认值**: `False`

是否读取 Nonebot 的配置项 `COMMAND_SEP` 来作为全局的 Alconna 命令分隔符。

## alconna_global_extensions

- **类型**: `List[str]`
- **默认值**: `[]`

全局加载的扩展，路径以 . 分隔，如 `foo.bar.baz:DemoExtension`。

## alconna_context_style

- **类型**: `Optional[Literal["bracket", "parentheses"]]`
- **默认值**: `None`

全局命令上下文插值的风格，None 为关闭，bracket 为 `{...}`，parentheses 为 `$(...)`。

## alconna_enable_saa_patch

- **类型**: `bool`
- **默认值**: `False`

是否启用 SAA 补丁。

## alconna_apply_filehost

- **类型**: `bool`
- **默认值**: `False`

是否启用文件托管。

## alconna_apply_fetch_targets

- **类型**: `bool`
- **默认值**: `False`

是否启动时拉取一次发送对象列表。
