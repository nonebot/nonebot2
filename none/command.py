import re
from typing import Tuple, Union, Callable, Iterable, Dict, Any

from aiocqhttp import CQHttp

from . import permissions as perm, logger

_command_tree = {}

# Key: str
# Value: tuple that identifies a command
_command_aliases = {}

# Key: context source
# Value: Command object
_command_sessions = {}


# TODO: Command 类只用来表示注册的命令，Session 类用来在运行时表示命令的参数等

class Command:
    __slots__ = ('name', 'arg', 'images', 'data', 'last_interaction')

    def __init__(self, name: Tuple[str]):
        self.name = name

    async def __call__(self, bot: CQHttp, ctx: Dict[str, Any],
                       *args, **kwargs) -> bool:
        logger.info(repr(self.images))
        cmd_tree = _command_tree
        for part in self.name:
            if part not in cmd_tree:
                return False
            cmd_tree = cmd_tree[part]
        cmd = cmd_tree
        if 'func' not in cmd or not isinstance(cmd['func'], Callable):
            return False
        # TODO: check permission
        await cmd['func'](bot, ctx, self)
        return True


async def handle_command(bot: CQHttp, ctx: Dict[str, Any]) -> bool:
    # TODO: check if there is a session
    msg_text = ctx['message'].extract_plain_text().lstrip()

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
    cmd_name = _command_aliases.get(cmd_name_text)

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

    cmd = Command(cmd_name)
    cmd.arg = ''.join(cmd_remained)
    cmd.images = [s.data['url'] for s in ctx['message']
                  if s.type == 'image' and 'url' in s.data]
    return await cmd(bot, ctx)


def on_command(name: Union[str, Tuple[str]], aliases: Iterable = (),
               permission: int = perm.EVERYONE) -> Callable:
    def deco(func: Callable) -> Callable:
        if not isinstance(name, (str, tuple)):
            raise TypeError('the name of a command must be a str or tuple')
        if not name:
            raise ValueError('the name of a command must not be empty')

        cmd_name = name if isinstance(name, tuple) else (name,)
        current_parent = _command_tree
        for parent_key in cmd_name[:-1]:
            current_parent[parent_key] = {}
            current_parent = current_parent[parent_key]
        current_parent[cmd_name[-1]] = {
            'name': cmd_name,
            'func': func,
            'permission': permission
        }
        for alias in aliases:
            _command_aliases[alias] = cmd_name
        return func

    return deco
