r"""
规则
====

每个事件响应器 ``Matcher`` 拥有一个匹配规则 ``Rule`` ，其中是 **异步** ``RuleChecker`` 的集合，只有当所有 ``RuleChecker`` 检查结果为 ``True`` 时继续运行。

\:\:\:tip 提示
``RuleChecker`` 既可以是 async function 也可以是 sync function，但在最终会被 ``nonebot.utils.run_sync`` 转换为 async function
\:\:\:
"""

import re
import shlex
import asyncio
from itertools import product
from argparse import Namespace, ArgumentParser as ArgParser
from typing import Any, Dict, Union, Tuple, Optional, Callable, Sequence, NoReturn, Awaitable, TYPE_CHECKING

from pygtrie import CharTrie

from nonebot import get_driver
from nonebot.log import logger
from nonebot.utils import run_sync
from nonebot.exception import ParserExit
from nonebot.typing import T_State, T_RuleChecker

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event, MessageSegment


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
        self, *checkers: Callable[["Bot", "Event", T_State],
                                  Awaitable[bool]]) -> None:
        """
        :参数:

          * ``*checkers: Callable[[Bot, Event, T_State], Awaitable[bool]]``: **异步** RuleChecker

        """
        self.checkers = set(checkers)
        """
        :说明:

          存储 ``RuleChecker``

        :类型:

          * ``Set[Callable[[Bot, Event, T_State], Awaitable[bool]]]``
        """

    async def __call__(self, bot: "Bot", event: "Event",
                       state: T_State) -> bool:
        """
        :说明:

          检查是否符合所有规则

        :参数:

          * ``bot: Bot``: Bot 对象
          * ``event: Event``: Event 对象
          * ``state: T_State``: 当前 State

        :返回:

          - ``bool``
        """
        results = await asyncio.gather(
            *map(lambda c: c(bot, event, state), self.checkers))
        return all(results)

    def __and__(self, other: Optional[Union["Rule", T_RuleChecker]]) -> "Rule":
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
    def get_value(cls, bot: "Bot", event: "Event",
                  state: T_State) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        if event.get_type() != "message":
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
        message = event.get_message()
        message_seg = message[0]
        if message_seg.is_text():
            prefix = cls.prefix.longest_prefix(str(message_seg).lstrip())
        message_seg_r = message[-1]
        if message_seg_r.is_text():
            suffix = cls.suffix.longest_prefix(
                str(message_seg_r).rstrip()[::-1])

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

    async def _startswith(bot: "Bot", event: "Event", state: T_State) -> bool:
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

    async def _endswith(bot: "Bot", event: "Event", state: T_State) -> bool:
        if event.get_type() != "message":
            return False
        text = event.get_plaintext()
        return bool(pattern.match(text))

    return Rule(_endswith)


def keyword(*keywords: str) -> Rule:
    """
    :说明:

      匹配消息关键词

    :参数:

      * ``*keywords: str``: 关键词
    """

    async def _keyword(bot: "Bot", event: "Event", state: T_State) -> bool:
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

    async def _command(bot: "Bot", event: "Event", state: T_State) -> bool:
        return state["_prefix"]["command"] in commands

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

    def exit(self, status=0, message=None):
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

    async def _shell_command(bot: "Bot", event: "Event",
                             state: T_State) -> bool:
        if state["_prefix"]["command"] in commands:
            message = str(event.get_message())
            strip_message = message[len(state["_prefix"]["raw_command"]
                                       ):].lstrip()
            state["argv"] = shlex.split(strip_message)
            if parser:
                try:
                    args = parser.parse_args(state["argv"])
                    state["args"] = args
                except ParserExit as e:
                    state["args"] = e
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

    async def _regex(bot: "Bot", event: "Event", state: T_State) -> bool:
        if event.get_type() != "message":
            return False
        matched = pattern.search(str(event.get_message()))
        if matched:
            state["_matched"] = matched.group()
            state["_matched_groups"] = matched.groups()
            state["_matched_dict"] = matched.groupdict()
            return True
        else:
            return False

    return Rule(_regex)


def to_me() -> Rule:
    """
    :说明:

      通过 ``event.is_tome()`` 判断事件是否与机器人有关

    :参数:

      * 无
    """

    async def _to_me(bot: "Bot", event: "Event", state: T_State) -> bool:
        return event.is_tome()

    return Rule(_to_me)
