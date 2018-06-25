import re
from collections import defaultdict
from typing import Tuple, Union, Callable, Iterable, Dict, Any, Optional

from aiocqhttp import CQHttp, Error as CQHttpError
from aiocqhttp.message import Message

from . import permissions as perm
from .helpers import context_source

# Key: str (one segment of command name)
# Value: subtree or a leaf Command object
_registry = {}

# Key: str
# Value: tuple that identifies a command
_aliases = {}

# Key: context source
# Value: list (stack) of Session objects
_sessions = defaultdict(list)


class Command:
    __slots__ = ('name', 'func', 'permission', 'args_parser')

    def __init__(self, name: Tuple[str], func: Callable, permission: int):
        self.name = name
        self.func = func
        self.permission = permission
        self.args_parser = None

    async def run(self, bot, session, *,
                  permission: int = None) -> bool:
        if permission is None:
            permission = await calculate_permission(bot, session.ctx)
        if isinstance(self.func, Callable) and permission & self.permission:
            if isinstance(self.args_parser, Callable):
                self.args_parser(session)
            await self.func(bot, session)
            return True
        return False


async def calculate_permission(bot: CQHttp, ctx: Dict[str, Any]) -> int:
    permission = 0
    if ctx['user_id'] in bot.config.SUPERUSERS:
        permission |= perm.IS_SUPERUSER
    if ctx['message_type'] == 'private':
        if ctx['sub_type'] == 'friend':
            permission |= perm.IS_PRIVATE_FRIEND
        elif ctx['sub_type'] == 'group':
            permission |= perm.IS_PRIVATE_GROUP
        elif ctx['sub_type'] == 'discuss':
            permission |= perm.IS_PRIVATE_DISCUSS
        elif ctx['sub_type'] == 'other':
            permission |= perm.IS_PRIVATE_OTHER
    elif ctx['message_type'] == 'group':
        permission |= perm.IS_GROUP_MEMBER
        if not ctx['anonymous']:
            try:
                member_info = await bot.get_group_member_info(**ctx)
                if member_info:
                    if member_info['role'] == 'owner':
                        permission |= perm.IS_GROUP_OWNER
                    elif member_info['role'] == 'admin':
                        permission |= perm.IS_GROUP_ADMIN
            except CQHttpError:
                pass
    elif ctx['message_type'] == 'discuss':
        permission |= perm.IS_DISCUSS
    return permission


def on_command(name: Union[str, Tuple[str]], aliases: Iterable = (),
               permission: int = perm.EVERYONE) -> Callable:
    def deco(func: Callable) -> Callable:
        if not isinstance(name, (str, tuple)):
            raise TypeError('the name of a command must be a str or tuple')
        if not name:
            raise ValueError('the name of a command must not be empty')

        cmd_name = name if isinstance(name, tuple) else (name,)
        current_parent = _registry
        for parent_key in cmd_name[:-1]:
            current_parent[parent_key] = {}
            current_parent = current_parent[parent_key]
        cmd = Command(name=cmd_name, func=func, permission=permission)
        current_parent[cmd_name[-1]] = cmd
        for alias in aliases:
            _aliases[alias] = cmd_name

        def args_parser(parser_func: Callable):
            cmd.args_parser = parser_func
            return parser_func

        func.args_parser = args_parser
        return func

    return deco


def _find_command(name: Union[str, Tuple[str]]) -> Optional[Command]:
    cmd_name = name if isinstance(name, tuple) else (name,)

    if not cmd_name:
        return None

    cmd_tree = _registry
    for part in cmd_name[:-1]:
        if part not in cmd_tree:
            return None
        cmd_tree = cmd_tree[part]

    return cmd_tree.get(cmd_name[-1])


class FurtherInteractionNeeded(Exception):
    """
    Raised by session.require_arg() indicating
    that the command should enter interactive mode
    to ask the user for some arguments.
    """
    pass


