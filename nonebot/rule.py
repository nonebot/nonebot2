"""本模块是 {ref}`nonebot.matcher.Matcher.rule` 的类型定义。

每个{ref}`事件响应器 <nonebot.matcher.Matcher>`拥有一个
{ref}`nonebot.rule.Rule`，其中是 `RuleChecker` 的集合。
只有当所有 `RuleChecker` 检查结果为 `True` 时继续运行。

FrontMatter:
    sidebar_position: 5
    description: nonebot.rule 模块
"""

import re
import shlex
from argparse import Action
from gettext import gettext
from argparse import ArgumentError
from contextvars import ContextVar
from itertools import chain, product
from argparse import Namespace as Namespace
from argparse import ArgumentParser as ArgParser
from typing import (
    IO,
    TYPE_CHECKING,
    List,
    Type,
    Tuple,
    Union,
    TypeVar,
    Optional,
    Sequence,
    TypedDict,
    NamedTuple,
    cast,
    overload,
)

from pygtrie import CharTrie

from nonebot import get_driver
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.exception import ParserExit
from nonebot.internal.rule import Rule as Rule
from nonebot.adapters import Bot, Event, Message, MessageSegment
from nonebot.params import Command, EventToMe, CommandArg, CommandWhitespace
from nonebot.consts import (
    CMD_KEY,
    PREFIX_KEY,
    SHELL_ARGS,
    SHELL_ARGV,
    CMD_ARG_KEY,
    KEYWORD_KEY,
    RAW_CMD_KEY,
    ENDSWITH_KEY,
    CMD_START_KEY,
    FULLMATCH_KEY,
    REGEX_MATCHED,
    STARTSWITH_KEY,
    CMD_WHITESPACE_KEY,
)

T = TypeVar("T")


class CMD_RESULT(TypedDict):
    command: Optional[Tuple[str, ...]]
    raw_command: Optional[str]
    command_arg: Optional[Message]
    command_start: Optional[str]
    command_whitespace: Optional[str]


class TRIE_VALUE(NamedTuple):
    command_start: str
    command: Tuple[str, ...]


