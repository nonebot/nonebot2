---
sidebar_position: 9
description: nonebot.consts 模块
---

# nonebot.consts

本模块包含了 NoneBot 事件处理过程中使用到的常量。

## _var_ `RECEIVE_KEY` {#RECEIVE_KEY}

- **类型:** Literal['_receive_{id}']

- **说明:** `receive` 存储 key

## _var_ `LAST_RECEIVE_KEY` {#LAST_RECEIVE_KEY}

- **类型:** Literal['_last_receive']

- **说明:** `last_receive` 存储 key

## _var_ `ARG_KEY` {#ARG_KEY}

- **类型:** Literal['{key}']

- **说明:** `arg` 存储 key

## _var_ `REJECT_TARGET` {#REJECT_TARGET}

- **类型:** Literal['_current_target']

- **说明:** 当前 `reject` 目标存储 key

## _var_ `REJECT_CACHE_TARGET` {#REJECT_CACHE_TARGET}

- **类型:** Literal['_next_target']

- **说明:** 下一个 `reject` 目标存储 key

## _var_ `PREFIX_KEY` {#PREFIX_KEY}

- **类型:** Literal['_prefix']

- **说明:** 命令前缀存储 key

## _var_ `CMD_KEY` {#CMD_KEY}

- **类型:** Literal['command']

- **说明:** 命令元组存储 key

## _var_ `RAW_CMD_KEY` {#RAW_CMD_KEY}

- **类型:** Literal['raw_command']

- **说明:** 命令文本存储 key

## _var_ `CMD_ARG_KEY` {#CMD_ARG_KEY}

- **类型:** Literal['command_arg']

- **说明:** 命令参数存储 key

## _var_ `CMD_START_KEY` {#CMD_START_KEY}

- **类型:** Literal['command_start']

- **说明:** 命令开头存储 key

## _var_ `SHELL_ARGS` {#SHELL_ARGS}

- **类型:** Literal['_args']

- **说明:** shell 命令 parse 后参数字典存储 key

## _var_ `SHELL_ARGV` {#SHELL_ARGV}

- **类型:** Literal['_argv']

- **说明:** shell 命令原始参数列表存储 key

## _var_ `REGEX_MATCHED` {#REGEX_MATCHED}

- **类型:** Literal['_matched']

- **说明:** 正则匹配结果存储 key

## _var_ `REGEX_GROUP` {#REGEX_GROUP}

- **类型:** Literal['_matched_groups']

- **说明:** 正则匹配 group 元组存储 key

## _var_ `REGEX_DICT` {#REGEX_DICT}

- **类型:** Literal['_matched_dict']

- **说明:** 正则匹配 group 字典存储 key

## _var_ `STARTSWITH_KEY` {#STARTSWITH_KEY}

- **类型:** Literal['_startswith']

- **说明:** 响应触发前缀 key

## _var_ `ENDSWITH_KEY` {#ENDSWITH_KEY}

- **类型:** Literal['_endswith']

- **说明:** 响应触发后缀 key

## _var_ `FULLMATCH_KEY` {#FULLMATCH_KEY}

- **类型:** Literal['_fullmatch']

- **说明:** 响应触发完整消息 key

## _var_ `KEYWORD_KEY` {#KEYWORD_KEY}

- **类型:** Literal['_keyword']

- **说明:** 响应触发关键字 key