class Session:
    __slots__ = ('cmd', 'ctx',
                 'current_key', 'current_prompt',
                 'current_arg', 'current_arg_text',
                 'images', 'args', 'last_interaction')

    def __init__(self, cmd: Command, ctx: Dict[str, Any], *,
                 current_arg: str = '', args: Dict[str, Any] = None):
        self.cmd = cmd
        self.ctx = ctx
        self.current_key = None
        self.current_prompt = None
        self.current_arg = current_arg
        self.current_arg_text = Message(current_arg).extract_plain_text()
        self.images = [s.data['url'] for s in ctx['message']
                       if s.type == 'image' and 'url' in s.data]
        self.args = args or {}
        self.last_interaction = None

    def refresh(self, ctx: Dict[str, Any], *, current_arg: str = ''):
        self.ctx = ctx
        self.current_arg = current_arg
        self.current_arg_text = Message(current_arg).extract_plain_text()
        self.images = [s.data['url'] for s in ctx['message']
                       if s.type == 'image' and 'url' in s.data]

    @property
    def is_valid(self):
        # TODO: 检查 last_interaction
        return True

    def require_arg(self, key: str, prompt: str = None, *,
                    interactive: bool = True) -> Any:
        """
        Get an argument with a given key.

        If "interactive" is True, and the argument does not exist
        in the current session, a FurtherInteractionNeeded exception
        will be raised, and the caller of the command will know
        it should keep the session for further interaction with the user.

        If "interactive" is False, missed key will cause a result of None.

        :param key: argument key
        :param prompt: prompt to ask the user with
        :param interactive: should enter interactive mode while key missing
        :return: the argument value
        :raise FurtherInteractionNeeded: further interaction is needed
        """
        value = self.args.get(key)
        if value is not None or not interactive:
            return value

        self.current_key = key
        self.current_prompt = prompt or f'请输入 {self.current_key}：'
        raise FurtherInteractionNeeded


def _new_command_session(bot: CQHttp,
                         ctx: Dict[str, Any]) -> Optional[Session]:
    msg_text = str(ctx['message']).lstrip()

    for start in bot.config.COMMAND_START:
        if isinstance(start, type(re.compile(''))):
            m = start.search(msg_text)
            if m:
                full_command = msg_text[len(m.group(0)):].lstrip()
                break
        elif isinstance(start, str):
            if msg_text.startswith(start):
                full_command = msg_text[len(start):].lstrip()
                break
    else:
        # it's not a command
        return None

    if not full_command:
        # command is empty
        return None

    cmd_name_text, *cmd_remained = full_command.split(maxsplit=1)
    cmd_name = _aliases.get(cmd_name_text)

    if not cmd_name:
        for sep in bot.config.COMMAND_SEP:
            if isinstance(sep, type(re.compile(''))):
                cmd_name = tuple(sep.split(cmd_name_text))
                break
            elif isinstance(sep, str):
                cmd_name = tuple(cmd_name_text.split(sep))
                break
        else:
            cmd_name = (cmd_name_text,)

    cmd = _find_command(cmd_name)
    if not cmd:
        return None

    return Session(cmd, ctx, current_arg=''.join(cmd_remained))


async def handle_command(bot: CQHttp, ctx: Dict[str, Any]) -> bool:
    src = context_source(ctx)
    if _sessions[src]:
        session = _sessions[src][-1]
        session.refresh(ctx, current_arg=str(ctx['message']))
        # TODO: 检查 is_valid
    else:
        session = _new_command_session(bot, ctx)
        if not session:
            return False
        _sessions[src].append(session)

    try:
        res = await session.cmd.run(bot, session)
        # the command is finished, pop the session
        _sessions[src].pop()
        if not _sessions[src]:
            # session stack of the current user is empty
            del _sessions[src]
        return res
    except FurtherInteractionNeeded:
        # ask the user for more information
        await bot.send(ctx, session.current_prompt)

        # return True because this step of the session is successful
        return True


async def call_command(name: Union[str, Tuple[str]],
                       bot: CQHttp, ctx: Dict[str, Any], **kwargs) -> bool:
    """
    Call a command internally.

    There is no permission restriction on this function,
    which means any command can be called from any other command.
    Unexpected users should be handled by the caller command's permission
    option.

    :param name: command name (str or tuple of str)
    :param bot: CQHttp instance
    :param ctx: event context
    :param kwargs: other keyword args that will be passed to Session()
    :return: the command is successfully called
    """
    cmd = _find_command(name)
    if cmd:
        session = Session(cmd, ctx, **kwargs)
        # TODO: 插入 session
        return await cmd.run(bot, session, permission=perm.IS_SUPERUSER)
    return False
