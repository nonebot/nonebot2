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
from typing import Any, Set, List, Tuple, Union, NoReturn, Optional, Sequence

from pygtrie import CharTrie

from nonebot import get_driver
from nonebot.log import logger
from nonebot.dependencies import Dependent
from nonebot.exception import ParserExit, SkippedException
from nonebot.adapters import Bot, Event, Message, MessageSegment
from nonebot.typing import T_State, T_RuleChecker, T_DependencyCache
from nonebot.consts import (
    CMD_KEY,
    PREFIX_KEY,
    REGEX_DICT,
    SHELL_ARGS,
    SHELL_ARGV,
    CMD_ARG_KEY,
    RAW_CMD_KEY,
    REGEX_GROUP,
    REGEX_MATCHED,
)
from nonebot.params import (
    State,
    Command,
    BotParam,
    EventToMe,
    EventType,
    EventParam,
    StateParam,
    DependParam,
    DefaultParam,
    EventMessage,
    EventPlainText,
)

CMD_RESULT = TypedDict(
    "CMD_RESULT",
    {
        "command": Optional[Tuple[str, ...]],
        "raw_command": Optional[str],
        "command_arg": Optional[Message[MessageSegment]],
    },
)


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
        DependParam,
        BotParam,
        EventParam,
        StateParam,
        DefaultParam,
    ]

    def __init__(self, *checkers: Union[T_RuleChecker, Dependent[bool]]) -> None:
        """
        :参数:

          * ``*checkers: Union[T_RuleChecker, Dependent[bool]]``: RuleChecker

        """
        self.checkers: Set[Dependent[bool]] = set(
            checker
            if isinstance(checker, Dependent)
            else Dependent[bool].parse(
                call=checker, allow_types=self.HANDLER_PARAM_TYPES
            )
            for checker in checkers
        )
        """
        :说明:

          存储 ``RuleChecker``

        :类型:

          * ``Set[Dependent[bool]]``
        """

    async def __call__(
        self,
        bot: Bot,
        event: Event,
        state: T_State,
        stack: Optional[AsyncExitStack] = None,
        dependency_cache: Optional[T_DependencyCache] = None,
    ) -> bool:
        """
        :说明:

          检查是否符合所有规则

        :参数:

          * ``bot: Bot``: Bot 对象
          * ``event: Event``: Event 对象
          * ``state: T_State``: 当前 State
          * ``stack: Optional[AsyncExitStack]``: 异步上下文栈
          * ``dependency_cache: Optional[CacheDict[T_Handler, Any]]``: 依赖缓存

        :返回:

          - ``bool``
        """
        if not self.checkers:
            return True
        try:
            results = await asyncio.gather(
                *(
                    checker(
                        bot=bot,
                        event=event,
                        state=state,
                        stack=stack,
                        dependency_cache=dependency_cache,
                    )
                    for checker in self.checkers
                )
            )
        except SkippedException:
            return False
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

    @classmethod
    def add_prefix(cls, prefix: str, value: Any):
        if prefix in cls.prefix:
            logger.warning(f'Duplicated prefix rule "{prefix}"')
            return
        cls.prefix[prefix] = value

    @classmethod
    def get_value(cls, bot: Bot, event: Event, state: T_State) -> CMD_RESULT:
        prefix = CMD_RESULT(command=None, raw_command=None, command_arg=None)
        state[PREFIX_KEY] = prefix
        if event.get_type() != "message":
            return prefix

        message = event.get_message()
        message_seg: MessageSegment = message[0]
        if message_seg.is_text():
            segment_text = str(message_seg).lstrip()
            pf = cls.prefix.longest_prefix(segment_text)
            prefix[RAW_CMD_KEY] = pf.key
            prefix[CMD_KEY] = pf.value
            if pf.key:
                msg = message.copy()
                msg.pop(0)
                new_message = msg.__class__(segment_text[len(pf.key) :].lstrip())
                for new_segment in reversed(new_message):
                    msg.insert(0, new_segment)
                prefix[CMD_ARG_KEY] = msg

        return prefix


class StartswithRule:
    def __init__(self, msg: Tuple[str, ...], ignorecase: bool = False):
        self.msg = msg
        self.ignorecase = ignorecase

    async def __call__(
        self, type: str = EventType(), text: str = EventPlainText()
    ) -> Any:
        if type != "message":
            return False
        return bool(
            re.match(
                f"^(?:{'|'.join(re.escape(prefix) for prefix in self.msg)})",
                text,
                re.IGNORECASE if self.ignorecase else 0,
            )
        )


def startswith(msg: Union[str, Tuple[str, ...]], ignorecase: bool = False) -> Rule:
    """
    :说明:

      匹配消息开头

    :参数:

      * ``msg: str``: 消息开头字符串
    """
    if isinstance(msg, str):
        msg = (msg,)

    return Rule(StartswithRule(msg, ignorecase))


