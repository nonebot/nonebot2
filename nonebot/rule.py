#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则
====

每个事件响应器 ``Matcher`` 拥有一个匹配规则 ``Rule`` ，其中是 **异步** ``RuleChecker`` 的集合，只有当所有 ``RuleChecker`` 检查结果为 ``True`` 时继续运行。

\:\:\:tip 提示
``RuleChecker`` 既可以是 async function 也可以是 sync function，但在最终会被 ``nonebot.utils.run_sync`` 转换为 async function
\:\:\:
"""

import re
import asyncio
from itertools import product

from pygtrie import CharTrie

from nonebot import get_driver
from nonebot.log import logger
from nonebot.utils import run_sync
from nonebot.typing import Bot, Any, Dict, Event, Union, Tuple, NoReturn, Optional, Callable, Awaitable, RuleChecker


class Rule:
    """
    :说明:
      ``Matcher`` 规则类，当事件传递时，在 ``Matcher`` 运行前进行检查。
    :示例:

    .. code-block:: python

        Rule(async_function) & sync_function
        # 等价于
        from nonebot.utils import run_sync
        Rule(async_function, run_sync(sync_function))
    """
    __slots__ = ("checkers",)

    def __init__(
            self, *checkers: Callable[[Bot, Event, dict],
                                      Awaitable[bool]]) -> None:
        """
        :参数:
          * ``*checkers: Callable[[Bot, Event, dict], Awaitable[bool]]``: **异步** RuleChecker
        """
        self.checkers = set(checkers)
        """
        :说明:
          存储 ``RuleChecker``
        :类型:
          * ``Set[Callable[[Bot, Event, dict], Awaitable[bool]]]``
        """

    async def __call__(self, bot: Bot, event: Event, state: dict) -> bool:
        """
        :说明:
          检查是否符合所有规则
        :参数:
          * ``bot: Bot``: Bot 对象
          * ``event: Event``: Event 对象
          * ``state: dict``: 当前 State
        :返回:
          - ``bool``
        """
        results = await asyncio.gather(
            *map(lambda c: c(bot, event, state), self.checkers))
        return all(results)

    def __and__(self, other: Optional[Union["Rule", RuleChecker]]) -> "Rule":
        checkers = self.checkers.copy()
        if other is None:
            return self
        elif isinstance(other, Rule):
            checkers |= other.checkers
        elif asyncio.iscoroutinefunction(other):
            checkers.add(other)  # type: ignore
        else:
            checkers.add(run_sync(other))
        return Rule(*checkers)

    def __or__(self, other) -> NoReturn:
        raise RuntimeError("Or operation between rules is not allowed.")


class TrieRule:
    prefix: CharTrie = CharTrie()
    suffix: CharTrie = CharTrie()

    @classmethod
    def add_prefix(cls, prefix: str, value: Any):
        if prefix in cls.prefix:
            logger.warning(f'Duplicated prefix rule "{prefix}"')
            return
        cls.prefix[prefix] = value

    @classmethod
    def add_suffix(cls, suffix: str, value: Any):
        if suffix[::-1] in cls.suffix:
            logger.warning(f'Duplicated suffix rule "{suffix}"')
            return
        cls.suffix[suffix[::-1]] = value

    @classmethod
    def get_value(cls, bot: Bot, event: Event,
                  state: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        if event.type != "message":
            state["_prefix"] = {"raw_command": None, "command": None}
            state["_suffix"] = {"raw_command": None, "command": None}
            return {
                "raw_command": None,
                "command": None
            }, {
                "raw_command": None,
                "command": None
            }

        prefix = None
        suffix = None
        message = event.message[0]
        if message.type == "text":
            prefix = cls.prefix.longest_prefix(message.data["text"].lstrip())
        message_r = event.message[-1]
        if message_r.type == "text":
            suffix = cls.suffix.longest_prefix(
                message_r.data["text"].rstrip()[::-1])

        state["_prefix"] = {
            "raw_command": prefix.key,
            "command": prefix.value
        } if prefix else {
            "raw_command": None,
            "command": None
        }
        state["_suffix"] = {
            "raw_command": suffix.key,
            "command": suffix.value
        } if suffix else {
            "raw_command": None,
            "command": None
        }

        return ({
            "raw_command": prefix.key,
            "command": prefix.value
        } if prefix else {
            "raw_command": None,
            "command": None
        }, {
            "raw_command": suffix.key,
            "command": suffix.value
        } if suffix else {
            "raw_command": None,
            "command": None
        })


def startswith(msg: str) -> Rule:
    """
    :说明:
      匹配消息开头
    :参数:
      * ``msg: str``: 消息开头字符串
    """

    async def _startswith(bot: Bot, event: Event, state: dict) -> bool:
        return event.plain_text.startswith(msg)

    return Rule(_startswith)


def endswith(msg: str) -> Rule:
    """
    :说明:
      匹配消息结尾
    :参数:
      * ``msg: str``: 消息结尾字符串
    """

    async def _endswith(bot: Bot, event: Event, state: dict) -> bool:
        return event.plain_text.endswith(msg)

    return Rule(_endswith)


def keyword(msg: str) -> Rule:
    """
    :说明:
      匹配消息关键词
    :参数:
      * ``msg: str``: 关键词
    """

    async def _keyword(bot: Bot, event: Event, state: dict) -> bool:
        return bool(event.plain_text and msg in event.plain_text)

    return Rule(_keyword)


def command(command: Tuple[str, ...]) -> Rule:
    """
    :说明:
      命令形式匹配，根据配置里提供的 ``command_start``, ``command_sep`` 判断消息是否为命令。
    :参数:
      * ``command: Tuples[str, ...]``: 命令内容
    :示例:
      使用默认 ``command_start``, ``command_sep`` 配置

      命令 ``("test",)`` 可以匹配：``/test`` 开头的消息
      命令 ``("test", "sub")`` 可以匹配”``/test.sub`` 开头的消息

    \:\:\:tip 提示
    命令内容与后续消息间无需空格！
    \:\:\:
    """

    config = get_driver().config
    command_start = config.command_start
    command_sep = config.command_sep
    if len(command) == 1:
        for start in command_start:
            TrieRule.add_prefix(f"{start}{command[0]}", command)
    else:
        for start, sep in product(command_start, command_sep):
            TrieRule.add_prefix(f"{start}{sep.join(command)}", command)

    async def _command(bot: Bot, event: Event, state: dict) -> bool:
        return command == state["_prefix"]["command"]

    return Rule(_command)


def regex(regex: str, flags: Union[int, re.RegexFlag] = 0) -> Rule:
    """
    :说明:
      根据正则表达式进行匹配
    :参数:
      * ``regex: str``: 正则表达式
      * ``flags: Union[int, re.RegexFlag]``: 正则标志
    """

    pattern = re.compile(regex, flags)

    async def _regex(bot: Bot, event: Event, state: dict) -> bool:
        return bool(pattern.search(str(event.message)))

    return Rule(_regex)


def to_me() -> Rule:
    """
    :说明:
      通过 ``event.to_me`` 判断消息是否是发送给机器人
    :参数:
      * 无
    """

    async def _to_me(bot: Bot, event: Event, state: dict) -> bool:
        return bool(event.to_me)

    return Rule(_to_me)
