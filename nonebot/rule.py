r"""
规则
====

每个事件响应器 ``Matcher`` 拥有一个匹配规则 ``Rule`` ，其中是 ``RuleChecker`` 的集合，只有当所有 ``RuleChecker`` 检查结果为 ``True`` 时继续运行。

\:\:\:tip 提示
``RuleChecker`` 既可以是 async function 也可以是 sync function
\:\:\:
"""

import re
import shlex
import asyncio
from itertools import product
from argparse import Namespace
from contextlib import AsyncExitStack
from typing_extensions import TypedDict
from argparse import ArgumentParser as ArgParser
from typing import (Any, Dict, List, Type, Tuple, Union, Callable, NoReturn,
                    Optional, Sequence)

from pygtrie import CharTrie

from nonebot.log import logger
from nonebot.handler import Handler
from nonebot import params, get_driver
from nonebot.exception import ParserExit
from nonebot.typing import T_State, T_RuleChecker
from nonebot.adapters import Bot, Event, MessageSegment

PREFIX_KEY = "_prefix"
SUFFIX_KEY = "_suffix"
CMD_KEY = "command"
RAW_CMD_KEY = "raw_command"
CMD_RESULT = TypedDict("CMD_RESULT", {
    "command": Optional[Tuple[str, ...]],
    "raw_command": Optional[str]
})

SHELL_ARGS = "_args"
SHELL_ARGV = "_argv"

REGEX_MATCHED = "_matched"
REGEX_GROUP = "_matched_groups"
REGEX_DICT = "_matched_dict"


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

    HANDLER_PARAM_TYPES = [
        params.BotParam, params.EventParam, params.StateParam,
        params.DefaultParam
    ]

    def __init__(self, *checkers: Union[T_RuleChecker, Handler]) -> None:
        """
        :参数:

          * ``*checkers: Union[T_RuleChecker, Handler]``: RuleChecker

        """
        self.checkers = set(
            checker if isinstance(checker, Handler) else Handler(
                checker, allow_types=self.HANDLER_PARAM_TYPES)
            for checker in checkers)
        """
        :说明:

          存储 ``RuleChecker``

        :类型:

          * ``Set[Handler]``
        """

    async def __call__(
        self,
        bot: Bot,
        event: Event,
        state: T_State,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[Dict[Callable[..., Any],
                                        Any]] = None) -> bool:
        """
        :说明:

          检查是否符合所有规则

        :参数:

          * ``bot: Bot``: Bot 对象
          * ``event: Event``: Event 对象
          * ``state: T_State``: 当前 State
          * ``stack: Optional[AsyncExitStack]``: 异步上下文栈
          * ``dependency_cache: Optional[Dict[Callable[..., Any], Any]]``: 依赖缓存

        :返回:

          - ``bool``
        """
        if not self.checkers:
            return True
        results = await asyncio.gather(
            *(checker(bot=bot,
                      event=event,
                      state=state,
                      _stack=stack,
                      _dependency_cache=dependency_cache)
              for checker in self.checkers))
        return all(results)

    def __and__(self, other: Optional[Union["Rule", T_RuleChecker]]) -> "Rule":
        if other is None:
            return self
        elif isinstance(other, Rule):
            return Rule(*self.checkers, *other.checkers)
        else:
            return Rule(*self.checkers, other)

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
                  state: T_State) -> Tuple[CMD_RESULT, CMD_RESULT]:
        prefix = CMD_RESULT(command=None, raw_command=None)
        suffix = CMD_RESULT(command=None, raw_command=None)
        state[PREFIX_KEY] = prefix
        state[SUFFIX_KEY] = suffix
        if event.get_type() != "message":
            return prefix, suffix

        message = event.get_message()
        message_seg: MessageSegment = message[0]
        if message_seg.is_text():
            pf = cls.prefix.longest_prefix(str(message_seg).lstrip())
            prefix[RAW_CMD_KEY] = pf.key
            prefix[CMD_KEY] = pf.value
        message_seg_r: MessageSegment = message[-1]
        if message_seg_r.is_text():
            sf = cls.suffix.longest_prefix(str(message_seg_r).rstrip()[::-1])
            suffix[RAW_CMD_KEY] = sf.key
            suffix[CMD_KEY] = sf.value

        return prefix, suffix


