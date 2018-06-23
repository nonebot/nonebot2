import re
from typing import Tuple, Union, Callable, Iterable, Dict, Any, Optional

from aiocqhttp import CQHttp, Error as CQHttpError
from aiocqhttp.message import Message

from . import permissions as perm

# Key: str (one segment of command name)
# Value: subtree or a leaf Command object
_registry = {}

# Key: str
# Value: tuple that identifies a command
_aliases = {}

# Key: context source
# Value: Command object
_sessions = {}


class Command:
    __slots__ = ('name', 'func', 'permission')

    def __init__(self, name: Tuple[str], func: Callable, permission: int):
        self.name = name
        self.func = func
        self.permission = permission

    async def run(self, bot, ctx, session) -> Any:
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

        if isinstance(self.func, Callable) and permission & self.permission:
            return await self.func(bot, ctx, session)
        return None


def _find_command(name: Tuple[str]) -> Optional[Command]:
    if not name:
        return None

    cmd_tree = _registry
    for part in name[:-1]:
        if part not in cmd_tree:
            return None
        cmd_tree = cmd_tree[part]

    return cmd_tree.get(name[-1])


class Session:
    __slots__ = ('cmd', 'arg', 'arg_text',
                 'images', 'data', 'last_interaction')

    def __init__(self, cmd: Command, arg: str = ''):
        self.cmd = cmd
        self.arg = arg
        self.arg_text = Message(arg).extract_plain_text()
        self.images = []
        self.data = {}
        self.last_interaction = None


async def handle_command(bot: CQHttp, ctx: Dict[str, Any]) -> bool:
    # TODO: check if there is a session
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
        return False

    if not full_command:
        # command is empty
        return False

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
        return False

    session = Session(cmd=cmd, arg=''.join(cmd_remained))
    session.images = [s.data['url'] for s in ctx['message']
                      if s.type == 'image' and 'url' in s.data]
    await cmd.run(bot, ctx, session)
    return True


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
        current_parent[cmd_name[-1]] = Command(
            name=cmd_name, func=func, permission=permission)
        for alias in aliases:
            _aliases[alias] = cmd_name
        return func

    return deco