parser_message: ContextVar[str] = ContextVar("parser_message")


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
            command=None,
            raw_command=None,
            command_arg=None,
            command_start=None,
            command_whitespace=None,
        )
        state[PREFIX_KEY] = prefix
        if event.get_type() != "message":
            return prefix

        message = event.get_message()
        message_seg: MessageSegment = message[0]
        if message_seg.is_text():
            segment_text = str(message_seg).lstrip()
            if pf := cls.prefix.longest_prefix(segment_text):
                value: TRIE_VALUE = pf.value
                prefix[RAW_CMD_KEY] = pf.key
                prefix[CMD_START_KEY] = value.command_start
                prefix[CMD_KEY] = value.command

                msg = message.copy()
                msg.pop(0)

                # check whitespace
                arg_str = segment_text[len(pf.key) :]
                arg_str_stripped = arg_str.lstrip()
                has_arg = arg_str_stripped or msg
                if (
                    has_arg
                    and (stripped_len := len(arg_str) - len(arg_str_stripped)) > 0
                ):
                    prefix[CMD_WHITESPACE_KEY] = arg_str[:stripped_len]

                # construct command arg
                if arg_str_stripped:
                    new_message = msg.__class__(arg_str_stripped)
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

    def __repr__(self) -> str:
        return f"Startswith(msg={self.msg}, ignorecase={self.ignorecase})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, StartswithRule)
            and frozenset(self.msg) == frozenset(other.msg)
            and self.ignorecase == other.ignorecase
        )

    def __hash__(self) -> int:
        return hash((frozenset(self.msg), self.ignorecase))

    async def __call__(self, event: Event, state: T_State) -> bool:
        try:
            text = event.get_plaintext()
        except Exception:
            return False
        if match := re.match(
            f"^(?:{'|'.join(re.escape(prefix) for prefix in self.msg)})",
            text,
            re.IGNORECASE if self.ignorecase else 0,
        ):
            state[STARTSWITH_KEY] = match.group()
            return True
        return False


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

    def __repr__(self) -> str:
        return f"Endswith(msg={self.msg}, ignorecase={self.ignorecase})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, EndswithRule)
            and frozenset(self.msg) == frozenset(other.msg)
            and self.ignorecase == other.ignorecase
        )

    def __hash__(self) -> int:
        return hash((frozenset(self.msg), self.ignorecase))

    async def __call__(self, event: Event, state: T_State) -> bool:
        try:
            text = event.get_plaintext()
        except Exception:
            return False
        if match := re.search(
            f"(?:{'|'.join(re.escape(suffix) for suffix in self.msg)})$",
            text,
            re.IGNORECASE if self.ignorecase else 0,
        ):
            state[ENDSWITH_KEY] = match.group()
            return True
        return False


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
        self.msg = tuple(map(str.casefold, msg) if ignorecase else msg)
        self.ignorecase = ignorecase

    def __repr__(self) -> str:
        return f"Fullmatch(msg={self.msg}, ignorecase={self.ignorecase})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, FullmatchRule)
            and frozenset(self.msg) == frozenset(other.msg)
            and self.ignorecase == other.ignorecase
        )

    def __hash__(self) -> int:
        return hash((frozenset(self.msg), self.ignorecase))

    async def __call__(self, event: Event, state: T_State) -> bool:
        try:
            text = event.get_plaintext()
        except Exception:
            return False
        if not text:
            return False
        text = text.casefold() if self.ignorecase else text
        if text in self.msg:
            state[FULLMATCH_KEY] = text
            return True
        return False


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

    def __repr__(self) -> str:
        return f"Keywords(keywords={self.keywords})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, KeywordsRule) and frozenset(
            self.keywords
        ) == frozenset(other.keywords)

    def __hash__(self) -> int:
        return hash(frozenset(self.keywords))

    async def __call__(self, event: Event, state: T_State) -> bool:
        try:
            text = event.get_plaintext()
        except Exception:
            return False
        if not text:
            return False
        if key := next((k for k in self.keywords if k in text), None):
            state[KEYWORD_KEY] = key
            return True
        return False


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
        force_whitespace: 是否强制命令后必须有指定空白符
    """

    __slots__ = ("cmds", "force_whitespace")

    def __init__(
        self,
        cmds: List[Tuple[str, ...]],
        force_whitespace: Optional[Union[str, bool]] = None,
    ):
        self.cmds = tuple(cmds)
        self.force_whitespace = force_whitespace

    def __repr__(self) -> str:
        return f"Command(cmds={self.cmds})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CommandRule) and frozenset(self.cmds) == frozenset(
            other.cmds
        )

    def __hash__(self) -> int:
        return hash((frozenset(self.cmds),))

    async def __call__(
        self,
        cmd: Optional[Tuple[str, ...]] = Command(),
        cmd_arg: Optional[Message] = CommandArg(),
        cmd_whitespace: Optional[str] = CommandWhitespace(),
    ) -> bool:
        if cmd not in self.cmds:
            return False
        if self.force_whitespace is None or not cmd_arg:
            return True
        if isinstance(self.force_whitespace, str):
            return self.force_whitespace == cmd_whitespace
        return self.force_whitespace == (cmd_whitespace is not None)


def command(
    *cmds: Union[str, Tuple[str, ...]],
    force_whitespace: Optional[Union[str, bool]] = None,
) -> Rule:
    """匹配消息命令。

    根据配置里提供的 {ref}``command_start` <nonebot.config.Config.command_start>`,
    {ref}``command_sep` <nonebot.config.Config.command_sep>` 判断消息是否为命令。

    可以通过 {ref}`nonebot.params.Command` 获取匹配成功的命令（例: `("test",)`），
    通过 {ref}`nonebot.params.RawCommand` 获取匹配成功的原始命令文本（例: `"/test"`），
    通过 {ref}`nonebot.params.CommandArg` 获取匹配成功的命令参数。

    参数:
        cmds: 命令文本或命令元组
        force_whitespace: 是否强制命令后必须有指定空白符

    用法:
        使用默认 `command_start`, `command_sep` 配置情况下：

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

    return Rule(CommandRule(commands, force_whitespace))