def startswith(msg: Union[str, Tuple[str, ...]],
               ignorecase: bool = False) -> Rule:
    """
    :说明:

      匹配消息开头

    :参数:

      * ``msg: str``: 消息开头字符串
    """
    if isinstance(msg, str):
        msg = (msg,)

    pattern = re.compile(
        f"^(?:{'|'.join(re.escape(prefix) for prefix in msg)})",
        re.IGNORECASE if ignorecase else 0)

    async def _startswith(bot: Bot, event: Event, state: T_State) -> bool:
        if event.get_type() != "message":
            return False
        text = event.get_plaintext()
        return bool(pattern.match(text))

    return Rule(_startswith)


def endswith(msg: Union[str, Tuple[str, ...]],
             ignorecase: bool = False) -> Rule:
    """
    :说明:

      匹配消息结尾

    :参数:

      * ``msg: str``: 消息结尾字符串
    """
    if isinstance(msg, str):
        msg = (msg,)

    pattern = re.compile(
        f"(?:{'|'.join(re.escape(prefix) for prefix in msg)})$",
        re.IGNORECASE if ignorecase else 0)

    async def _endswith(bot: Bot, event: Event, state: T_State) -> bool:
        if event.get_type() != "message":
            return False
        text = event.get_plaintext()
        return bool(pattern.search(text))

    return Rule(_endswith)


def keyword(*keywords: str) -> Rule:
    """
    :说明:

      匹配消息关键词

    :参数:

      * ``*keywords: str``: 关键词
    """

    async def _keyword(event: Event) -> bool:
        if event.get_type() != "message":
            return False
        text = event.get_plaintext()
        return bool(text and any(keyword in text for keyword in keywords))

    return Rule(_keyword)


