"""本模块是 {ref}`nonebot.matcher.Matcher.rule` 的类型定义。

每个事件响应器 {ref}`nonebot.matcher.Matcher` 拥有一个匹配规则 {ref}`nonebot.rule.Rule`
其中是 `RuleChecker` 的集合，只有当所有 `RuleChecker` 检查结果为 `True` 时继续运行。

FrontMatter:
    sidebar_position: 5
    description: nonebot.rule 模块
"""

import re
import shlex
from itertools import product
from argparse import Namespace
from typing_extensions import TypedDict
from argparse import ArgumentParser as ArgParser
from typing import Any, List, Tuple, Union, Optional, Sequence, NamedTuple

from pygtrie import CharTrie

from nonebot import get_driver
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.exception import ParserExit
from nonebot.internal.rule import Rule as Rule
from nonebot.adapters import Bot, Event, Message, MessageSegment
from nonebot.params import (
    Command,
    EventToMe,
    EventType,
    CommandArg,
    EventMessage,
    EventPlainText,
)
from nonebot.consts import (
    CMD_KEY,
    PREFIX_KEY,
    REGEX_DICT,
    SHELL_ARGS,
    SHELL_ARGV,
    CMD_ARG_KEY,
    RAW_CMD_KEY,
    REGEX_GROUP,
    CMD_START_KEY,
    REGEX_MATCHED,
)

CMD_RESULT = TypedDict(
    "CMD_RESULT",
    {
        "command": Optional[Tuple[str, ...]],
        "raw_command": Optional[str],
        "command_arg": Optional[Message[MessageSegment]],
        "command_start": Optional[str],
    },
)

TRIE_VALUE = NamedTuple(
    "TRIE_VALUE", [("command_start", str), ("command", Tuple[str, ...])]
)


class TrieRule:
    prefix: CharTrie = CharTrie()

    @classmethod
    def add_prefix(cls, prefix: str, value: TRIE_VALUE) -> None:
        if prefix in cls.prefix:
            logger.warning(f'Duplicated prefix rule "{prefix}"')
            return
        cls.prefix[prefix] = value

    @classmethod
    def get_value(cls, bot: Bot, event: Event, state: T_State) -> CMD_RESULT:
        prefix = CMD_RESULT(
            command=None, raw_command=None, command_arg=None, command_start=None
        )
        state[PREFIX_KEY] = prefix
        if event.get_type() != "message":
            return prefix

        message = event.get_message()
        message_seg: MessageSegment = message[0]
        if message_seg.is_text():
            segment_text = str(message_seg).lstrip()
            pf = cls.prefix.longest_prefix(segment_text)
            if pf:
                value: TRIE_VALUE = pf.value
                prefix[RAW_CMD_KEY] = pf.key
                prefix[CMD_START_KEY] = value.command_start
                prefix[CMD_KEY] = value.command
                msg = message.copy()
                msg.pop(0)
                new_message = msg.__class__(segment_text[len(pf.key) :].lstrip())
                for new_segment in reversed(new_message):
                    msg.insert(0, new_segment)
                prefix[CMD_ARG_KEY] = msg

        return prefix


class StartswithRule:
    """检查消息纯文本是否以指定字符串开头。

    参数:
        msg: 指定消息开头字符串元组
        ignorecase: 是否忽略大小写
    """

    __slots__ = ("msg", "ignorecase")

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
    """匹配消息纯文本开头。

    参数:
        msg: 指定消息开头字符串元组
        ignorecase: 是否忽略大小写
    """
    if isinstance(msg, str):
        msg = (msg,)

    return Rule(StartswithRule(msg, ignorecase))


class EndswithRule:
    """检查消息纯文本是否以指定字符串结尾。

    参数:
        msg: 指定消息结尾字符串元组
        ignorecase: 是否忽略大小写
    """

    __slots__ = ("msg", "ignorecase")

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
    """匹配消息纯文本结尾。

    参数:
        msg: 指定消息开头字符串元组
        ignorecase: 是否忽略大小写
    """
    if isinstance(msg, str):
        msg = (msg,)

    return Rule(EndswithRule(msg, ignorecase))


