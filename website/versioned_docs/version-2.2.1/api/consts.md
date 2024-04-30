---
sidebar_position: 9
description: nonebot.consts 模块
---

# nonebot.consts

本模块包含了 NoneBot 事件处理过程中使用到的常量。

## _var_ `RECEIVE_KEY` {#RECEIVE-KEY}

- **类型:** Literal['\_receive\_{id}']

- **说明:** `receive` 存储 key

## _var_ `LAST_RECEIVE_KEY` {#LAST-RECEIVE-KEY}

- **类型:** Literal['\_last\_receive']

- **说明:** `last_receive` 存储 key

## _var_ `ARG_KEY` {#ARG-KEY}

- **类型:** Literal['{key}']

- **说明:** `arg` 存储 key

## _var_ `REJECT_TARGET` {#REJECT-TARGET}

- **类型:** Literal['\_current\_target']

- **说明:** 当前 `reject` 目标存储 key

## _var_ `REJECT_CACHE_TARGET` {#REJECT-CACHE-TARGET}

- **类型:** Literal['\_next\_target']

- **说明:** 下一个 `reject` 目标存储 key

## _var_ `PREFIX_KEY` {#PREFIX-KEY}

- **类型:** Literal['\_prefix']

- **说明:** 命令前缀存储 key

## _var_ `CMD_KEY` {#CMD-KEY}

- **类型:** Literal['command']

- **说明:** 命令元组存储 key

## _var_ `RAW_CMD_KEY` {#RAW-CMD-KEY}

- **类型:** Literal['raw\_command']

- **说明:** 命令文本存储 key

## _var_ `CMD_ARG_KEY` {#CMD-ARG-KEY}

- **类型:** Literal['command\_arg']

- **说明:** 命令参数存储 key

## _var_ `CMD_START_KEY` {#CMD-START-KEY}

- **类型:** Literal['command\_start']

- **说明:** 命令开头存储 key

## _var_ `CMD_WHITESPACE_KEY` {#CMD-WHITESPACE-KEY}

- **类型:** Literal['command\_whitespace']

- **说明:** 命令与参数间空白符存储 key

## _var_ `SHELL_ARGS` {#SHELL-ARGS}

- **类型:** Literal['\_args']

- **说明:** shell 命令 parse 后参数字典存储 key

## _var_ `SHELL_ARGV` {#SHELL-ARGV}

- **类型:** Literal['\_argv']

- **说明:** shell 命令原始参数列表存储 key

## _var_ `REGEX_MATCHED` {#REGEX-MATCHED}

- **类型:** Literal['\_matched']

- **说明:** 正则匹配结果存储 key

## _var_ `STARTSWITH_KEY` {#STARTSWITH-KEY}

- **类型:** Literal['\_startswith']

- **说明:** 响应触发前缀 key

## _var_ `ENDSWITH_KEY` {#ENDSWITH-KEY}

- **类型:** Literal['\_endswith']

- **说明:** 响应触发后缀 key

## _var_ `FULLMATCH_KEY` {#FULLMATCH-KEY}

- **类型:** Literal['\_fullmatch']

- **说明:** 响应触发完整消息 key

## _var_ `KEYWORD_KEY` {#KEYWORD-KEY}

- **类型:** Literal['\_keyword']

- **说明:** 响应触发关键字 key
