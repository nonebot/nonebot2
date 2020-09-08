#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import asyncio
from itertools import product

from pygtrie import CharTrie

from nonebot import get_driver
from nonebot.log import logger
from nonebot.utils import run_sync
from nonebot.typing import Bot, Any, Dict, Event, Union, Tuple, NoReturn, RuleChecker


class Rule:
    __slots__ = ("checkers",)

    def __init__(self, *checkers: RuleChecker) -> None:
        self.checkers = list(checkers)

    async def __call__(self, bot: Bot, event: Event, state: dict) -> bool:
        results = await asyncio.gather(
            *map(lambda c: c(bot, event, state), self.checkers))
        return all(results)

    def __and__(self, other: Union["Rule", RuleChecker]) -> "Rule":
        checkers = [*self.checkers]
        if isinstance(other, Rule):
            checkers.extend(other.checkers)
        elif asyncio.iscoroutinefunction(other):
            checkers.append(other)
        else:
            checkers.append(run_sync(other))
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
    TrieRule.add_prefix(msg, (msg,))

    async def _startswith(bot: Bot, event: Event, state: dict) -> bool:
        return msg in state["_prefix"]

    return Rule(_startswith)


def endswith(msg: str) -> Rule:
    TrieRule.add_suffix(msg, (msg,))

    async def _endswith(bot: Bot, event: Event, state: dict) -> bool:
        return msg in state["_suffix"]

    return Rule(_endswith)


def keyword(msg: str) -> Rule:

    async def _keyword(bot: Bot, event: Event, state: dict) -> bool:
        return bool(event.plain_text and msg in event.plain_text)

    return Rule(_keyword)


def command(command: Tuple[str, ...]) -> Rule:
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
    pattern = re.compile(regex, flags)

    async def _regex(bot: Bot, event: Event, state: dict) -> bool:
        return bool(pattern.search(str(event.message)))

    return Rule(_regex)


def to_me() -> Rule:

    async def _to_me(bot: Bot, event: Event, state: dict) -> bool:
        return bool(event.to_me)

    return Rule(_to_me)