class FullmatchRule:
    """检查消息纯文本是否与指定字符串全匹配。

    参数:
        msg: 指定消息全匹配字符串元组
        ignorecase: 是否忽略大小写
    """

    __slots__ = ("msg", "ignorecase")

    def __init__(self, msg: Tuple[str, ...], ignorecase: bool = False):
        self.msg = frozenset(map(str.casefold, msg) if ignorecase else msg)
        self.ignorecase = ignorecase

    async def __call__(
        self, type_: str = EventType(), text: str = EventPlainText()
    ) -> bool:
        return (
            type_ == "message"
            and (text.casefold() if self.ignorecase else text) in self.msg
        )


def fullmatch(msg: Union[str, Tuple[str, ...]], ignorecase: bool = False) -> Rule:
    """完全匹配消息。

    参数:
        msg: 指定消息全匹配字符串元组
        ignorecase: 是否忽略大小写
    """
    if isinstance(msg, str):
        msg = (msg,)

    return Rule(FullmatchRule(msg, ignorecase))


class KeywordsRule:
    """检查消息纯文本是否包含指定关键字。

    参数:
        keywords: 指定关键字元组
    """

    __slots__ = ("keywords",)

    def __init__(self, *keywords: str):
        self.keywords = keywords

    async def __call__(
        self, type: str = EventType(), text: str = EventPlainText()
    ) -> bool:
        if type != "message":
            return False
        return bool(text and any(keyword in text for keyword in self.keywords))


def keyword(*keywords: str) -> Rule:
    """匹配消息纯文本关键词。

    参数:
        keywords: 指定关键字元组
    """

    return Rule(KeywordsRule(*keywords))


class CommandRule:
    """检查消息是否为指定命令。

    参数:
        cmds: 指定命令元组列表
    """

    __slots__ = ("cmds",)

    def __init__(self, cmds: List[Tuple[str, ...]]):
        self.cmds = cmds

    async def __call__(self, cmd: Optional[Tuple[str, ...]] = Command()) -> bool:
        return cmd in self.cmds

    def __repr__(self):
        return f"<Command {self.cmds}>"