class ArgumentParser(ArgParser):
    """`shell_like` 命令参数解析器，解析出错时不会退出程序。

    支持 {ref}`nonebot.adapters.Message` 富文本解析。

    用法:
        用法与 `argparse.ArgumentParser` 相同，
        参考文档: [argparse](https://docs.python.org/3/library/argparse.html)
    """

    if TYPE_CHECKING:

        @overload
        def parse_known_args(
            self,
            args: Optional[Sequence[Union[str, MessageSegment]]] = None,
            namespace: None = None,
        ) -> Tuple[Namespace, List[Union[str, MessageSegment]]]:
            ...

        @overload
        def parse_known_args(
            self, args: Optional[Sequence[Union[str, MessageSegment]]], namespace: T
        ) -> Tuple[T, List[Union[str, MessageSegment]]]:
            ...

        @overload
        def parse_known_args(
            self, *, namespace: T
        ) -> Tuple[T, List[Union[str, MessageSegment]]]:
            ...

        def parse_known_args(
            self,
            args: Optional[Sequence[Union[str, MessageSegment]]] = None,
            namespace: Optional[T] = None,
        ) -> Tuple[Union[Namespace, T], List[Union[str, MessageSegment]]]:
            ...

    @overload
    def parse_args(
        self,
        args: Optional[Sequence[Union[str, MessageSegment]]] = None,
        namespace: None = None,
    ) -> Namespace:
        ...

    @overload
    def parse_args(
        self, args: Optional[Sequence[Union[str, MessageSegment]]], namespace: T
    ) -> T:
        ...

    @overload
    def parse_args(self, *, namespace: T) -> T:
        ...

    def parse_args(
        self,
        args: Optional[Sequence[Union[str, MessageSegment]]] = None,
        namespace: Optional[T] = None,
    ) -> Union[Namespace, T]:
        result, argv = self.parse_known_args(args, namespace)
        if argv:
            msg = gettext("unrecognized arguments: %s")
            self.error(msg % " ".join(map(str, argv)))
        return cast(Union[Namespace, T], result)

    def _parse_optional(
        self, arg_string: Union[str, MessageSegment]
    ) -> Optional[Tuple[Optional[Action], str, Optional[str]]]:
        return (
            super()._parse_optional(arg_string) if isinstance(arg_string, str) else None
        )

    def _print_message(self, message: str, file: Optional[IO[str]] = None):
        if (msg := parser_message.get(None)) is not None:
            parser_message.set(msg + message)
        else:
            super()._print_message(message, file)

    def exit(self, status: int = 0, message: Optional[str] = None):
        if message:
            self._print_message(message)
        raise ParserExit(status=status, message=parser_message.get(None))


class ShellCommandRule:
    """检查消息是否为指定 shell 命令。

    参数:
        cmds: 指定命令元组列表
        parser: 可选参数解析器
    """

    __slots__ = ("cmds", "parser")

    def __init__(self, cmds: List[Tuple[str, ...]], parser: Optional[ArgumentParser]):
        self.cmds = tuple(cmds)
        self.parser = parser

    def __repr__(self) -> str:
        return f"ShellCommand(cmds={self.cmds}, parser={self.parser})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ShellCommandRule)
            and frozenset(self.cmds) == frozenset(other.cmds)
            and self.parser is other.parser
        )

    def __hash__(self) -> int:
        return hash((frozenset(self.cmds), self.parser))

    async def __call__(
        self,
        state: T_State,
        cmd: Optional[Tuple[str, ...]] = Command(),
        msg: Optional[Message] = CommandArg(),
    ) -> bool:
        if cmd not in self.cmds or msg is None:
            return False

        state[SHELL_ARGV] = list(
            chain.from_iterable(
                shlex.split(str(seg)) if cast(MessageSegment, seg).is_text() else (seg,)
                for seg in msg
            )
        )

        if self.parser:
            t = parser_message.set("")
            try:
                args = self.parser.parse_args(state[SHELL_ARGV])
                state[SHELL_ARGS] = args
            except ArgumentError as e:  # pragma: py-gte-39
                state[SHELL_ARGS] = ParserExit(status=2, message=str(e))
            except ParserExit as e:
                state[SHELL_ARGS] = e
            finally:
                parser_message.reset(t)
        return True