def command(*cmds: Union[str, Tuple[str, ...]]) -> Rule:
    r"""
    :说明:

      命令形式匹配，根据配置里提供的 ``command_start``, ``command_sep`` 判断消息是否为命令。

      可以通过 ``state["_prefix"]["command"]`` 获取匹配成功的命令（例：``("test",)``），通过 ``state["_prefix"]["raw_command"]`` 获取匹配成功的原始命令文本（例：``"/test"``）。

    :参数:

      * ``*cmds: Union[str, Tuple[str, ...]]``: 命令内容

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
    commands = list(cmds)
    for index, command in enumerate(commands):
        if isinstance(command, str):
            commands[index] = command = (command,)

        if len(command) == 1:
            for start in command_start:
                TrieRule.add_prefix(f"{start}{command[0]}", command)
        else:
            for start, sep in product(command_start, command_sep):
                TrieRule.add_prefix(f"{start}{sep.join(command)}", command)

    async def _command(state: T_State) -> bool:
        return state[PREFIX_KEY][CMD_KEY] in commands

    return Rule(_command)


class ArgumentParser(ArgParser):
    """
    :说明:

      ``shell_like`` 命令参数解析器，解析出错时不会退出程序。
    """

    def _print_message(self, message, file=None):
        old_message: str = getattr(self, "message", "")
        if old_message:
            old_message += "\n"
        old_message += message
        setattr(self, "message", old_message)

    def exit(self, status: int = 0, message: Optional[str] = None):
        raise ParserExit(status=status,
                         message=message or getattr(self, "message", None))

    def parse_args(self,
                   args: Optional[Sequence[str]] = None,
                   namespace: Optional[Namespace] = None) -> Namespace:
        setattr(self, "message", "")
        return super().parse_args(args=args,
                                  namespace=namespace)  # type: ignore


def shell_command(*cmds: Union[str, Tuple[str, ...]],
                  parser: Optional[ArgumentParser] = None) -> Rule:
    r"""
    :说明:

      支持 ``shell_like`` 解析参数的命令形式匹配，根据配置里提供的 ``command_start``, ``command_sep`` 判断消息是否为命令。

      可以通过 ``state["_prefix"]["command"]`` 获取匹配成功的命令（例：``("test",)``），通过 ``state["_prefix"]["raw_command"]`` 获取匹配成功的原始命令文本（例：``"/test"``）。

      可以通过 ``state["argv"]`` 获取用户输入的原始参数列表

      添加 ``parser`` 参数后, 可以自动处理消息并将结果保存在 ``state["args"]`` 中。

    :参数:

      * ``*cmds: Union[str, Tuple[str, ...]]``: 命令内容
      * ``parser: Optional[ArgumentParser]``: ``nonebot.rule.ArgumentParser`` 对象

    :示例:

      使用默认 ``command_start``, ``command_sep`` 配置，更多示例参考 ``argparse`` 标准库文档。

    .. code-block:: python

        from nonebot.rule import ArgumentParser

        parser = ArgumentParser()
        parser.add_argument("-a", action="store_true")

        rule = shell_command("ls", parser=parser)

    \:\:\:tip 提示
    命令内容与后续消息间无需空格！
    \:\:\:
    """
    if not isinstance(parser, ArgumentParser):
        raise TypeError(
            "`parser` must be an instance of nonebot.rule.ArgumentParser")

    config = get_driver().config
    command_start = config.command_start
    command_sep = config.command_sep
    commands = list(cmds)
    for index, command in enumerate(commands):
        if isinstance(command, str):
            commands[index] = command = (command,)

        if len(command) == 1:
            for start in command_start:
                TrieRule.add_prefix(f"{start}{command[0]}", command)
        else:
            for start, sep in product(command_start, command_sep):
                TrieRule.add_prefix(f"{start}{sep.join(command)}", command)

    async def _shell_command(event: Event, state: T_State) -> bool:
        if state[PREFIX_KEY][CMD_KEY] in commands:
            message = str(event.get_message())
            strip_message = message[len(state[PREFIX_KEY][RAW_CMD_KEY]
                                       ):].lstrip()
            state[SHELL_ARGV] = shlex.split(strip_message)
            if parser:
                try:
                    args = parser.parse_args(state[SHELL_ARGV])
                    state[SHELL_ARGS] = args
                except ParserExit as e:
                    state[SHELL_ARGS] = e
            return True
        else:
            return False

    return Rule(_shell_command)


def regex(regex: str, flags: Union[int, re.RegexFlag] = 0) -> Rule:
    r"""
    :说明:

      根据正则表达式进行匹配。

      可以通过 ``state["_matched"]`` ``state["_matched_groups"]`` ``state["_matched_dict"]``
      获取正则表达式匹配成功的文本。

    :参数:

      * ``regex: str``: 正则表达式
      * ``flags: Union[int, re.RegexFlag]``: 正则标志

    \:\:\:tip 提示
    正则表达式匹配使用 search 而非 match，如需从头匹配请使用 ``r"^xxx"`` 来确保匹配开头
    \:\:\:
    """

    pattern = re.compile(regex, flags)

    async def _regex(event: Event, state: T_State) -> bool:
        if event.get_type() != "message":
            return False
        matched = pattern.search(str(event.get_message()))
        if matched:
            state[REGEX_MATCHED] = matched.group()
            state[REGEX_GROUP] = matched.groups()
            state[REGEX_DICT] = matched.groupdict()
            return True
        else:
            return False

    return Rule(_regex)


async def _to_me(event: Event) -> bool:
    return event.is_tome()


def to_me() -> Rule:
    """
    :说明:

      通过 ``event.is_tome()`` 判断事件是否与机器人有关

    :参数:

      * 无
    """

    return Rule(_to_me)