def command(*cmds: Union[str, Tuple[str, ...]]) -> Rule:
    """匹配消息命令。

    根据配置里提供的 {ref}``command_start` <nonebot.config.Config.command_start>`,
    {ref}``command_sep` <nonebot.config.Config.command_sep>` 判断消息是否为命令。

    可以通过 {ref}`nonebot.params.Command` 获取匹配成功的命令（例: `("test",)`），
    通过 {ref}`nonebot.params.RawCommand` 获取匹配成功的原始命令文本（例: `"/test"`），
    通过 {ref}`nonebot.params.CommandArg` 获取匹配成功的命令参数。

    参数:
        cmds: 命令文本或命令元组

    用法:
        使用默认 `command_start`, `command_sep` 配置

        命令 `("test",)` 可以匹配: `/test` 开头的消息
        命令 `("test", "sub")` 可以匹配: `/test.sub` 开头的消息

    :::tip 提示
    命令内容与后续消息间无需空格!
    :::
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
                TrieRule.add_prefix(f"{start}{command[0]}", TRIE_VALUE(start, command))
        else:
            for start, sep in product(command_start, command_sep):
                TrieRule.add_prefix(
                    f"{start}{sep.join(command)}", TRIE_VALUE(start, command)
                )

    return Rule(CommandRule(commands))


class ArgumentParser(ArgParser):
    """`shell_like` 命令参数解析器，解析出错时不会退出程序。

    用法:
        用法与 `argparse.ArgumentParser` 相同，
        参考文档: [argparse](https://docs.python.org/3/library/argparse.html)
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
    """检查消息是否为指定 shell 命令。

    参数:
        cmds: 指定命令元组列表
        parser: 可选参数解析器
    """

    __slots__ = ("cmds", "parser")

    def __init__(self, cmds: List[Tuple[str, ...]], parser: Optional[ArgumentParser]):
        self.cmds = cmds
        self.parser = parser

    async def __call__(
        self,
        state: T_State,
        cmd: Optional[Tuple[str, ...]] = Command(),
        msg: Optional[Message] = CommandArg(),
    ) -> bool:
        if cmd in self.cmds and msg is not None:
            message = str(msg)
            state[SHELL_ARGV] = shlex.split(message)
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
    """匹配 `shell_like` 形式的消息命令。

    根据配置里提供的 {ref}``command_start` <nonebot.config.Config.command_start>`,
    {ref}``command_sep` <nonebot.config.Config.command_sep>` 判断消息是否为命令。

    可以通过 {ref}`nonebot.params.Command` 获取匹配成功的命令（例: `("test",)`），
    通过 {ref}`nonebot.params.RawCommand` 获取匹配成功的原始命令文本（例: `"/test"`），
    通过 {ref}`nonebot.params.ShellCommandArgv` 获取解析前的参数列表（例: `["arg", "-h"]`），
    通过 {ref}`nonebot.params.ShellCommandArgs` 获取解析后的参数字典（例: `{"arg": "arg", "h": True}`）。

    :::warning 警告
    如果参数解析失败，则通过 {ref}`nonebot.params.ShellCommandArgs`
    获取的将是 {ref}`nonebot.exception.ParserExit` 异常。
    :::

    参数:
        cmds: 命令文本或命令元组
        parser: {ref}`nonebot.rule.ArgumentParser` 对象

    用法:
        使用默认 `command_start`, `command_sep` 配置，更多示例参考 `argparse` 标准库文档。

        ```python
        from nonebot.rule import ArgumentParser

        parser = ArgumentParser()
        parser.add_argument("-a", action="store_true")

        rule = shell_command("ls", parser=parser)
        ```

    :::tip 提示
    命令内容与后续消息间无需空格!
    :::
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
                TrieRule.add_prefix(f"{start}{command[0]}", TRIE_VALUE(start, command))
        else:
            for start, sep in product(command_start, command_sep):
                TrieRule.add_prefix(
                    f"{start}{sep.join(command)}", TRIE_VALUE(start, command)
                )

    return Rule(ShellCommandRule(commands, parser))


class RegexRule:
    """检查消息字符串是否符合指定正则表达式。

    参数:
        regex: 正则表达式
        flags: 正则表达式标记
    """

    __slots__ = ("regex", "flags")

    def __init__(self, regex: str, flags: int = 0):
        self.regex = regex
        self.flags = flags

    async def __call__(
        self,
        state: T_State,
        type: str = EventType(),
        msg: Message = EventMessage(),
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
    """匹配符合正则表达式的消息字符串。

    可以通过 {ref}`nonebot.params.RegexMatched` 获取匹配成功的字符串，
    通过 {ref}`nonebot.params.RegexGroup` 获取匹配成功的 group 元组，
    通过 {ref}`nonebot.params.RegexDict` 获取匹配成功的 group 字典。

    参数:
        regex: 正则表达式
        flags: 正则表达式标记

    :::tip 提示
    正则表达式匹配使用 search 而非 match，如需从头匹配请使用 `r"^xxx"` 来确保匹配开头
    :::

    :::tip 提示
    正则表达式匹配使用 `EventMessage` 的 `str` 字符串，而非 `EventMessage` 的 `PlainText` 纯文本字符串
    :::
    """

    return Rule(RegexRule(regex, flags))


class ToMeRule:
    """检查事件是否与机器人有关。"""

    __slots__ = ()

    async def __call__(self, to_me: bool = EventToMe()) -> bool:
        return to_me


def to_me() -> Rule:
    """匹配与机器人有关的事件。"""

    return Rule(ToMeRule())


__autodoc__ = {
    "Rule": True,
    "Rule.__call__": True,
    "TrieRule": False,
    "ArgumentParser.exit": False,
    "ArgumentParser.parse_args": False,
}