class EndswithRule:
    def __init__(self, msg: Tuple[str, ...], ignorecase: bool = False):
        self.msg = msg
        self.ignorecase = ignorecase

    async def __call__(
        self, type: str = EventType(), text: str = EventPlainText()
    ) -> Any:
        if type != "message":
            return False
        return bool(
            re.search(
                f"(?:{'|'.join(re.escape(prefix) for prefix in self.msg)})$",
                text,
                re.IGNORECASE if self.ignorecase else 0,
            )
        )


def endswith(msg: Union[str, Tuple[str, ...]], ignorecase: bool = False) -> Rule:
    """
    :说明:

      匹配消息结尾

    :参数:

      * ``msg: str``: 消息结尾字符串
    """
    if isinstance(msg, str):
        msg = (msg,)

    return Rule(EndswithRule(msg, ignorecase))


class KeywordsRule:
    def __init__(self, *keywords: str):
        self.keywords = keywords

    async def __call__(
        self, type: str = EventType(), text: str = EventPlainText()
    ) -> bool:
        if type != "message":
            return False
        return bool(text and any(keyword in text for keyword in self.keywords))


def keyword(*keywords: str) -> Rule:
    """
    :说明:

      匹配消息关键词

    :参数:

      * ``*keywords: str``: 关键词
    """

    return Rule(KeywordsRule(*keywords))


class CommandRule:
    def __init__(self, cmds: List[Tuple[str, ...]]):
        self.cmds = cmds

    async def __call__(self, cmd: Optional[Tuple[str, ...]] = Command()) -> bool:
        return cmd in self.cmds

    def __repr__(self):
        return f"<Command {self.cmds}>"


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
    commands: List[Tuple[str, ...]] = []
    for command in cmds:
        if isinstance(command, str):
            command = (command,)

        commands.append(command)

        if len(command) == 1:
            for start in command_start:
                TrieRule.add_prefix(f"{start}{command[0]}", command)
        else:
            for start, sep in product(command_start, command_sep):
                TrieRule.add_prefix(f"{start}{sep.join(command)}", command)

    return Rule(CommandRule(commands))


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
        raise ParserExit(
            status=status, message=message or getattr(self, "message", None)
        )

    def parse_args(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[Namespace] = None,
    ) -> Namespace:
        setattr(self, "message", "")
        return super().parse_args(args=args, namespace=namespace)  # type: ignore


class ShellCommandRule:
    def __init__(self, cmds: List[Tuple[str, ...]], parser: Optional[ArgumentParser]):
        self.cmds = cmds
        self.parser = parser

    async def __call__(
        self,
        cmd: Optional[Tuple[str, ...]] = Command(),
        msg: Message = EventMessage(),
        state: T_State = State(),
    ) -> bool:
        if cmd in self.cmds:
            message = str(msg)
            strip_message = message[len(state[PREFIX_KEY][RAW_CMD_KEY]) :].lstrip()
            state[SHELL_ARGV] = shlex.split(strip_message)
            if self.parser:
                try:
                    args = self.parser.parse_args(state[SHELL_ARGV])
                    state[SHELL_ARGS] = args
                except ParserExit as e:
                    state[SHELL_ARGS] = e
            return True
        else:
            return False


def shell_command(
    *cmds: Union[str, Tuple[str, ...]], parser: Optional[ArgumentParser] = None
) -> Rule:
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
    if parser is not None and not isinstance(parser, ArgumentParser):
        raise TypeError("`parser` must be an instance of nonebot.rule.ArgumentParser")

    config = get_driver().config
    command_start = config.command_start
    command_sep = config.command_sep
    commands: List[Tuple[str, ...]] = []
    for command in cmds:
        if isinstance(command, str):
            command = (command,)

        commands.append(command)

        if len(command) == 1:
            for start in command_start:
                TrieRule.add_prefix(f"{start}{command[0]}", command)
        else:
            for start, sep in product(command_start, command_sep):
                TrieRule.add_prefix(f"{start}{sep.join(command)}", command)

    return Rule(ShellCommandRule(commands, parser))


class RegexRule:
    def __init__(self, regex: str, flags: int = 0):
        self.regex = regex
        self.flags = flags

    async def __call__(
        self,
        type: str = EventType(),
        msg: Message = EventMessage(),
        state: T_State = State(),
    ) -> bool:
        if type != "message":
            return False
        matched = re.search(self.regex, str(msg), self.flags)
        if matched:
            state[REGEX_MATCHED] = matched.group()
            state[REGEX_GROUP] = matched.groups()
            state[REGEX_DICT] = matched.groupdict()
            return True
        else:
            return False


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

    return Rule(RegexRule(regex, flags))


class ToMeRule:
    async def __call__(self, to_me: bool = EventToMe()) -> bool:
        return to_me


def to_me() -> Rule:
    """
    :说明:

      通过 ``event.is_tome()`` 判断事件是否与机器人有关

    :参数:

      * 无
    """

    return Rule(ToMeRule())
