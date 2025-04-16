---
sidebar_position: 4
description: 配置项
---

# 配置项

## alconna_auto_send_output

- **类型**: `bool | None`
- **默认值**: `None`

是否全局启用输出信息自动发送，不启用则会在触发特殊内置选项后仍然将解析结果传递至响应器。

## alconna_use_command_start

- **类型**: `bool`
- **默认值**: `False`

是否读取 Nonebot 的配置项 `COMMAND_START` 来作为全局的 Alconna 命令前缀

## alconna_global_completion

- **类型**: [`CompConfig | None`](./matcher.mdx#补全会话)
- **默认值**: `None`

全局的补全会话配置 (不代表全局启用补全会话)。

## alconna_use_origin

- **类型**: `bool`
- **默认值**: `False`

是否全局使用原始消息 (即未经过 to_me 等处理的)，该选项会影响到 Alconna 的匹配行为。

## alconna_use_command_sep

- **类型**: `bool`
- **默认值**: `False`

是否读取 Nonebot 的配置项 `COMMAND_SEP` 来作为全局的 Alconna 命令分隔符。

## alconna_global_extensions

- **类型**: `list[str]`
- **默认值**: `[]`

全局加载的扩展，其读取路径以 . 分隔，如 `foo.bar.baz:DemoExtension`。

对于内置扩展，路径为 `nonebot_plugin_alconna.builtins.extensions` 下的模块名，如 `ReplyMergeExtension`，可以使用 `@` 来缩写路径，
如 `@reply:ReplyMergeExtension`。

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

是否启动时拉取一次[发送对象](./uniseg/utils.mdx#发送对象)列表。

## alconna_builtin_plugins

- **类型**: `set[str]`
- **默认值**: `set()`

需要加载的内置插件列表。

## alconna_conflict_resolver

- **类型**: `Literal["raise", "default", "ignore", "replace"]`
- **默认值**: `"default"`

命令冲突解决策略，决定当不同插件之间或者同一插件之间存在两个以上相同的命令时的处理方式：

- `default`: 默认处理方式，保留两个命令
- `raise`: 抛出异常
- `ignore`: 忽略较新的命令
- `replace`: 替换较旧的命令

## alconna_response_self

- **类型**: `bool`
- **默认值**: `False`

是否让响应器处理由 bot 自身发送的消息。