def shell_command(
    *cmds: Union[str, Tuple[str, ...]], parser: Optional[ArgumentParser] = None
) -> Rule:
    """匹配 `shell_like` 形式的消息命令。

    根据配置里提供的 {ref}``command_start` <nonebot.config.Config.command_start>`,
    {ref}``command_sep` <nonebot.config.Config.command_sep>` 判断消息是否为命令。

    可以通过 {ref}`nonebot.params.Command` 获取匹配成功的命令
    （例: `("test",)`），
    通过 {ref}`nonebot.params.RawCommand` 获取匹配成功的原始命令文本
    （例: `"/test"`），
    通过 {ref}`nonebot.params.ShellCommandArgv` 获取解析前的参数列表
    （例: `["arg", "-h"]`），
    通过 {ref}`nonebot.params.ShellCommandArgs` 获取解析后的参数字典
    （例: `{"arg": "arg", "h": True}`）。

    :::warning 警告
    如果参数解析失败，则通过 {ref}`nonebot.params.ShellCommandArgs`
    获取的将是 {ref}`nonebot.exception.ParserExit` 异常。
    :::

    参数:
        cmds: 命令文本或命令元组
        parser: {ref}`nonebot.rule.ArgumentParser` 对象

    用法:
        使用默认 `command_start`, `command_sep` 配置，更多示例参考
        [argparse](https://docs.python.org/3/library/argparse.html) 标准库文档。

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

    def __repr__(self) -> str:
        return f"Regex(regex={self.regex!r}, flags={self.flags})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, RegexRule)
            and self.regex == other.regex
            and self.flags == other.flags
        )

    def __hash__(self) -> int:
        return hash((self.regex, self.flags))

    async def __call__(self, event: Event, state: T_State) -> bool:
        try:
            msg = event.get_message()
        except Exception:
            return False
        if matched := re.search(self.regex, str(msg), self.flags):
            state[REGEX_MATCHED] = matched
            return True
        else:
            return False


def regex(regex: str, flags: Union[int, re.RegexFlag] = 0) -> Rule:
    """匹配符合正则表达式的消息字符串。

    可以通过 {ref}`nonebot.params.RegexStr` 获取匹配成功的字符串，
    通过 {ref}`nonebot.params.RegexGroup` 获取匹配成功的 group 元组，
    通过 {ref}`nonebot.params.RegexDict` 获取匹配成功的 group 字典。

    参数:
        regex: 正则表达式
        flags: 正则表达式标记

    :::tip 提示
    正则表达式匹配使用 search 而非 match，如需从头匹配请使用 `r"^xxx"` 来确保匹配开头
    :::

    :::tip 提示
    正则表达式匹配使用 `EventMessage` 的 `str` 字符串，
    而非 `EventMessage` 的 `PlainText` 纯文本字符串
    :::
    """

    return Rule(RegexRule(regex, flags))


class ToMeRule:
    """检查事件是否与机器人有关。"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "ToMe()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ToMeRule)

    def __hash__(self) -> int:
        return hash((self.__class__,))

    async def __call__(self, to_me: bool = EventToMe()) -> bool:
        return to_me


def to_me() -> Rule:
    """匹配与机器人有关的事件。"""

    return Rule(ToMeRule())


class IsTypeRule:
    """检查事件类型是否为指定类型。"""

    __slots__ = ("types",)

    def __init__(self, *types: Type[Event]):
        self.types = types

    def __repr__(self) -> str:
        return f"IsType(types={tuple(type.__name__ for type in self.types)})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, IsTypeRule) and self.types == other.types

    def __hash__(self) -> int:
        return hash((self.types,))

    async def __call__(self, event: Event) -> bool:
        return isinstance(event, self.types)


def is_type(*types: Type[Event]) -> Rule:
    """匹配事件类型。

    参数:
        types: 事件类型
    """

    return Rule(IsTypeRule(*types))


__autodoc__ = {
    "Rule": True,
    "Rule.__call__": True,
    "TrieRule": False,
    "ArgumentParser.exit": False,
    "ArgumentParser.parse_args": False,
}
